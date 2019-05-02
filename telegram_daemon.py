from logger import Logger
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.bot import Bot
import textwrap
from db_manager import DB_Manager
from sqlite3 import IntegrityError


class TelegramNotifier:
    def __init__(self, auth_token):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.db_manager = DB_Manager(check_same_thread=False)
        self.updater = Updater(auth_token, use_context=True)
        self.bot = Bot(auth_token)
        self.logger = Logger("telegram.log")
        self.logger.info("Starting the daemon...")

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    # update.to_dict =>

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        # add or update to the sqlite table.
        chat = update.message.chat
        user_tuple = self.db_manager.create_user_tuple(chat.id)
        self.db_manager.add_new_user(user_tuple)
        self.logger.info(
            'A new user with username: %s and chat_id: %s subscribed to the list.' % (chat.username, chat.id)
        )
        update.message.reply_text('Welcome! You have successfully subscribed to real time notification for a six '
                                  'scored in IPL 2019 cricket match.')

    def subscribe(self, update, context):
        """Send a message when the command /start is issued."""
        # add or update to the sqlite table.
        chat = update.message.chat
        user_tuple = self.db_manager.create_user_tuple(chat.id)
        try:
            status = self.db_manager.add_new_user(user_tuple)
        except IntegrityError:
            self.logger.info('Username: %s and chat_id: %s is already subscribed to the list.')
            update.message.reply_text('You are already subscribed to real time notification for a six '
                                      'scored in IPL 2019 cricket match.')
            return True
        self.logger.info(
            'Username: %s and chat_id: %s subscribed to the list.' % (chat.username, chat.id)
        )
        update.message.reply_text('Welcome! You have successfully subscribed to real time notification for a six '
                                  'scored in IPL 2019 cricket match.')

    def snooze(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text("You have successfully snoozed the notifications for the day.")
        # update to the sqlite table.
        chat = update.message.chat
        self.db_manager.snooze(chat.id)
        self.logger.info(
            'Username: %s with chat_id: %s snoozed the notifications for the day.' % (chat.username, chat.id))

    def remove_snooze(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text("You have successfully resumed the notifications for the day.")
        # update to the sqlite table.
        chat = update.message.chat
        self.db_manager.remove_snooze(chat.id)
        self.logger.info(
            'Username: %s with chat_id: %s resumed the notifications for the day.' % (chat.username, chat.id))

    def unsubscribe(self, update, context):
        """Send a message when the command /start is issued."""
        # remove or update to the sqlite table.
        chat = update.message.chat
        self.db_manager.remove_user(chat.id)
        self.logger.info(
            'Username: %s and chat_id: %s unsubscribed to the list.' % (chat.username, chat.id)
        )
        update.message.reply_text('You have successfully unsubscribed the notifications forever.')

    def swiggy_offer(self, update, context):
        """Send a message when the command /start is issued."""
        promotional_message = """Swiggy has an active IPL campaign going where you get clear 60% OFF in your order 
        upto Rs.75 for every six scored in IPL 2019 upto six minutes to the time when the six was scored using coupon 
        code: SWIGGY6, more information available at: http://6.swiggy.com """
        # remove or update to the sqlite table.
        self.bot.send_message(chat_id=update.message.chat_id, text=promotional_message, parse_mode='markdown')

    def echo(self, update, context):
        """Display help text."""
        standard_message = """
        Can't understand your action, try /help to find answer to your query.
        """
        self.bot.send_message(chat_id=update.message.chat_id, text=standard_message, parse_mode='markdown')

    def help(self, update, context):
        """Send a message when the command /help is issued."""
        help_message = textwrap.dedent("""
            1. /subscribe - To subscribe to sixes scored in IPL to avail 60% off swiggy coupon (SWIGGY6)
            2. /snooze - To snooze the notifications for sixes scored for the day.
            3. /removeSnooze - To resume the notifications for the day.
            4. /unsubscribe - To unsubscribe to the sixes scored notifications.
            5. /swiggyOffer - To know more about the ongoing swiggy offer.
        """)
        self.bot.send_message(chat_id=update.message.chat_id, text=help_message, parse_mode='markdown')

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.error('Update "%s" caused error "%s"' % (update, context.error))

    def main(self):
        """Start the bot."""
        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("subscribe", self.subscribe))
        dp.add_handler(CommandHandler("snooze", self.snooze))
        dp.add_handler(CommandHandler("removeSnooze", self.remove_snooze))
        dp.add_handler(CommandHandler("unsubscribe", self.unsubscribe))
        dp.add_handler(CommandHandler("swiggyOffer", self.swiggy_offer))
        dp.add_handler(CommandHandler("help", self.help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


if __name__ == "__main__":
    telegram_bot_key = "your-token"
    tn = TelegramNotifier(telegram_bot_key)
    tn.main()

# Chat object format:
# update.to_json() =>
# {
#    "update_id":107211934,
#    "message":{
#       "message_id":25,
#       "date":1555169655,
#       "chat":{
#          "id":418353901,
#          "type":"private",
#          "username":"ugupta41",
#          "first_name":"Ujjwal",
#          "last_name":"Gupta"
#       },
#       "text":"/subscribe",
#       "entities":[
#          {
#             "type":"bot_command",
#             "offset":0,
#             "length":10
#          }
#       ],
#       "caption_entities":[
#
#       ],
#       "photo":[
#
#       ],
#       "new_chat_members":[
#
#       ],
#       "new_chat_photo":[
#
#       ],
#       "delete_chat_photo":false,
#       "group_chat_created":false,
#       "supergroup_chat_created":false,
#       "channel_chat_created":false,
#       "from":{
#          "id":418353901,
#          "first_name":"Ujjwal",
#          "is_bot":false,
#          "last_name":"Gupta",
#          "username":"ugupta41",
#          "language_code":"en"
#       }
#    },
#    "_effective_user":{
#       "id":418353901,
#       "first_name":"Ujjwal",
#       "is_bot":false,
#       "last_name":"Gupta",
#       "username":"ugupta41",
#       "language_code":"en"
#    },
#    "_effective_chat":{
#       "id":418353901,
#       "type":"private",
#       "username":"ugupta41",
#       "first_name":"Ujjwal",
#       "last_name":"Gupta"
#    },
#    "_effective_message":{
#       "message_id":25,
#       "date":1555169655,
#       "chat":{
#          "id":418353901,
#          "type":"private",
#          "username":"ugupta41",
#          "first_name":"Ujjwal",
#          "last_name":"Gupta"
#       },
#       "text":"/subscribe",
#       "entities":[
#          {
#             "type":"bot_command",
#             "offset":0,
#             "length":10
#          }
#       ],
#       "caption_entities":[
#
#       ],
#       "photo":[
#
#       ],
#       "new_chat_members":[
#
#       ],
#       "new_chat_photo":[
#
#       ],
#       "delete_chat_photo":false,
#       "group_chat_created":false,
#       "supergroup_chat_created":false,
#       "channel_chat_created":false,
#       "from":{
#          "id":418353901,
#          "first_name":"Ujjwal",
#          "is_bot":false,
#          "last_name":"Gupta",
#          "username":"ugupta41",
#          "language_code":"en"
#       }
#    }
# }
