#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
import core.basket as b


class MyException(Exception):
    pass

class HandlerRemove(object):

    def __init__(self, is_dir, is_recursive, is_basket, basket_path, logger):
        self.basket_path = basket_path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.is_basket = is_basket
        self.logger = logger
    def run(self, path):
        for unit in path:
            if self.is_basket:
                b.go_basket(self.basket_path, unit, self.is_dir, self.is_recursive, self.logger)
            self.remove(unit)
    def remove(self, path):
        if os.path.isfile(path):
            os.remove(path)
            self.logger.log("File {} deleted".format(os.path.basename(path)), logging.INFO)
        elif os.path.isdir(path):
            self.remove_dir(path)
            self.logger.log("Directory {} deleted".format(os.path.basename(path)), logging.INFO)

    def remove_dir(self, path):
        if not self.is_dir and not self.is_recursive:
            self.logger.log("cannot remove '{}', it's dir".format(path), logging.WARNING)
        elif self.is_dir:
            if len(os.listdir(path)) != 0:
                self.logger.log("Directory {} not empty".format(path), logging.WARNING)
            else:
                os.rmdir(path)
                self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                logging.INFO)
        elif self.is_recursive:
            b = True
            for obj in os.listdir(path):
                try:
                    self.remove(path + "/" + obj)
                except OSError:
                    self.logger.log("OSError", logging.ERROR)
                    b = False
                except MyException:
                    self.logger.log("MyException", logging.ERROR)
                    b = False
            if b:
                os.rmdir(path)
                self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                logging.INFO)
            else:
                raise MyException()
