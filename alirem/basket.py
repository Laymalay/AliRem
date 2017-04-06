#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
from os import listdir, mkdir, access
from os.path import join, exists, isfile, basename, isdir
import logging
import datetime
import alirem.basket_list as basketlist
import alirem.exception as exception

class BasketHandler(object):
    def __init__(self, basket_path, path, is_dir,
                 is_recursive, logger,
                 is_dryrun, is_interactive, is_force):
        self.basket_path = basket_path
        self.path = path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_copied = True
        self.is_force = is_force
        self.basket_list = basketlist.BasketList()
        self.basket_list.load()

    def run(self):

        if not exists(self.basket_path):
            mkdir(self.basket_path)
            self.logger.log("Basket was created", logging.INFO)
        if self.check_flags():
            self.copy(self.path, self.basket_path)


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
            new_dst = join(dst, path)
            if not self.copy(join(path, obj), new_dst):
                self.file_copied = False

        if self.file_copied:
            if self.asking('''Do you want to move this directory to basket:
                            {}?'''.format(os.path.basename(path))):
                self.copy_empty_dir(path, dst)
                self.logger.log("Directory {} copied".format(os.path.basename(path)),
                                logging.INFO)
            else:
                self.file_copied = False

        else:
            if not self.is_force:
                self.logger.log("Permission Denied ",
                                logging.ERROR, exception.PermissionDenied)

    def copy_empty_dir(self, path, dst):
        # dst = join(self.basket_path, basename(path))
        # dst = self.check_in_basket(dst)
        if self.asking('Do u want to move this directory: {} to basket?'.format(basename(path))):
            self.check_access_and_copy_dir(path, dst)
            self.logger.log("Moved directory {} to the basket".format(basename(path)),
                            logging.INFO)

            return True
        else:
            return False


    def copy_file(self, path, dst):
        # dst = join(self.basket_path, basename(path))
        # dst = self.check_in_basket(dst)
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
                
                shutil.copyfile(path, os.path.dirname(dst))
                self.basket_list.add(basename(path), path,
                                     self.basket_path, dst, datetime.datetime.now())
                self.basket_list.save()
                return True
        else:
            return False

    def check_access_and_copy_dir(self, path, dst):
        if access(path, os.R_OK):
            if not self.is_dryrun:
                shutil.copytree(path, dst)
                self.basket_list.add(basename(path), path,
                                     self.basket_path, dst, datetime.datetime.now())
                self.basket_list.save()
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




















    def check_in_basket(self, path):
        path_check = join(self.basket_path, basename(path))

        if exists(path_check):
            index = 1
            while True:
                if not exists(path_check+'({})'.format(index)):
                    break
                index += 1
            new_name = path+'({})'.format(index)
        else:
            new_name = path

        return new_name

    def check_flags(self):
        if isdir(self.path):
            if (len(listdir(self.path)) != 0 and self.is_recursive
                    and not self.is_dir) or (len(listdir(self.path)) == 0
                                             and (self.is_dir or self.is_recursive)):
                return True
            else:
                if not self.is_recursive and not  self.is_dir:
                    self.logger.log("It's a directory", logging.ERROR, exception.ItIsDirectory)
                elif len(listdir(self.path)) != 0 and  self.is_dir:
                    self.logger.log("Directory not empty",
                                    logging.ERROR, exception.NotEmptyDirectory)
                    return False
        else:
            return True
