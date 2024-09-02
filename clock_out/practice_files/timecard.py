"""
Javascript button
document.evaluate(path, document, null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()

Button to get to the time sheet page ...
button_path = '//ul[@id="time-management-dropdown"]/li[position()=1]/a'

in_day = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'IN DAY')]"
out_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'OUT LUNCH')]"     
in_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'IN LUNCH')]"        
out_day = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'OUT DAY')]"


in_day set for 9 am
out_lunch set for 12 pm
in_lunch set for 1 pm
out_day set for 5:59 pm

//div[@id='time-clock-card']//div[@class='liveClock quickPunch']//p[contains(text(),'9:00:')]
//div[@id='time-clock-card']//div[@class='liveClock quickPunch']//p[contains(text(),'12:00:')]
//div[@id='time-clock-card']//div[@class='liveClock quickPunch']//p[contains(text(),'1:00:')]
//div[@id='time-clock-card']//div[@class='liveClock quickPunch']//p[contains(text(),'5:59:')]
"""

from datetime import datetime as dt
import time
import schedule
import pytz
# now = dt.now().strftime("%I:%M:%S %p")
# lunch_in = dt(year=dt.year,
#               month=dt.month,
#               day=dt.date,
#               hour=13, minute=0, second=0, microsecond=0)

in_day = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'IN DAY')]"
out_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'OUT LUNCH')]"
in_lunch = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'IN LUNCH')]"
out_day = "//div[@class='buttonContainer formGroup row btn-container']//button[contains(.,'OUT DAY')]"


def clock_in(xpath):
    clockin_btn = WebDriverWait(self.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    print(dt.now(pytz.timezone('US/Eastern')))


def start_scheduler():
    schedule.every().day.at("09:00").do(lambda: clock_in(in_day))  # 9 AM EST
    schedule.every().day.at("12:00").do(lambda: clock_in(out_lunch))  # 12 PM EST
    schedule.every().day.at("13:00").do(lambda: clock_in(in_lunch))  # 1 PM EST
    schedule.every().day.at("17:59").do(lambda: clock_in(out_day))  # 6 PM EST

    while True:
        schedule.run_pending()
        time.sleep(1)


print(dt.now(pytz.timezone('US/Eastern')))
start_scheduler()
