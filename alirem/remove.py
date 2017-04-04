#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
import alirem.basket as basket


class MyException(Exception):
    pass

class RemoveHandler(object):

    def __init__(self, is_dir,
                 is_recursive, is_interactive, is_dryrun,
                 is_basket, logger, basket_path='basket'):
        self.basket_path = basket_path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.is_basket = is_basket
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_removed = True

    def remove_empty_dir(self, path):
        if not self.is_dryrun:
            os.rmdir(path)

    def remove_file(self, path):
        if not self.is_dryrun:
            os.remove(path)

    def asking(self, msg):
        if self.is_interactive:
            print msg+'\n'
            answer = raw_input('[Y/n]\n')
            if answer != "n":
                return True
            else:
                return False
        else:
            return True

    def run_remove(self, path):
        if os.path.exists(path):
            if self.is_basket:
                if basket.move_to_basket(self.basket_path, path,
                                         self.is_dir, self.is_recursive, self.logger,
                                         self.is_dryrun, self.is_interactive) is True:
                    self.remove(path)
            else:
                self.remove(path)
        else:
            self.logger.log("Can not find such path", logging.ERROR)


    def remove(self, path):
        if os.path.isfile(path):
            if self.asking('Do u want to delete this file: {}?'.format(os.path.basename(path))):
                self.remove_file(path)
                self.logger.log("File {} deleted".format(os.path.basename(path)), logging.INFO, 0)
                return True
            else:
                return False
        elif os.path.isdir(path):
            # if self.asking('''Do u want to delete this directory:
            #                 {}?'''.format(os.path.basename(path))):
            self.remove_dir(path)
            return True


    def remove_dir(self, path):
        if not self.is_dir and not self.is_recursive:
            self.logger.log("cannot remove '{}', it's dir".format(path), logging.WARNING, 1)
        elif self.is_dir:
            if len(os.listdir(path)) != 0:
                self.logger.log("Directory {} not empty".format(path), logging.WARNING, 1)
            else:
                if self.asking('''Do u want to delete this empty directory:
                                  {}?'''.format(os.path.basename(path))):
                    self.remove_empty_dir(path)
                    self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                    logging.INFO, 0)
        elif self.is_recursive:
            b = True

            for obj in os.listdir(path):
                try:
                    if not self.remove(path + "/" + obj):
                        self.file_removed = False

                except OSError:
                    # self.logger.log("OSError", logging.ERROR)
                    b = False
                except MyException:
                    # self.logger.log("MyException", logging.ERROR)
                    b = False
            if b:
                if self.file_removed:
                # if len(os.listdir(path)) == 0 or self.is_dryrun:
                    if self.asking('''Do you want to delete this empty directory:
                                    {}?'''.format(os.path.basename(path))):
                        self.remove_empty_dir(path)
                        self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                        logging.INFO, 0)
                    else:
                        self.file_removed = False
            else:
                raise MyException()
