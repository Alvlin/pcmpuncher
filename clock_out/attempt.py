import os
import time
from datetime import datetime as dt

cookie_path = 'data/pcm_cookies.csv'
tfmt = "%m/%d/%Y"
modification_time = os.path.getmtime(cookie_path)
current_datetime = dt.now().strftime(tfmt)
modification_datetime = dt.strptime(time.ctime(modification_time),
                                    "%a %b %d %H:%M:%S %Y").strftime(tfmt)
delta = dt.strptime(current_datetime, tfmt) - \
    dt.strptime(modification_datetime, tfmt)
print(f"Modification datetime: {modification_datetime}")
print(f"Refresh Cookies: {delta.days}")
