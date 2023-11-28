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


pay_com_login_url = 'https://www.paycomonline.net/v4/ee/web.php/app/login'
pay_com_timec_url = 'https://www.paycomonline.net/v4/ee/web.php/timeclock/WEB04'
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

INDAY = 'in-day'
OUTLUNCH = 'out-lunch'
INLUNCH = 'in-lunch'
OUTDAY = 'out-day'


class gc_driver():
    cookie_path = 'data/pcm_cookies.csv'

    def __init__(self):
        load_dotenv()
        self.driver_path = Service(os.environ['GC_DRIVER_PATH'])
        self.gc_options = webdriver.ChromeOptions()
        self.gc_options.add_argument('--headless')
        self.gc_options.add_argument("--disable-extensions")
        self.gc_options.add_argument("--disable-gpu")
        self.gc_options.add_argument("--window-size=1920,1080")
        self.gc_options.add_argument("--disable-extensions")
        self.gc_options.add_argument("--proxy-server='direct://'")
        self.gc_options.add_argument("--proxy-bypass-list=*")
        self.gc_options.add_argument("--log-level=2")
        self.driver = webdriver.Chrome(
            service=self.driver_path, options=self.gc_options)

    def run_pcm(self):
        self.driver.get(pay_com_login_url)
        self.login()  # can fail if cookies expired or credentials are wrong
        self.driver.get(pay_com_timec_url)

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
            if self.driver.title == 'Employee Self-Service ®':
                print(
                    f'{"Logged in ":10s} [SUCCESS] - {dt.now().strftime("%I:%M:%S %p")}')
        except:
            logging.error(
                'Login [FAIL] : Check CSredentials + 2FA Cookie')
            self.driver.close()

    def link_punch(self, status):
        self.run_pcm()
        self.driver.get(f'{pay_com_timec_url}\\punch\\{status}')
        print(
            f'{status:10s} [SUCCESS] - {dt.now().strftime("%I:%M:%S %p")}')

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
                logging.error(f'Add Cookie [FAIL]: {key} ')
                break
        self.driver.refresh()

    def prev_mod_cookie(self):
        tfmt = "%m/%d/%Y"
        modification_time = os.path.getmtime(gc_driver.cookie_path)
        current_datetime = dt.now().strftime(tfmt)
        modification_datetime = dt.strptime(time.ctime(modification_time),
                                            "%a %b %d %H:%M:%S %Y").strftime(tfmt)
        delta = dt.strptime(current_datetime, tfmt) - \
            dt.strptime(modification_datetime, tfmt)
        # print(f"Modification datetime: {modification_datetime}")
        return f"{'Update 🍪':10s}[{30 - delta.days} Days]"
    
    def schedule_links(self):
        # schedule.every(25).minutes.do(self.reset_page_timer)       # instead of keeping the site live just relog???
        # ---------------------------------------------------------------------------------------
        schedule.every().monday.at("09:00").do(
            lambda: self.link_punch(INDAY))  # 9 AM EST
        schedule.every().monday.at("12:00").do(
            lambda: self.link_punch(OUTLUNCH))  # 12 PM EST
        schedule.every().monday.at("13:00").do(
            lambda: self.link_punch(INLUNCH))  # 1 PM EST
        schedule.every().monday.at("17:59").do(
            lambda: self.link_punch(OUTDAY))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().tuesday.at("09:00").do(
            lambda: self.link_punch(INDAY))  # 9 AM EST
        schedule.every().tuesday.at("12:00").do(
            lambda: self.link_punch(OUTLUNCH))  # 12 PM EST
        schedule.every().tuesday.at("13:00").do(
            lambda: self.link_punch(INLUNCH))  # 1 PM EST
        schedule.every().tuesday.at("17:59").do(
            lambda: self.link_punch(OUTDAY))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().wednesday.at("09:00").do(
            lambda: self.link_punch(INDAY))  # 9 AM EST
        schedule.every().wednesday.at("12:00").do(
            lambda: self.link_punch(OUTLUNCH))  # 12 PM EST
        schedule.every().wednesday.at("13:00").do(
            lambda: self.link_punch(INLUNCH))  # 1 PM EST
        schedule.every().wednesday.at("17:59").do(
            lambda: self.link_punch(OUTDAY))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().thursday.at("09:00").do(
            lambda: self.link_punch(INDAY))  # 9 AM EST
        schedule.every().thursday.at("12:00").do(
            lambda: self.link_punch(OUTLUNCH))  # 12 PM EST
        schedule.every().thursday.at("13:00").do(
            lambda: self.link_punch(INLUNCH))  # 1 PM EST
        schedule.every().thursday.at("17:59").do(
            lambda: self.link_punch(OUTDAY))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        schedule.every().friday.at("09:00").do(
            lambda: self.link_punch(INDAY))  # 9 AM EST
        schedule.every().friday.at("12:00").do(
            lambda: self.link_punch(OUTLUNCH))  # 12 PM EST
        schedule.every().friday.at("13:00").do(
            lambda: self.link_punch(INLUNCH))  # 1 PM EST
        schedule.every().friday.at("17:59").do(
            lambda: self.link_punch(OUTDAY))  # 5:59 PM EST
        # ---------------------------------------------------------------------------------------
        print(f'{"Scheduled":10s} [SUCCESS]')
        print(self.prev_mod_cookie())
        while True:
            schedule.run_pending()
            time.sleep(1)


script = gc_driver()
script.schedule_links()
# script.run_pcm()

