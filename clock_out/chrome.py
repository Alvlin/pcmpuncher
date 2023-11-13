import os
import time
import logging
import schedule
from csv import DictReader
from selenium import webdriver
from dotenv import load_dotenv
from datetime import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
# in_day = "//div[@name='button_container']//button[contains(text(),'IN DAY')]"
# out_lunch = "//div[@name='button_container']//button[contains(text(),'OUT LUNCH')]"
# in_lunch = "//div[@name='button_container']//button[contains(text(),'IN LUNCH')]"
# out_day = "//div[@name='button_container']//button[contains(text(),'OUT DAY')]"

in_day = "//*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-day')]"
out_lunch = "//*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/out-lunch')]"
in_lunch = "//*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/in-lunch')]"
out_day = "//*[contains(@data-url, '/v4/ee/web.php/timeclock/WEB04/punch/out-day')]"


class gc_driver():
    cookie_path = 'pcm_cookies.csv'

    def __init__(self):
        # start_time = time.time()
        load_dotenv()
        self.driver_path = Service(os.environ['GC_DRIVER_PATH'])
        self.gc_options = webdriver.ChromeOptions()
        self.gc_options.add_argument("--log-level=2")
        self.gc_options.add_argument('--headless')
        self.gc_options.add_argument("--window-size=1920,1080")
        self.gc_options.add_argument("--disable-extensions")
        self.gc_options.add_argument("--proxy-server='direct://'")
        self.gc_options.add_argument("--proxy-bypass-list=*")
        self.gc_options.add_argument("--disable-extensions")
        self.gc_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(
            service=self.driver_path, options=self.gc_options)
        # end_time = time.time()
        # print(f'Driver bootup took: {end_time-start_time}')  # took about 2 seconds to load

    def run_pcm(self):
        # start_time = time.time()
        pay_com_login_url = 'https://www.paycomonline.net/v4/ee/web.php/app/login'
        self.driver.get(pay_com_login_url)
        self.login()  # can fail if cookies expired or credentials are wrong
        self.navi2_clock_page()  # can fail if website updates and xpath is changed
        # end_time = time.time() # took about 6 seconds to log in and navigate
        # print(f'Loggin on and navigating took: {end_time-start_time}')
        # self.start_scheduler()
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
            logging.error(
                'Login Unsuccessful: Check credentials + 2fa cookie')
            self.driver.close()

    def navi2_clock_page(self):
        try:
            punch_page = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//ul[@class="cardLinks"]/li/a[@href="/v4/ee/web.php/timeclock/WEB04"]')))
            punch_page.click()
            print(f'Loaded Clock In Page @ {dt.now()}')
        except:
            logging.error('Could Not Enter Clock In Page - Check XPATH...')
            self.driver.close()

        # print(self.driver.page_source)

    def punch_in(self, xpath):
        # logging.warning(self.driver.page_source)      # caution of auto logging out
        # print(f'Attemping 2 punch {xpath}')
        try:
            self.run_pcm()  # relog [ About 8 seconds on a good day ]
            punch_in_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            punch_in_btn.click()
            print(f'Punched In @ {dt.now()}')
        except:
            logging.error(
                f'Punch In Was Unsuccessful... Check XPATH: {xpath} ')
            # reboot if cant punch
        # print(self.driver.page_source)

    def reset_page_timer(self):
        self.driver.refresh()
        print(f'Refreshing Page @ {dt.now()}')
        # print('--------------------------')
        # source = self.driver.page_source
        # soup = BeautifulSoup(source)
        # print(soup.prettify)

    def start_scheduler(self):
        # schedule.every(25).minutes.do(self.reset_page_timer)       # instead of keeping the site live just relog???
        # ---------------------------------------------------------------------------------------
        schedule.every().monday.at("09:00").do(
            lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().monday.at("12:00").do(
            lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().monday.at("13:00").do(
            lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().monday.at("17:59").do(
            lambda: self.punch_in(out_day))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().tuesday.at("09:00").do(
            lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().tuesday.at("12:00").do(
            lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().tuesday.at("13:00").do(
            lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().tuesday.at("17:59").do(
            lambda: self.punch_in(out_day))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().wednesday.at("09:00").do(
            lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().wednesday.at("12:00").do(
            lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().wednesday.at("13:00").do(
            lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().wednesday.at("17:59").do(
            lambda: self.punch_in(out_day))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().thursday.at("09:00").do(
            lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().thursday.at("12:00").do(
            lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().thursday.at("13:00").do(
            lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().thursday.at("17:59").do(
            lambda: self.punch_in(out_day))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().friday.at("09:00").do(
            lambda: self.punch_in(in_day))  # 9 AM EST
        schedule.every().friday.at("12:00").do(
            lambda: self.punch_in(out_lunch))  # 12 PM EST
        schedule.every().friday.at("13:00").do(
            lambda: self.punch_in(in_lunch))  # 1 PM EST
        schedule.every().friday.at("17:59").do(
            lambda: self.punch_in(out_day))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        # schedule.every().sunday.at("19:01").do(lambda: self.run_pcm())
        # schedule.every().sunday.at("19:02").do(lambda: self.run_pcm())
        print('Scheduled ...')
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_cookies_values(self):
        with open(gc_driver.cookie_path, encoding='utf-8-sig') as f:
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
                logging.error(f'Adding Cookie Fail: {key} ')
                break
        self.driver.refresh()


script = gc_driver()
script.start_scheduler()
