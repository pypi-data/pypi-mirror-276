# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  automation-fw-helper
# FileName:     uiautomation_proxy.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/06/03
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import time
import atexit
import requests
from poco.utils import six
from poco.pocofw import Poco
import poco.drivers.android as poco_driver
from poco.utils.device import default_device
from airtest.core.android.ime import YosemiteIme
from automation_fw_helper.common.log import logger
from airtest.core.error import AdbShellError, AirtestError
from poco.drivers.android.utils.installation import install, uninstall
from poco.drivers.android.uiautomation import PocoServicePackage, UiAutomatorPackage, KeepRunningInstrumentationThread, \
    AndroidPocoAgent

__all__ = ['AndroidUiautomationPoco']
this_dir = os.path.dirname(os.path.realpath(poco_driver.__file__))


class AndroidUiautomationPoco(Poco):

    def __init__(self, device=None, using_proxy=True, force_restart=False, use_airtest_input=False, **options):
        # 加这个参数为了不在最新的pocounit方案中每步都截图
        self.screenshot_each_action = True
        if options.get('screenshot_each_action') is False:
            self.screenshot_each_action = False

        self.device = device or default_device()

        self.adb_client = self.device.adb
        if using_proxy:
            self.device_ip = self.adb_client.host or "127.0.0.1"
        else:
            self.device_ip = self.device.get_ip_address()

        # save current top activity (@nullable)
        try:
            current_top_activity_package = self.device.get_top_activity_name()
        except AirtestError as e:
            # 在一些极端情况下，可能获取不到top activity的信息
            print(e)
            current_top_activity_package = None
        if current_top_activity_package is not None:
            current_top_activity_package = current_top_activity_package.split('/')[0]

        # install ime
        self.ime = YosemiteIme(self.adb_client)

        # install
        self._instrument_proc = None
        self._install_service()

        # forward
        self.forward_list = []
        if using_proxy:
            p0, _ = self.adb_client.setup_forward("tcp:10080")
            p1, _ = self.adb_client.setup_forward("tcp:10081")
            self.forward_list.extend(["tcp:%s" % p0, "tcp:%s" % p1])
        else:
            p0 = 10080
            p1 = 10081

        # start
        ready = self._start_instrument(p0, force_restart=force_restart)
        if not ready:
            # 之前启动失败就卸载重装，现在改为尝试kill进程或卸载uiautomator
            self._kill_uiautomator()
            ready = self._start_instrument(p0)

            if current_top_activity_package is not None:
                current_top_activity2 = self.device.get_top_activity_name()
                if current_top_activity2 is None or current_top_activity_package not in current_top_activity2:
                    self.device.start_app(current_top_activity_package, activity=True)

            if not ready:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")
        if ready:
            # 首次启动成功后，在后台线程里监控这个进程的状态，保持让它不退出
            self._keep_running_thread = KeepRunningInstrumentationThread(self, p0)
            self._keep_running_thread.start()

        endpoint = "http://{}:{}".format(self.device_ip, p1)
        agent = AndroidPocoAgent(endpoint, self.ime, use_airtest_input)
        super(AndroidUiautomationPoco, self).__init__(agent, **options)

    def _install_service(self):
        updated = install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug.apk'))
        return updated

    def _is_running(self, package_name):
        """
        use ps |grep to check whether the process exists

        :param package_name: package name(e.g., com.github.uiautomator)
                            or regular expression(e.g., poco|airtest|uiautomator|airbase)
        :return: pid or None
        """
        cmd = r' |echo $(grep -E {package_name})'.format(package_name=package_name)
        if self.device.sdk_version > 25:
            cmd = r'ps -A' + cmd
        else:
            cmd = r'ps' + cmd
        processes = self.adb_client.shell(cmd).splitlines()
        for ps in processes:
            if ps:
                ps = ps.split()
                return ps[1]
        return None

    def _start_instrument(self, port_to_ping, force_restart=False, max_retries=10):

        instrumentation_cmd = [
            'am', 'instrument', '-w', '-e', 'debug', 'false', '-e', 'class',
            f'{PocoServicePackage}.InstrumentedTestAsLauncher',
            f'{PocoServicePackage}/androidx.test.runner.AndroidJUnitRunner'
        ]

        def restart_service(inst_cmd: list):
            self._kill_uiautomator()
            self.adb_client.shell(f'am start -n {PocoServicePackage}/.TestActivity')
            self._instrument_proc = self.adb_client.start_shell(inst_cmd)

        if not force_restart:
            try:
                url = 'http:' + f'//{self.device_ip}:{port_to_ping}/uiautomation/connectionState'
                state = requests.get(url, timeout=10)
                state = state.json()
                if state.get('connected'):
                    # 如果 UiAutomation Service 已连接，则跳过启动。
                    return True
            except requests.exceptions.RequestException:
                pass

        if self._instrument_proc is not None:
            if self._instrument_proc.poll() is None:
                self._instrument_proc.kill()
            self._instrument_proc = None

        ready = False
        restart_service(inst_cmd=instrumentation_cmd)

        def cleanup_proc(proc):
            def wrapped():
                try:
                    proc.kill()
                except (Exception,):
                    pass

            return wrapped

        atexit.register(cleanup_proc(self._instrument_proc))

        time.sleep(2)
        attempt = 0
        for _ in range(max_retries):
            attempt = attempt + 1
            try:
                url = 'http:' + f'//{self.device_ip}:{port_to_ping}'
                requests.get(url, timeout=10)
                ready = True
                break
            except requests.exceptions.Timeout:
                logger.error("Timeout occurred, will not retry.")
                break
            except requests.exceptions.ConnectionError:
                if self._instrument_proc.poll() is not None:
                    logger.warning("[pocoservice.apk] instrumentation test server process is no longer alive")
                    stdout = self._instrument_proc.stdout.read()
                    stdout = stdout.decode('utf-8') if isinstance(stdout, bytes) else stdout
                    stderr = self._instrument_proc.stderr.read()
                    stderr = stderr.decode('utf-8') if isinstance(stderr, bytes) else stderr
                    if stdout:
                        stdout = stdout[2:] if stdout.startswith(r"\r\n") is True else stdout
                        stdout = stdout[:-2] if stdout.endswith(r"\r\n") is True else stdout
                        logger.error(f'[pocoservice.apk] stdout: {stdout}')
                    if stderr:
                        stderr = stderr[2:] if stderr.startswith(r"\r\n") is True else stderr
                        stderr = stderr[:-2] if stderr.endswith(r"\r\n") is True else stderr
                        logger.error(f'[pocoservice.apk] stderr: {stderr}')
                    break  # Exit the loop if the process is no longer alive
                time.sleep(1)
                logger.warning(f"still waiting for uiautomation ready. Attempt {attempt} of {max_retries}")
                if attempt < max_retries:
                    try:
                        self.adb_client.shell(
                            ['monkey', '-p', PocoServicePackage, '-c', 'android.intent.category.LAUNCHER', '1']
                        )
                    except (Exception,):
                        pass
                    self.adb_client.shell(f'am start -n {PocoServicePackage}/.TestActivity')
                    self._instrument_proc = self.adb_client.start_shell(instrumentation_cmd)
                else:
                    logger.warning("Reached maximum retries, restarting service.")
                    restart_service(inst_cmd=instrumentation_cmd)
                    attempt = 0  # Reset attempt counter after restart
                    continue
        return ready

    def _kill_uiautomator(self):
        """
        poco-service无法与其他instrument启动的apk同时存在，因此在启动前，需要杀掉一些可能的进程：
        比如 io.appium.uiautomator2.server, com.github.uiautomator, com.netease.open.pocoservice等

        :return:
        """
        pid = self._is_running("uiautomator")
        if pid:
            logger.warning('{} should not run together with "uiautomator". "uiautomator" will be killed.'.format(
                self.__class__.__name__))
            self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

            try:
                self.adb_client.shell(['kill', pid])
            except AdbShellError:
                # 没有root权限
                uninstall(self.adb_client, UiAutomatorPackage)

    def on_pre_action(self, action, ui, args):
        if self.screenshot_each_action:
            # airteset log用
            from airtest.core.api import snapshot
            msg = repr(ui)
            if not isinstance(msg, six.text_type):
                msg = msg.decode('utf-8') if isinstance(msg, bytes) else msg
            snapshot(msg=msg)

    def stop_running(self):
        logger.warning('[pocoservice.apk] stopping PocoService')
        self._keep_running_thread.stop()
        self._keep_running_thread.join(3)
        self.remove_forwards()
        self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

    def remove_forwards(self):
        for p in self.forward_list:
            self.adb_client.remove_forward(p)
        self.forward_list = []
