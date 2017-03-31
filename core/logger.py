import logging
import logging.config


class Logger(object):
    def setup(self):
        logger = logging.getLogger('alirem')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler('alirem.log')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def __init__(self):
        self.logger = self.setup()
    def log(self, msg, level):
        self.logger.log(level, msg)
