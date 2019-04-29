from telegram_notifier import TelegramNotifier
from scrape import Scraper
from logger import Logger
import schedule
import datetime
import time
from utils import catch_exceptions, with_logging

logger_instance = Logger("app.log")
logger_instance.info("Initialising the parameters...")
# configs

telegram_bot_key = "your-api-token"

match_days = [
    [20, 21, 22, 23, 0, 3],  # Monday (8pm-12am)
    [20, 21, 22, 23, 0],  # Tuesday (8pm-12am)
    [20, 21, 22, 23, 0],  # Wednesday (8pm-12am)
    [20, 21, 22, 23, 0],  # Thursday (8pm-12am)
    [20, 21, 22, 23, 0],  # Friday (8pm-12am)
    [16, 17, 18, 19, 20, 21, 22, 23, 0],  # Saturday (4pm-8pm, 8pm-12am)
    [16, 17, 18, 19, 20, 21, 22, 23, 0],  # Sunday (4pm-8pm, 8pm-12am)
]

sc = Scraper()
tn = TelegramNotifier(telegram_bot_key)


@catch_exceptions(cancel_on_failure=True)
@with_logging
def loop():
    logger_instance.info("Looking for a new ball...")
    data = sc.scrape()
    if data['status'] is True:
        if data['data']['status'] is True:
            logger_instance.info("Found a new six!")
            logger_instance.info(data['data'])
            tn.notify()


schedule.every(1).minutes.do(loop)

logger_instance.info("Initialization done. Starting the loop.")

while True:
    dt_now = datetime.datetime.now()
    current_day = dt_now.weekday()
    current_hour = dt_now.hour

    day_settings = match_days[current_day]
    status = current_hour in day_settings
    if status:
        schedule.run_pending()
    time.sleep(1)
