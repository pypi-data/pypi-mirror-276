from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

chrome_options = webdriver.ChromeOptions()
user_data_dir = f'./cache/{self.__adb_device.device_serial}/chrome_cache'
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 "
    "Safari/537.36")
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-plugins-discovery')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
driver.execute_script("window.navigator.chrome = { runtime: {} };")
driver.execute_script("""
    Object.defineProperty(navigator, 'languages', {
        get: function() {
            return ['en-US', 'en'];
        }
    });
""")
driver.execute_script("""
    Object.defineProperty(navigator, 'plugins', {
        get: function() {
            return [1, 2, 3, 4, 5];
        }
    });
""")
driver.get(f'https://play.google.com/store/apps/details?id={package_name}')
time.sleep(10)