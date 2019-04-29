import logging


class Logger:
    def __init__(self, log_filename):
        self.logging = logging
        self.logging.basicConfig(filename=log_filename, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level="INFO")

    def log(self, log_type, message):
        log_method = getattr(self.logging, log_type)
        log_method(message)

    def info(self, message):
        self.log("info", message)

    def debug(self, message):
        self.log("debug", message)

    def warning(self, message):
        self.log("warning", message)

    def error(self, message):
        self.log("error", message)

