#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
import re
import alirem.basket_handler as BasketHandler
import alirem.exception as exception
import alirem.progress as progress

class RemoveHandler(object):
    def __init__(self, logger=None, is_dir=False,
                 is_recursive=False, is_interactive=False, is_dryrun=False,
                 is_basket=False, basket_path='basket', regexp=None,
                 symlinks=False, is_progress=False):
        self.basket_path = basket_path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.is_basket = is_basket
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_removed = True
        self.regexp = regexp
        self.symlinks = symlinks
        self.used_slinks = []
        self.is_progress = is_progress

    def remove(self, path):
        if os.path.islink(path):
            if self.symlinks:
                self.go_to_link(path)
            self.unlink(path)
        else:
            self._remove(path)

    def unlink(self, path):
        if not self.is_dryrun:
            os.unlink(path)
        self.logger.log("Symlink '{}' removed".format(path), logging.INFO)

    def go_to_link(self, path):
        inode = os.stat(path).st_ino
        realpath = os.path.basename(os.readlink(path))
        # os.path.relpath(os.path.abspath(os.readlink(src)))
        if inode not in self.used_slinks:
            self.used_slinks.append(inode)
            self._remove(realpath)

    def remove_empty_dir(self, path):
        if os.access(path, os.R_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
            self.__remove_empty_dir(path)
            return True
        else:
            self.logger.log("Permission Denied rm",
                            logging.ERROR, exception.PermissionDenied)
            return False

    def __remove_file(self, path):
        if not self.is_dryrun:
            if self.is_progress:
                progress.show_progress(task=lambda: os.remove(path),
                                       total_size=os.path.getsize(path),
                                       get_now_size=lambda: os.path.getsize(path))
            else:
                os.remove(path)

    def __remove_empty_dir(self, path):
        if not self.is_dryrun:
            os.rmdir(path)


    def remove_file(self, path):
        if os.access(path, os.R_OK):
            self.__remove_file(path)
            return True
        else:
            self.logger.log("Permission Denied rm",
                            logging.ERROR, exception.PermissionDenied)
            return False

    def asking(self, msg):
        if self.is_interactive:
            print msg+'\n'
            answer = raw_input('[Y/n]\n')
            return bool(answer != "n")
        else:
            return True

    def _remove(self, path):
        if os.path.exists(path):
            if self.is_basket:
                baskethandler = BasketHandler.BasketHandler(basket_path=self.basket_path, path=path,
                                                            is_dir=self.is_dir,
                                                            is_recursive=self.is_recursive,
                                                            logger=self.logger,
                                                            is_dryrun=self.is_dryrun,
                                                            is_interactive=self.is_interactive,
                                                            regexp=self.regexp,
                                                            symlinks=self.symlinks,
                                                            is_progress=self.is_progress)

                baskethandler.move_to_basket()
                self.__remove(path)

            else:
                self.__remove(path)
        else:
            self.logger.log("Can not find such path: {}".format(path),
                            logging.ERROR, exception.NoSuchPath)

    def __remove(self, path):
        if os.path.islink(path):
            if self.symlinks:
                self.go_to_link(path)
            self.unlink(path)
            return True

        if os.path.isfile(path):
            if self.check_regexp(path=path, regexp=self.regexp):
                if self.asking('Do u want to delete this file: {}?'.format(os.path.basename(path))):
                    if self.remove_file(path):
                        self.logger.log("File {} deleted".format(os.path.basename(path)),
                                        logging.INFO)
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
                if not self.__remove(path + "/" + obj):
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


    def check_regexp(self, regexp, path):
        if regexp != None:
            rez = re.search(regexp, path)
            if rez != None:
                if rez.group(0) == path:
                    return True
            self.logger.log("File not deleted '{}': Does not match the pattern.".format(path),
                            logging.INFO)
            return False
        else:
            return True
