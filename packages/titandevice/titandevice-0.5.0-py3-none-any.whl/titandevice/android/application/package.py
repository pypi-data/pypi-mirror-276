import subprocess
from typing import Optional

import frida
from adbutils import AppInfo, adb_path

from titandevice.android.application.application import Application
from titandevice.utils.adb_utils import ADBUtils


class Package:
    __package_info: AppInfo = None

    def __init__(self, package_name, adb_device: ADBUtils):
        self.__package_name = package_name
        self.__adb_device = adb_device
        self.__frida_device = frida.get_device(adb_device.device_serial)

    @staticmethod
    def __check_package_info(func):
        def wrapper(self, *args, **kwargs):
            if self.__package_info is None:
                self.__package_info = self.__adb_device.get_package_info(self.__package_name)
            return func(self, *args, **kwargs)

        return wrapper

    @property
    def package_name(self) -> str:
        return self.__package_name

    @property
    @__check_package_info
    def version_name(self) -> str:
        return self.__package_info.version_name

    @property
    @__check_package_info
    def version_code(self) -> int:
        return self.__package_info.version_code

    @property
    @__check_package_info
    def first_install_time(self) -> int:
        return int(self.__package_info.first_install_time.timestamp() * 1000)

    @property
    @__check_package_info
    def last_update_time(self) -> int:
        return int(self.__package_info.last_update_time.timestamp() * 1000)

    @property
    @__check_package_info
    def signature(self) -> str:
        return self.__package_info.signature

    @property
    @__check_package_info
    def path(self) -> str:
        return self.__package_info.path

    @property
    @__check_package_info
    def sub_apk_paths(self) -> list[str]:
        return self.__package_info.sub_apk_paths

    @property
    def is_running(self):
        return self.__package_name in [running_app.identifier for running_app in
                                       self.__frida_device.enumerate_applications()]

    @property
    def app_info(self) -> Optional[Application]:
        if self.is_running:
            for running_app in self.__frida_device.enumerate_applications():
                if running_app.identifier == self.__package_name:
                    return Application(
                        running_app.identifier,
                        running_app.name,
                        running_app.parameters,
                        running_app.pid,
                        self.__adb_device,
                        self.__frida_device
                    )

    def start_adb(self) -> Application:
        self.__adb_device.app_start(self.__package_name)
        return self.app_info

    def stop_adb(self):
        self.__adb_device.app_stop(self.__package_name)
        return not self.is_running

    def stop_frida(self):
        self.__frida_device.kill(self.app_info.pid)
        return not self.is_running

    def kill_adb(self):
        self.__adb_device.app_kill(self.__package_name)
        return not self.is_running

    def pull_apk_file(self, output_path):
        package_info = self.__adb_device.shell(f"pm path {self.__package_name}")
        apk_path = package_info.split(":", 1)[1].strip()
        subprocess.run(
            [adb_path(), "-s", self.__adb_device.device_serial, "pull", apk_path, output_path]
        )
        return output_path
