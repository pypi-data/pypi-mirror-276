from titandevice.android.device.device import Device
from titandevice.android.frida.frida_device import FridaDevice


class FridaDeviceManager:
    def __init__(
            self, android_device: Device, frida_server_file_name_prefix: str,
            frida_server_install_path: str
    ):
        self.__android_device = android_device
        self.__frida_server_file_name_prefix = frida_server_file_name_prefix
        if not frida_server_install_path.endswith('/'):
            frida_server_install_path += '/'
        self.__frida_server_install_path = frida_server_install_path

    def get_all_frida_list(self):
        return [
            FridaDevice(self.__android_device, frida_server_path) for
            frida_server_path in
            self.get_all_frida_executable_file_path()
        ]

    def get_all_frida_executable_file_path(self) -> list[str]:
        files = self.__android_device.get_all_files(self.__frida_server_install_path)
        return [self.__get_frida_server_path(file) for file in files if
                file.startswith(self.__frida_server_file_name_prefix)]

    def uninstall_all(self):
        for frida in self.get_all_frida_list():
            frida.stop()
            frida.uninstall()

    def install_frida(self, input_frida_server_path: str):
        from titandevice.utils import get_file_name_from_path
        file_name = get_file_name_from_path(input_frida_server_path)
        self.__android_device.push(
            input_frida_server_path, self.__frida_server_install_path
        )
        frida_server_file_path = self.__frida_server_install_path + file_name
        self.__android_device.shell(
            'su -c chmod +x ' + frida_server_file_path
        )
        return self.__android_device.file_exists(frida_server_file_path)

    def __get_frida_server_path(self, frida_server_name: str) -> str:
        return f'{self.__frida_server_install_path}{frida_server_name}'

    def stop_all_frida(self):
        for frida in self.get_all_frida_list():
            frida.stop()

    def get_frida_by_path(self, frida_server_full_path):
        return FridaDevice(self.__android_device, frida_server_full_path)

    def get_frida_by_version(self, frida_version):
        for frida in self.get_all_frida_list():
            if frida.version == frida_version:
                return frida
        return None
