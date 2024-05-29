from titandevice.android import logger
from titandevice.android.application.package_manager import PackageManager
from titandevice.android.capture.capture_manager import CaptureManager
from titandevice.android.config import Config
from titandevice.utils import get_local_ip, find_free_port
from titandevice.utils.adb_utils import ADBUtils


# from titandevice.android.application.application_manager import ApplicationManager
# from titandevice.android.capture.capture_manager import CaptureManager
# from titandevice.android.frida.frida_device_manager import FridaDeviceManager
# from titandevice.exception import DeviceMustBeRootedException


class DeviceManager:

    @staticmethod
    def get_all_devices() -> list['DeviceManager']:
        return [DeviceManager(device) for device in ADBUtils.get_all_devices()]

    @staticmethod
    def get_device(serial: str) -> 'DeviceManager':
        return DeviceManager(ADBUtils(serial))

    __package_manager: PackageManager = None
    __capture_manager: CaptureManager = None

    def __init__(self, adb_device: 'ADBUtils'):
        if not adb_device.is_root:
            raise Exception(f'ADB device {adb_device.device_serial} must be rooted.')
        self.__adb_device = adb_device
        self.__config = Config.get_config(adb_device.device_serial)
        logger.debug(f'DeviceManager: {self.dict()} initialized.')

    def dict(self):
        device_info = self.__adb_device.dict()
        config_info = self.__config.dict()
        return {**device_info, **config_info}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.dict())

    def get_package_manager(self) -> PackageManager:
        if self.__package_manager is None:
            self.__package_manager = PackageManager(self.__adb_device)
        return self.__package_manager

    def get_capture_manager(self, host: str = None, port: int = None):
        if self.__capture_manager is None:
            if host is None:
                host = get_local_ip()
            if port is None:
                port = find_free_port()

            self.__capture_manager = CaptureManager(self.__adb_device, host, port)
        return self.__capture_manager

    # def get_capture_manager(self) -> CaptureManager:
    #     if self.__capture_manager is None:
    #         self.__capture_manager = CaptureManager(self.__adb_device)
    #     return self.__capture_manager
    #

    # def get_frida_manager(
    #         self, frida_server_file_name_prefix, frida_server_install_path
    # ):
    #     if not self.__adb_device.is_root:
    #         raise DeviceMustBeRootedException(self.device_serial)
    #     return FridaDeviceManager(
    #         self, frida_server_file_name_prefix, frida_server_install_path
    #     )
