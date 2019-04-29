import sqlite3
from datetime import datetime


class DB_Manager:
    def __init__(self, check_same_thread=None):
        self.conn = sqlite3.connect('database.sqlite', check_same_thread=check_same_thread)
        self.cursor = self.conn.cursor()

    def get_active_subscribers(self):
        self.cursor.execute("SELECT * FROM `users` WHERE `snoozed_at` < datetime('now', 'localtime')")
        results = self.cursor.fetchall()
        return results

    @staticmethod
    def created_at_now():
        return datetime.now()

    @staticmethod
    def snoozed_at_tomorrow():
        now = datetime.now()
        return datetime(now.year, now.month, now.day+1)

    def add_new_user(self, user_tuple):
        self.cursor.execute("INSERT INTO `users` VALUES (?, ?, ?)", user_tuple)
        self.conn.commit()
        return True

    def create_user_tuple(self, chat_id):
        return int(chat_id), self.created_at_now(), self.created_at_now()

    def remove_user(self, chat_id):
        self.cursor.execute("DELETE FROM `users` WHERE `chat_id` = ?", (int(chat_id),))
        self.conn.commit()
        return True

    def snooze(self, chat_id):
        self.cursor.execute(
            "UPDATE `users` SET `snoozed_at` = ? WHERE `chat_id` = ?", (
                self.snoozed_at_tomorrow(),
                int(chat_id)
            )
        )
        self.conn.commit()
        return True

    def remove_snooze(self, chat_id):
        self.cursor.execute(
            "UPDATE `users` SET `snoozed_at` = ? WHERE `chat_id` = ?", (
                self.created_at_now(),
                int(chat_id)
            )
        )
        self.conn.commit()
        return True
