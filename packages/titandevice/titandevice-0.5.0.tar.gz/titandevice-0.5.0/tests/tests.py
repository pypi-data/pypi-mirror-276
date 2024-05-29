import time

from titandevice.android import logger
from titandevice.android.device.device_manager import DeviceManager

pixel3_device_serial = '8CMX1R4CQ'
pixel6_device_serial = '19301FDF6006EP'
oppo_device_serial = 'CMBUOBVGS8ZTN7QO'
xiaomi_device_serial = '7d1e8258'

wechat_package_name = 'com.tencent.mm'
weread_package_name = 'com.tencent.weread'


def install_from_google_play_test():
    device = DeviceManager.get_device(pixel6_device_serial)
    package_manager = device.get_package_manager()
    apps = [
        "com.aipersona.camera",
        "com.aqua.marine.connect.game",
        "com.araraapp",
        "com.asdjdh.qbcia",
        "com.bigcake.android.hexaconnect",
        "com.bp.tracker.pressure",
        "com.card2048.game.akal",
        "com.client.tenderu.android",
        "com.htit.golden.star.game",
        "com.hub.pinkyclub",
        "com.hwsj.club",
        "com.hypersoft.supermovie",
        "com.iweetalk",
        "com.lagg.animal.world.game",
        "com.lion.ditapro",
        "com.live.bling.android",
        "com.lucky.toktube",
        "com.luinnovations.lrsdom",
        "com.mercadolibre",
        "com.online.network.procy.manager",
        "com.pet.translator.dog.cat",
        "com.pg868_4.kwai",
        "com.piia.bubble.match",
        "com.piia.merge.balls",
        "com.piia.merge.fruits",
        "com.sun.moon.dory",
        "com.super.drxf",
        "com.sweetdonut.game",
        "com.touch.chat",
        "com.ufadgwda.vhuebda",
        "com.video.welive",
        "com.waterworld.games.tap.seasynth",
        "com.zuma.deluxe.marble.puzzle",
        "game.onelinedraw.com",
        "mattk.fairygame.famr.com"
    ]
    for app_name in apps:
        package_manager.install_package_with_google_play(app_name)
    for app_name in apps:
        package_manager.get_package(app_name).pull_apk_file(f"./cache/apks/{app_name}.apk")

    # package_manager.install_package_with_google_play(weread_package_name)


def package_manager_test():
    device = DeviceManager.get_device(pixel3_device_serial)
    package_manager = device.get_package_manager()
    installed_packages = package_manager.get_installed_packages()
    for package in installed_packages:
        if package.package_name == wechat_package_name:
            package.start_adb()


def device_manager_test():
    devices = DeviceManager.get_all_devices()
    print(devices)
    device = DeviceManager.get_device(pixel3_device_serial)
    print(device)


def print_all_packages():
    device = DeviceManager.get_device(pixel3_device_serial)
    package_manager = device.get_package_manager()
    installed_packages = package_manager.get_installed_packages()
    for package in installed_packages:
        print(package.package_name)


def capture_wechat_applet():
    applet_uri = ('MiniProgram://weixin?username=gh_a4298ecbd7c2&path=/pages/webview/webview?u=https%3A%2F%2Fwww'
                  '.shanghaidisneyresort.com%2fecoupon%2fproducts%2fcoupon-center&utm_source=mango&utm_medium=otv'
                  '&utm_campaign=202405-brand-may_jun&utm_content=202405brandotvmini029&utm_term=na')
    device = DeviceManager.get_device(pixel3_device_serial)
    logger.debug('DeviceManager initialized.')
    package_manager = device.get_package_manager()
    logger.debug('PackageManager initialized.')
    if package_manager.is_package_installed(wechat_package_name):
        logger.debug('WeChat is installed.')
        package_manager.clear_wechat_applet_cache()
        logger.debug('WeChat applet cache cleared.')
        capture_manager = device.get_capture_manager()
        logger.debug('CaptureManager initialized.')
        capture_manager.start_capture()
        logger.debug('Capture started.')
        package_manager.start_imgotv_deep_link(applet_uri)
        logger.debug('Deep link started.')
        logger.debug('Waiting for 5 minutes...')
        time.sleep(60 * 5)
        package_manager.close_adb(wechat_package_name)
        logger.debug('WeChat closed.')
        capture_manager.stop_capture()
        logger.debug('Capture stopped.')
        sa_flows = capture_manager.search_by_host('data.sensors.shanghaidisneyresort.com')
        for flow in sa_flows:
            logger.info(flow.request.url)
            logger.info(flow.request.text)


if __name__ == '__main__':
    # device_manager_test()
    # package_manager_test()
    # print_all_packages()
    # install_from_google_play_test()
    capture_wechat_applet()
