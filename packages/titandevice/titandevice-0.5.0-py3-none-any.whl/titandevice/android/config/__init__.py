import json
import os

CONFIG_PATH = './cache/android/titan_config.json'
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({}, f)


class Config:
    __device_serial: str
    __frida_server_file_name_prefix: str
    __frida_server_install_path: str

    def __init__(self, device_serial: str, frida_server_file_name_prefix: str, frida_server_install_path: str):
        self.__device_serial = device_serial
        self.__frida_server_file_name_prefix = frida_server_file_name_prefix
        self.__frida_server_install_path = frida_server_install_path

    @property
    def device_serial(self):
        return self.__device_serial

    @device_serial.setter
    def device_serial(self, value):
        self.__device_serial = value
        self.write_config(self)

    @property
    def frida_server_file_name_prefix(self):
        return self.__frida_server_file_name_prefix

    @frida_server_file_name_prefix.setter
    def frida_server_file_name_prefix(self, value):
        self.__frida_server_file_name_prefix = value
        self.write_config(self)

    @property
    def frida_server_install_path(self):
        return self.__frida_server_install_path

    @frida_server_install_path.setter
    def frida_server_install_path(self, value):
        self.__frida_server_install_path = value
        self.write_config(self)

    def __str__(self):
        return f"Config: {self.dict()}"

    @staticmethod
    def get_config(device_serial: str) -> 'Config':
        with open(CONFIG_PATH, 'r') as file:
            configs = json.load(file)
            if device_serial not in configs:
                return Config(device_serial, '', '')
            return Config(**configs[device_serial])

    @staticmethod
    def write_config(config: 'Config'):
        with open(CONFIG_PATH, 'r') as file:
            configs = json.load(file)
            configs[config.__device_serial] = config.dict()
        with open(CONFIG_PATH, 'w') as file:
            json.dump(configs, file)

    def dict(self):
        return {
            'device_serial': self.__device_serial,
            'frida_server_file_name_prefix': self.__frida_server_file_name_prefix,
            'frida_server_install_path': self.__frida_server_install_path
        }
