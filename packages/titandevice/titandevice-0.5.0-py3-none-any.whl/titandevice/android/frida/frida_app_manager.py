import frida

from titandevice.android.frida.frida_app import FridaApp


class FridaAppManager:

    def __init__(self, android_device):
        self.__android_device = android_device
        self.__frida_device = frida.get_device(self.__android_device.__device_serial)

    def get_all_running_app(self):
        return [FridaApp(self.__frida_device, application) for application in
                self.__frida_device.enumerate_applications()]

    def is_app_running(self, app_name):
        return app_name in [app.name for app in self.get_all_running_app()]

    def get_app(self, app_name):
        for app in self.get_all_running_app():
            if app.package_name == app_name:
                return app
        return None
