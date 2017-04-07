#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
from os import listdir, mkdir, access, makedirs
from os.path import join, exists, isfile, basename, isdir, dirname
import logging
import datetime
import alirem.basket_list as basketlist
import alirem.exception as exception

class CopyHandler(object):
    def __init__(self, logger, is_force,
                 is_dryrun=None, is_interactive=None):
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_copied = True
        self.is_force = is_force

    def run(self, path, dst):
        self.copy(path, dst)

    def copy(self, path, dst):

        if isfile(path):
            if self.copy_file(path, dst):
                return True
            else:
                return False
        if isdir(path):

            if os.access(path, os.R_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
                self.copy_dir(path, dst)
                return True
            else:
                return False



    def copy_dir(self, path, dst):
        for obj in listdir(path):
            if not self.copy(join(path, obj), join(dst, obj)):
                self.file_copied = False
        if self.file_copied:
            self.logger.log("Directory {} copied".format(os.path.basename(path)),
                            logging.INFO)
        else:
            if not self.is_force:
                self.logger.log("Permission Denied ",
                                logging.ERROR, exception.PermissionDenied)



    def copy_file(self, path, dst):
        if self.asking('\nDo u want to move this file: {} to basket?'.format(basename(path))):
            if self.check_access_and_copy_file(path, dst):
                self.logger.log("Moved file {} to the basket".format(basename(path)), logging.INFO)

                return True
            else:
                return False
        else:
            return False


    def check_access_and_copy_file(self, path, dst):
        if access(path, os.R_OK):
            if not self.is_dryrun:
                if not exists(dirname(dst)):
                    makedirs(dirname(dst))
                shutil.copyfile(path, dst)
                return True
        else:
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



