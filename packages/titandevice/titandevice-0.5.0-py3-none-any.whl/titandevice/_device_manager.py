import os.path
import subprocess
import time
from typing import Optional

import apkutils2
from adbutils import adb, adb_path

from ._device_exception import *
from ._device_models import DeviceInfo, FridaInfo, PackageInfo, AppInfo


class _DeviceManager(object):
    _device: adb.device
    _serial: str
    _is_root: bool = False
    _device_info: Optional[DeviceInfo] = None

    @staticmethod
    def check_is_root(func):
        def wrapper(self, *args, **kwargs):
            if not self._is_root:
                raise DeviceMustBeRootedException(self._serial)
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, device_serial: str):
        if device_serial not in [device.serial for device in adb.device_list()]:
            raise DeviceNoFoundException(device_serial)
        self._serial = device_serial
        self._device = adb.device(device_serial)
        self._is_root = self.__is_root()

    @staticmethod
    def get_all_device_manager_list() -> list["_DeviceManager"]:
        return [
            _DeviceManager(device.serial)
            for device in adb.device_list()
        ]

    @staticmethod
    def get_frida_server_name_from_path(frida_server_path: str) -> str:
        return os.path.basename(frida_server_path)

    def __get_frida_pid(self, frida_server_name) -> str:
        return self._device.shell(f"pgrep {frida_server_name}").strip()

    def __is_frida_running(self, frida_server_name) -> bool:
        return self._device.shell(f"pgrep {frida_server_name}").strip() != ""

    def __is_frida_installed(self, frida_server_path) -> bool:
        return self.__file_exists(frida_server_path)

    def __get_frida_version(self, frida_server_path) -> str | None:
        if not self.__is_frida_installed(frida_server_path):
            return None
        return self._device.shell(
            f"su -c {frida_server_path} --version"
        ).strip()

    def __file_exists(self, path: str) -> bool:
        return 'No such file or directory' not in self._device.shell(
            f"ls {path}"
        ).strip()

    def __is_root(self):
        return self.__file_exists("/system/xbin/su") or self.__file_exists(
            "/system/bin/su"
        )

    def get_device_info(self) -> DeviceInfo:
        if self._device_info is None:
            self._device_info = DeviceInfo(
                serial=self._device.serial,
                product=self._device.prop.name,
                model=self._device.prop.model,
                device=self._device.prop.device,
                is_root=self._is_root,
            )
        return self._device_info

    @check_is_root
    def install_frida(self, input_file_path, frida_server_path):
        self._device.push(input_file_path, frida_server_path)
        self._device.shell(f"su -c chmod +x {frida_server_path}")
        time.sleep(0.1)
        return self.get_frida_info(frida_server_path)

    @check_is_root
    def get_frida_info(self, frida_server_path, frida_server_name=None) -> FridaInfo:
        if frida_server_name is None:
            frida_server_name = self.get_frida_server_name_from_path(frida_server_path)
        return FridaInfo(
            is_running=self.__is_frida_running(frida_server_name),
            is_installed=self.__is_frida_installed(frida_server_path),
            version=self.__get_frida_version(frida_server_path)
        )

    @check_is_root
    def start_frida(self, frida_server_path):
        if not self.__is_frida_installed(frida_server_path):
            raise FridaServerNotInstalledException(self._serial, frida_server_path)
        subprocess.Popen(
            [adb_path(), '-s', self._serial, 'shell', 'nohup',
             'su -c "{}" &'.format(frida_server_path)]
        )
        time.sleep(0.1)
        return self.get_frida_info(frida_server_path)

    @check_is_root
    def stop_frida(self, frida_server_path):
        frida_server_name = self.get_frida_server_name_from_path(frida_server_path)
        if not self.__is_frida_running(frida_server_name):
            raise FridaServerNotRunningException(self._serial, frida_server_name)
        self._device.shell(f"su -c kill -9 {self.__get_frida_pid(frida_server_name)}")
        time.sleep(0.1)
        return self.get_frida_info(frida_server_path)

    @check_is_root
    def uninstall_frida(self, frida_server_path):
        if not self.__is_frida_installed(frida_server_path):
            raise FridaServerNotInstalledException(self._serial, frida_server_path)
        self._device.shell(f"su -c rm {frida_server_path}")
        time.sleep(0.1)
        return self.get_frida_info(frida_server_path)

    def __is_package_installed(self, package_name: str) -> bool:
        return package_name in self.get_installed_packages()

    def get_installed_packages(self) -> list[str]:
        return self._device.list_packages()

    def get_package_info(self, package_name: str) -> PackageInfo:
        if not self.__is_package_installed(package_name):
            raise PackageNotInstalledException(self._serial, package_name)
        app_info = self._device.app_info(package_name)
        return PackageInfo(
            package_name=app_info.package_name,
            version_name=app_info.version_name,
            version_code=app_info.version_code,
            flags=app_info.flags,
            first_install_time=app_info.first_install_time.timestamp(),
            last_update_time=app_info.last_update_time.timestamp(),
            path=app_info.path,
            sub_apk_paths=app_info.sub_apk_paths
        )

    def install_package(
            self, package_path: str, uninstall=False, no_launch=True
    ) -> PackageInfo:
        apk = apkutils2.APK(package_path)
        package_name = apk.manifest.package_name
        if (not uninstall) and self.__is_package_installed(package_name):
            raise InstallPackageMustUninstallFirstException(self._serial, package_name)
        self._device.install(package_path, uninstall=uninstall, nolaunch=no_launch)
        return self.get_package_info(package_name)

    def uninstall_package(self, package_name) -> list[str]:
        if not self.__is_package_installed(package_name):
            raise PackageNotInstalledException(self._serial, package_name)
        self._device.uninstall(package_name)
        return self.get_installed_packages()

    def start_package(self, package_name, activity=None) -> AppInfo:
        if not self.__is_package_installed(package_name):
            raise PackageNotInstalledException(self._serial, package_name)
        self._device.app_start(package_name, activity)
        time.sleep(0.1)
        return self.get_current_app()

    def stop_package(self, package_name) -> AppInfo:
        if not self.__is_package_installed(package_name):
            raise PackageNotInstalledException(self._serial, package_name)
        self._device.app_stop(package_name)
        time.sleep(0.1)
        return self.get_current_app()

    def get_current_app(self) -> AppInfo:
        app_current = self._device.app_current()
        return AppInfo(
            package=app_current.package,
            activity=app_current.activity,
            pid=app_current.pid
        )
