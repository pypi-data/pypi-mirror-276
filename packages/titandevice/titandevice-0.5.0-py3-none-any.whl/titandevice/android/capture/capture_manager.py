import datetime
import os
import subprocess
import threading

from mitmproxy import http
from mitmproxy.io import io, FlowReader

from titandevice.utils.adb_utils import ADBUtils


class CaptureManager:

    def __init__(self, adb_devices: ADBUtils, host, port):
        self.__adb_device = adb_devices
        self.__proxy_host = host
        self.__proxy_port = port
        self.__mitmproxy_process = None
        self.__capture_thread = None
        mitmdump_path = f"./cache/android/mitmdump/{self.__adb_device.device_serial}/"
        os.makedirs(mitmdump_path, exist_ok=True)
        self.__capture_dump_file = os.path.abspath(os.path.join(
            mitmdump_path,
            "dump_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.text')
        )
        self.__capture_flow_list = None

    def set_system_proxy(self):
        self.__adb_device.shell(f'settings put global http_proxy {self.__proxy_host}:{self.__proxy_port}')

    def is_system_proxy_set(self):
        return self.get_system_proxy() != 'null'

    def get_system_proxy(self):
        return self.__adb_device.shell('settings get global http_proxy')

    def clear_system_proxy(self):
        self.__adb_device.shell('settings put global http_proxy :0')
        self.__adb_device.shell('settings delete global http_proxy')

    def start_capture(self):
        if not self.is_system_proxy_set():
            self.set_system_proxy()
        if self.get_system_proxy() != f'{self.__proxy_host}:{self.__proxy_port}':
            self.set_system_proxy()
            return self.start_capture()

        def run_write_file_mitmproxy():
            try:
                self.__mitmproxy_process = subprocess.Popen(
                    ['mitmdump', '-w', self.__capture_dump_file, '-p', str(self.__proxy_port)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as e:
                print(f"Unexpected error: {e}")

        self.__capture_thread = threading.Thread(target=run_write_file_mitmproxy)
        self.__capture_thread.start()

    def stop_capture(self):
        self.clear_system_proxy()
        if self.__mitmproxy_process:
            self.__mitmproxy_process.terminate()
            self.__mitmproxy_process.wait()
        if self.__capture_thread:
            self.__capture_thread.join()

    def get_capture_flow_list(self) -> list[http.HTTPFlow]:
        if self.__capture_flow_list is None:
            self.__read_capture_to_memory()
        return self.__capture_flow_list

    def get_capture_flow_list_from_file(self, file_path):
        with open(file_path, 'rb') as log_file:
            flow_reader: FlowReader = io.FlowReader(log_file)
            self.__capture_flow_list = [f for f in flow_reader.stream() if isinstance(f, http.HTTPFlow)]
        return self.__capture_flow_list

    def __read_capture_to_memory(self):
        with open(self.__capture_dump_file, 'rb') as log_file:
            if self.__capture_flow_list is None:
                self.__capture_flow_list = []
            flow_reader: FlowReader = io.FlowReader(log_file)
            for f in flow_reader.stream():
                try:
                    if isinstance(f, http.HTTPFlow):
                        if f not in self.__capture_flow_list:
                            self.__capture_flow_list.append(f)
                except Exception as e:
                    print(e)

    def search_by_host(self, host) -> list[http.HTTPFlow]:
        return [f for f in self.get_capture_flow_list() if f.request.host == host]

    def get_mitmproxy_dump_file(self):
        return self.__capture_dump_file
