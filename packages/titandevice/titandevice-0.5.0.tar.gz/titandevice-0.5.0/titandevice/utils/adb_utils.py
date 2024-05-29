from xml.etree import ElementTree

import adbutils
from adbutils import AdbDevice, AppInfo

from titandevice.android import logger


class ADBUtils:
    @staticmethod
    def get_all_devices() -> list['ADBUtils']:
        return [ADBUtils(device) for device in adbutils.adb.device_list()]

    def __init__(self, device: str | AdbDevice):
        if isinstance(device, str):
            self.__adb_device = adbutils.adb.device(device)
        else:
            self.__adb_device = device

    @property
    def device_serial(self) -> str:
        return self.__adb_device.serial

    @property
    def model(self):
        return self.__adb_device.prop.model

    @property
    def device(self):
        return self.__adb_device.prop.device

    @property
    def ip(self):
        try:
            return self.__adb_device.wlan_ip()
        except Exception as e:
            logger.exception(e)
            return 'Unknown IP'

    @property
    def os_version(self):
        return self.__adb_device.shell("getprop ro.build.version.release").strip()

    @property
    def is_root(self):
        return self.file_exists('/system/bin/su')

    def dict(self):
        return {
            "device_serial": self.device_serial,
            "model": self.model,
            "device": self.device,
            "os_version": self.os_version,
            "is_root": self.is_root,
            "ip": self.ip
        }

    def __str__(self):
        return f'ADBUtils: {self.dict()}'

    def file_exists(self, file_path: str) -> bool:
        try:
            result = self.__adb_device.shell(f"test -e {file_path} && echo 'exists' || echo 'not exists'")
            return 'exists' in result
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False

    def get_package_info(self, package_name) -> AppInfo:
        return self.__adb_device.app_info(package_name)

    def list_packages(self) -> list[str]:
        return self.__adb_device.list_packages()

    def install(self, local_package_path, uninstall, nolaunch, silent):
        self.__adb_device.install(local_package_path, uninstall=uninstall, nolaunch=nolaunch, silent=silent)

    def uninstall(self, package_name):
        self.__adb_device.uninstall(package_name)

    def shell(self, param, sudo=False):
        if sudo:
            return self.__adb_device.shell(f"su -c '{param}'")
        return self.__adb_device.shell(param)

    def app_start(self, package_name):
        self.__adb_device.app_start(package_name)

    def app_current(self):
        return self.__adb_device.app_current()

    def app_stop(self, package_name):
        self.__adb_device.app_stop(package_name)

    def app_kill(self, package_name):
        self.shell(f"am kill -f {package_name}", True)

    def click_button_by_text(self, text) -> bool:
        try:
            dump_xml = self.__adb_device.dump_hierarchy()
            ui_root = ElementTree.fromstring(dump_xml)
        except Exception as e:
            logger.error(f"Failed to dump or parse UI hierarchy: {e}")
            return False

        for ui_node in ui_root.findall('.//node'):
            ui_node_text = ui_node.get('text', '')
            if ui_node_text == text:
                try:
                    bounds = ui_node.get('bounds')

                    # 计算中心点
                    bounds_values = bounds.split('][')
                    x1_y1 = bounds_values[0].strip().replace('[', '')
                    x2_y2 = bounds_values[1].strip().replace(']', '')
                    x1, y1 = map(int, x1_y1.split(','))
                    x2, y2 = map(int, x2_y2.split(','))
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2

                    self.__adb_device.click(center_x, center_y)
                    return True
                except Exception as e:
                    logger.error(f"Failed to click on the node: {e}")
                    return False
        return False

    def close_package(self, package_name):
        self.__adb_device.app_stop(package_name)
