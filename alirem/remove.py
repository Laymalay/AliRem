#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
import alirem.basket as basket
import alirem.exception as exception


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
        if os.access(path, os.R_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
            if not self.is_dryrun:
                os.rmdir(path)
                return True
        else:
            self.logger.log("Permission Denied rm",
                            logging.ERROR, exception.PermissionDenied)
            return False

    def remove_file(self, path):
        if os.access(path, os.R_OK):
            if not self.is_dryrun:
                os.remove(path)
                return True
        else:
            self.logger.log("Permission Denied rm",
                            logging.ERROR, exception.PermissionDenied)
            return False

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
                baskethandler = basket.BasketHandler(self.basket_path, path,
                                                     self.is_dir, self.is_recursive, self.logger,
                                                     self.is_dryrun, self.is_interactive)

                baskethandler.run()
                self.remove(path)

            else:
                self.remove(path)
        else:
            self.logger.log("Can not find such path", logging.ERROR, exception.NoSuchPath)

    def remove(self, path):
        if os.path.isfile(path):
            if self.asking('Do u want to delete this file: {}?'.format(os.path.basename(path))):
                if self.remove_file(path):
                    self.logger.log("File {} deleted".format(os.path.basename(path)), logging.INFO)
                    return True

            return False
        elif os.path.isdir(path):
            if os.access(path, os.R_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
                self.remove_dir(path)
                return True
            else:
                return False


    def remove_dir(self, path):
        if not self.is_dir and not self.is_recursive:
            self.logger.log("cannot remove '{}', it's dir".format(path),
                            logging.ERROR, exception.ItIsDirectory)
        elif self.is_dir:
            if len(os.listdir(path)) != 0:
                self.logger.log("Directory {} not empty".format(path),
                                logging.ERROR, exception.NotEmptyDirectory)
            else:
                if self.asking('''Do u want to delete this empty directory:
                                  {}?'''.format(os.path.basename(path))):
                    self.remove_empty_dir(path)
                    self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                    logging.INFO)
        elif self.is_recursive:

            for obj in os.listdir(path):
                if not self.remove(path + "/" + obj):
                    self.file_removed = False

            if self.file_removed:
                if len(os.listdir(path)) == 0 or self.is_dryrun:
                    if self.asking('''Do you want to delete this empty directory:
                                    {}?'''.format(os.path.basename(path))):
                        self.remove_empty_dir(path)
                        self.logger.log("Directory {} deleted".format(os.path.basename(path)),
                                        logging.INFO)
                    else:
                        self.file_removed = False

