import logging
import logging.config


class Logger(object):
    def Parser_mode(self, mode):
        if mode.upper() == 'INFO':
            return logging.INFO

        if mode.upper() == 'DEBUG':
            return logging.DEBUG

        if mode.upper() == 'WARNING':
            return logging.WARNING

        if mode.upper() == 'ERROR':
            return logging.ERROR

    def setup(self, mode_for_file, mode_for_cmd, path):
        mode_for_file = self.Parser_mode(mode_for_file)
        mode_for_cmd = self.Parser_mode(mode_for_cmd)
        logger = logging.getLogger('alirem')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path)
        fh.setLevel(mode_for_file)
        ch = logging.StreamHandler()
        ch.setLevel(mode_for_cmd)
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def __init__(self, mode_for_file, mode_for_cmd, path):
        self.logger = self.setup(mode_for_file, mode_for_cmd, path)
    def log(self, msg, level):
        self.logger.log(level, msg)
