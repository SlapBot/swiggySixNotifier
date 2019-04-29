from telegram.ext import Updater, messagequeue as mq
from telegram.bot import Bot
from db_manager import DB_Manager
import textwrap


class TelegramNotifier:
    def __init__(self, auth_token):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.updater = Updater(auth_token, use_context=True)
        self.q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        self.bot = MQBot(auth_token, mqueue=self.q)

    def notify(self):
        db_manager = DB_Manager(False)
        subscribers = db_manager.get_active_subscribers()
        notification_message = textwrap.dedent("""
            Watch out! A new six was scored, use coupon (SWIGGY6) to avail 60% off in your order above 99rs on swiggy
            If you have already used the coupon for the day snooze the notifications using /snooze command.
        """)
        for subscriber in subscribers:
            self.bot.send_message(str(subscriber[0]), notification_message)
        return True


class MQBot(Bot):
    """A subclass of Bot which delegates send method handling to MQ"""
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments"""
        return super(MQBot, self).send_message(*args, **kwargs)
