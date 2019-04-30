# SWiggySixNotifier

Gives notification settings on sixes scored in IPL within 6 minutes since it was scored that can be then used to avail discount on swiggy orders using coupon (SWIGGY6).

Bot can be accessed via telegram using the below link.

**Live at**: http://t.me/swiggySixNotifierBot

## Installation

In order to run your very own bot in your own server, follow up with these commands:

1. `python -m venv swiggysixnotifier`
2. `source swiggysixnotifier/bin/activate`
3. `pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. Create your own bot following telegram docs link: https://core.telegram.org/bots#3-how-do-i-create-a-bot
6. Add your API token of bot at main.py and telegram_daemon.py
7. `python main.py` (run on background using `screen` as a starter - recommended)
8. `python telegram_daemon.py` (run on background `screen` as a starter - recommended)
9. Done.
