import frida

from titandevice.utils.adb_utils import ADBUtils


class Application:
    package_name: str
    name: str
    parameters: str
    pid: int

    def __init__(self, package_name, name, parameters, pid, adb_device: ADBUtils, frida_device: frida.core.Device):
        self.package_name = package_name
        self.name = name
        self.parameters = parameters
        self.pid = pid
        self.__adb_device = adb_device
        self.__frida_device = frida_device

    @property
    def is_front(self):
        front_app = self.__frida_device.get_frontmost_application()
        if front_app is not None:
            return front_app.identifier == self.package_name
        return False

    def click_button_by_text(self, text) -> bool:
        return self.__adb_device.click_button_by_text(text)

    def close_adb(self):
        self.__adb_device.close_package(self.package_name)
