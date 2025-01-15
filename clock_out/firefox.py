import os
import time
import logging
import schedule
from csv import DictReader, DictWriter
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
from datetime import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import simpledialog



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
    root = tk.Tk()
    root.withdraw()

    def __init__(self):    # Constructor run by default when object is called
        load_dotenv()      # loads in .env file (make sure there is a .env file)
        self.driver_path = Service(GeckoDriverManager().install())
        self.gc_options = webdriver.FirefoxOptions()
        # self.gc_options.add_argument('--headless')
        self.gc_options.add_argument("--width=1500")
        self.gc_options.add_argument("--height=900")
        self.gc_options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.gc_options.log.level = "trace"
        self.driver = webdriver.Firefox(
            service=self.driver_path, options=self.gc_options)
        
    def link_punch(self, status):
        self.run_pcm()
        self.driver.get(f'{pay_com_timec_url}\\punch\\{status}')
        print(
            f'{status:10s} [SUCCESS] - {dt.now().strftime("%I:%M:%S %p")}')

    def run_pcm(self):
        self.driver.get(pay_com_login_url)
        self.login()  # can fail if cookies expired or credentials are wrong
        self.driver.get(pay_com_timec_url)

    def login(self):
        self.load_cookies()
        try:
            username = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtlogin']")))
            userpass = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='txtpass']")))
            userpin = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='userpinid']")))
            submit_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSubmit']")))
            
            username.send_keys(os.environ['USER_NAME'])
            userpass.send_keys(os.environ['USER_PASS'])
            userpin.send_keys(os.environ['USER_PIN'])
            submit_btn.click()

            print("Title after page clicked" , self.driver.title)
            if self.driver.title == 'Employee Self-Service ®':  # must have space before ® to = success login
                print(
                    f'{"Logged in ":10s} [SUCCESS] - {dt.now().strftime("%I:%M:%S %p")}')
        except TimeoutError:
            print('Elements not found ')
            

    def retry_login(self):
            try:
                select_email = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//label[@for='factor_option0']")))
                send_code_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='btn-next']")))
                select_email.click()
                send_code_btn.click()

                while True:
                    user_input = simpledialog.askstring("Input", "Enter access code")
                    
                    if user_input is None:  # User clicked Cancel
                        continue  # Or handle cancellation differently
                        
                    try:
                        user_input = user_input 
                        break  # Exit loop if conversion successful
                    except ValueError:
                        print("Error", "Please enter a valid numeric code")
                        continue

                pin_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located ((By.XPATH, "//*[@id='pin']")))
                remember_device_btn = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//label[@for='remember_device']")))
                login_button = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='btn-verify']")))
                
                if user_input is not None:
                    user_input = int(user_input)
                    pin_input.send_keys(user_input)
                    remember_device_btn.send_keys(Keys.ENTER)
                    login_button.send_keys(Keys.ENTER)
                    WebDriverWait(self.driver, 50).until(lambda driver: driver.title == 'Employee Self-Service ®')

            except TimeoutError:
                print('Elements not found')
            
                # self.retry_login()

    # def get_autograb_cookie(self):
    #     try:
    #         cookies = self.driver.get_cookies()
    #         for cookie in cookies:
    #             if 'pcm-device-token-' in cookie['name']: 
    #                 print(cookie)
    #                 header = ['name', 'value', 'domain', 'path']
    #                 cookie_jar = {'name':cookie['name'],
    #                               'value':cookie['value'],
    #                               'domain':'www.paycomonline.net',
    #                               'path':'/'}
    #                 with open(gc_driver.cookie_path, mode='w', newline='') as f:
    #                     dict_write = DictWriter(f, fieldnames=header)
    #                     dict_write.writeheader()
    #                     dict_write.writerow(cookie_jar)
    #     except:
    #         print('cookie no longer exists')

    def get_cookies_values(self):
        with open(gc_driver.cookie_path, encoding='utf-8-sig') as f:
            dict_reader = DictReader(f)
            list_of_dicts = list(dict_reader)
        f.close()
        return list_of_dicts

    def load_cookies(self):
        cook_keys = self.get_cookies_values()
        print(cook_keys)
        if cook_keys:  #load only if its not empty string
            for key in cook_keys:
                try:
                    self.driver.add_cookie(key)
                except:
                    print("Failed to inject cookies")
                    print(key)
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
script.run_pcm()
# script.schedule_links()
