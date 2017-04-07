#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import logging.config



class Logger(object):
    def __init__(self, mode_for_file, mode_for_cmd, path, is_silent, is_force):
        self.is_silent = is_silent
        self.logger = self.setup(mode_for_cmd, path, mode_for_file)
        self.is_force = is_force

    def parser_mode(self, mode):
        if mode.upper() == 'INFO':
            return logging.INFO

        if mode.upper() == 'DEBUG':
            return logging.DEBUG

        if mode.upper() == 'WARNING':
            return logging.WARNING

        if mode.upper() == 'ERROR':
            return logging.ERROR

    def setup(self, mode_for_cmd, path, mode_for_file=None):
        logger = logging.getLogger('alirem')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

        if mode_for_file is not None:
            mode_for_file_parsed = self.parser_mode(mode_for_file)
            filehandler = logging.FileHandler(path+'.log')
            filehandler.setLevel(mode_for_file_parsed)
            filehandler.setFormatter(formatter)
            jsonfilehandler = logging.FileHandler(path+'.json')
            jsonfilehandler.setLevel(mode_for_file_parsed)
            formatter_json = logging.Formatter((
                ',\n'
                '{\n'
                '   "asctime": "%(asctime)s",\n'
                '   "name":"%(name)s",\n'
                '   "levelname": "%(levelname)s",\n'
                '   "message":  "%(message)s"\n'
                '}'))
            jsonfilehandler.setFormatter(formatter_json)
            logger.addHandler(jsonfilehandler)
            logger.addHandler(filehandler)

        mode_for_cmd_parsed = self.parser_mode(mode_for_cmd)


        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(mode_for_cmd_parsed)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)

        return logger

    def log(self, msg, level, error=None):
        if not self.is_silent:
            self.logger.log(level, msg)
        if error is not None and not self.is_force:
            raise error()




