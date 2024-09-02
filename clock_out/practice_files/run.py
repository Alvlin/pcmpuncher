from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from csv import DictReader
import os
from dotenv import load_dotenv
from datetime import datetime as dt
import time
import schedule
import pytz

in_day = "//div[@name='button_container']//button[contains(text(),'IN DAY')]"
out_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(text(),'OUT LUNCH')]"
in_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(text(),'IN LUNCH')]"
out_day = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(text(),'OUT DAY')]"
# //*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-lunch')]
# //*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-lunch')]
# //*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-lunch')]
# //*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-lunch')]


class ff_driver():
    # profile = webdriver.FirefoxProfile(
    #     'C:\\Users\\alvin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\tzkyst80.default-release')
    # profile.set_preference("dom.webdriver.enabled", False)
    # profile.set_preference('useAutomationExtension', False)
    # profile.update_preferences()
    cookie_path = 'pcm_cookies.csv'

    def __init__(self):
        load_dotenv()
        self.driver_path = Service(os.environ['DRIVER_PATH'])
        self.ff_options = Options()
        self.ff_options.add_argument('--headless')
        self.ff_options.add_argument("--window-size=1920,1080")
        self.ff_options.add_argument("--disable-extensions")
        self.ff_options.add_argument("--proxy-server='direct://'")
        self.ff_options.add_argument("--proxy-bypass-list=*")
        self.ff_options.add_argument("--disable-extensions")
        self.ff_options.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(
            service=self.driver_path, options=self.ff_options)

    def boot_ff(self):
        pay_com_login_url = 'https://www.paycomonline.net/v4/ee/web.php/app/login'
        self.driver.get(pay_com_login_url)
        self.login()  # can fail if cookies expired or credentials are wrong
        self.navi2_clock_page()  # can fail if website updates and xpath is changed
        self.start_scheduler()
        # print(self.driver.page_source)
        # self.driver.close()

    def login(self):
        self.load_cookies()
        try:
            username = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id= 'txtlogin']")))
            userpass = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id= 'txtpass']")))
            userpin = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id= 'userpinid']")))
            submit_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id= 'btnSubmit']")))
            username.send_keys(os.environ['USER_NAME'])
            userpass.send_keys(os.environ['USER_PASS'])
            userpin.send_keys(os.environ['USER_PIN'])
            submit_btn.click()
            print('Successfully logged in')
        except:
            print('couldnt login - check credentials + 2fa cookie')
            self.driver.close()

    def navi2_clock_page(self):
        try:
            punch_page = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//ul[@class="cardLinks"]/li/a[@href="/v4/ee/web.php/timeclock/WEB04"]')))
            punch_page.click()
            print('In Clock In Page')
        except:
            print('Could Not Enter Clock In Page - Check XPATH...')
            self.driver.close()

        # print(self.driver.page_source)

    def punch_in(self, xpath):
        print('refreshing the page')
        self.driver.refresh()
        print(self.driver.page_source)      # checker
        print(f'punching card @ {xpath}')
        print(dt.now(pytz.timezone('US/Eastern')))
        try:
            punch_in_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            punch_in_btn.click()
        except:
            print("No button Found to punch in - Check XPATH")
        # print(self.driver.page_source)

    def start_scheduler(self):
        schedule.every().day.at("09:00").do(lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().day.at("12:00").do(lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().day.at("13:00").do(lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().day.at("17:59").do(lambda: self.punch_in(out_day))  # 5:59 PM EST
        print('waiting now')
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_cookies_values(self):
        with open(ff_driver.cookie_path, encoding='utf-8-sig') as f:
            dict_reader = DictReader(f)
            list_of_dicts = list(dict_reader)
        f.close()
        return list_of_dicts

    def load_cookies(self):
        cook_keys = self.get_cookies_values()
        for key in cook_keys:
            try:
                self.driver.add_cookie(key)
            except:
                print(f'this couldnt be added {key}')
        self.driver.refresh()


script = ff_driver()
script.boot_ff()
