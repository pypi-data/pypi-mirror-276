import base64
import time

import apkutils2

from titandevice.android import logger
from titandevice.android.application.package import Package
from titandevice.exception import GooglePlayIsNotInstalledException, PackageNotInstalledException
from titandevice.utils.adb_utils import ADBUtils


class PackageManager:
    __adb_device: ADBUtils
    __google_play_account: str = None
    __google_play_password: str = None

    def __init__(self, adb_device):
        self.__adb_device = adb_device

    def get_installed_packages(self) -> list[Package]:
        return [Package(package_name, self.__adb_device) for package_name in self.__adb_device.list_packages()]

    def is_package_installed(self, package_name: str) -> bool:
        return package_name in self.__adb_device.list_packages()

    def get_package(self, package_name) -> Package:
        return Package(package_name, self.__adb_device)

    def install_package(self, local_package_path: str, uninstall=True, no_launch=True):
        apk = apkutils2.APK(local_package_path)
        package_name = apk.manifest.package_name
        self.__adb_device.install(
            local_package_path, uninstall=uninstall, nolaunch=no_launch, silent=True
        )
        return self.is_package_installed(package_name)

    def is_google_play_installed(self) -> bool:
        return self.is_package_installed('com.android.vending')

    def install_package_with_google_play(self, package_name):
        if not self.is_google_play_installed():
            raise GooglePlayIsNotInstalledException(self.__adb_device.device_serial)
        logger.debug(f'Installing package {package_name} with Google Play.')
        self.__adb_device.shell(f'am start -a android.intent.action.VIEW -d "market://details?id={package_name}"')
        play_package = self.get_package("com.android.vending")
        play_app = play_package.app_info
        if play_app is not None:
            if not play_app.is_front:
                logger.debug(f'Google Play is not in front, waiting for 0.1 seconds.')
                time.sleep(0.1)
            logger.debug(f'Google Play is in front, run click to install.')
            self.__adb_device.click_button_by_text("取消")
            self.__adb_device.click_button_by_text("安装")

    def uninstall_package(self, package_name) -> bool:
        self.__adb_device.uninstall(package_name)
        return not self.is_package_installed(package_name)

    def start_imgotv_deep_link(self, uri: str):
        if not uri.startswith('imgotv://'):
            if uri.startswith('MiniProgram://'):
                uri = f'imgotv://weixin_jump?weixin_parameter={base64.b64encode(uri.encode()).decode()}'
            if uri.startswith('weixin://'):
                uri = f'imgotv://weixin_jump?weixin_parameter={base64.b64encode(uri.encode()).decode()}'
        self.__adb_device.shell(f'am start -d "{uri}"')

    def clear_wechat_applet_cache(self) -> bool:
        package_name = 'com.tencent.mm'
        if not self.is_package_installed(package_name):
            raise PackageNotInstalledException(self.__adb_device.device_serial, package_name)
        logger.debug(f'Clearing WeChat applet cache.')
        wechat_package = self.get_package(package_name)
        wechat_app = wechat_package.start_adb()
        logger.debug(f'Checking if WeChat is in front.')
        while not wechat_app.is_front:
            logger.debug(f'WeChat is not in front, waiting for 0.1 seconds.')
            wechat_app = wechat_package.start_adb()
        time.sleep(10)
        success = False
        try:
            logger.debug(f'Clicking.')
            if not wechat_app.click_button_by_text("我"):
                raise Exception("Click 我 failed.")
            if not wechat_app.click_button_by_text("设置"):
                raise Exception("Click 设置 failed.")
            if not wechat_app.click_button_by_text("通用"):
                raise Exception("Click 通用 failed.")
            if not wechat_app.click_button_by_text("存储空间"):
                raise Exception("Click 存储空间 failed.")
            wechat_app.click_button_by_text("前往清理")
            wechat_app.click_button_by_text("清理")
            wechat_app.click_button_by_text("清理")
            time.sleep(1)

            logger.debug('Clearing WeChat applet cache successfully.')
            # 激活小程序防止白屏
            self.start_imgotv_deep_link('weixin://dl/business/?appid=wxbecffbf7bd411cc3&path=pages/notes/today&query'
                                        '=utm_campaign=gf&utm_medium=gf&utm_source=gf')

            logger.debug('Waiting for 5 seconds to open WeChat applet.')
            time.sleep(10)
        except Exception as e:
            logger.error(f"Clear wechat applet cache error: {e}")
        logger.debug('Closing WeChat.')
        wechat_app.close_adb()
        return success

    def close_adb(self, package_name):
        self.__adb_device.close_package(package_name)
