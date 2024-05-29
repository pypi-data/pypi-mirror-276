import typing

import _frida
from frida import core
from frida.core import Session, Script


class FridaApp:
    @staticmethod
    def __check_is_attached(func):
        def wrapper(self, *args, **kwargs):
            if self.__session is None:
                raise Exception('请先调用attach方法')
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, frida_device: core.Device, application: _frida.Application):
        self.__frida_device = frida_device
        self.name = application.name
        self.package_name = application.identifier
        self.pid = application.pid
        self.parameters = application.parameters
        self.__session: typing.Optional[Session] = None

    def dict(self):
        return {
            'name': self.name,
            'package_name': self.package_name,
            'pid': self.pid,
            'is_running': self.is_running(),
            'parameters': self.parameters
        }

    def is_running(self):
        return self.pid != 0

    def attach(self):
        if self.__session is not None:
            self.__session.detach()
        self.__session = self.__frida_device.attach(self.pid)
        return self.__session

    @__check_is_attached
    def create_script_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            return self.create_script(file.read())

    @__check_is_attached
    def create_script(self, script: str):
        script: Script = self.__session.create_script(script)
        script.on('message', lambda message, data: print(message))
        script.load()
