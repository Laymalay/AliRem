#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
import re
from os import listdir, mkdir, access, makedirs
from os.path import join, exists, isfile, basename, isdir, dirname, islink
import logging
import alirem.exception as exception
import alirem.progress as progress
import threading
import datetime

class CopyHandler(object):
    def __init__(self, logger, is_merge=False, is_replace=False,
                 is_dryrun=False, is_interactive=False, regexp=None,
                 symlinks=False, is_progress=True):
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_copied = True
        self.is_merge = is_merge
        self.is_replace = is_replace
        self.regexp = regexp
        self.symlinks = symlinks
        self.is_progress = is_progress

    def run(self, path, dst):
        if str(os.path.abspath(dst)).startswith(os.path.abspath(path)):
            self.logger.log("Error with moving <{}> to <{}>".format(path,
                                                                    dst),
                            logging.ERROR, exception.Error)
        try:
            self.copy(path, dst)
        except exception.PermissionDenied:
            if exists(dst):
                shutil.rmtree(dst)
            raise exception.PermissionDenied

    def copy(self, path, dst):
        if islink(path) and not self.symlinks:
            self.copy_symlink(path, dst)
            return True
        if not islink(path):
            if isfile(path):
                if self.copy_file(path, dst):
                    return True
                else:
                    return False
            if isdir(path):
                if os.access(path, os.R_OK) and os.access(path, os.W_OK) \
                                            and os.access(path, os.X_OK):
                    self.copy_dir(path, dst)
                    return True
                else:
                    return False

    def create_dir(self, path):
        if not self.is_dryrun:
            if exists(path) and not self.is_merge and not self.is_replace:
                self.logger.log("Name conflict, use merge or replace param",
                                logging.ERROR, exception.FileExists)
                return
            if self.is_replace and exists(path):
                shutil.rmtree(path)
                print 'create ', path
                mkdir(path)
                return
            if not exists(path) and self.is_merge:
                print 'create ', path
                mkdir(path)
                return
            if not exists(path):
                print 'create ', path
                mkdir(path)



    def copy_content(self, path, dst):
        for obj in listdir(path):
            if isfile(join(path, obj)):
                self.copy(join(path, obj), join(dst, obj))


    def copy_dir(self, path, dst):
        self.create_dir(dst)
        for obj in listdir(path):
            if isdir(os.path.abspath(join(path,obj))):
                self.copy(join(path, obj), join(dst, obj))

        t = threading.Thread(target= self.copy_content, args=(path,dst,))
        t.start()
        print datetime.datetime.now()
        print t, 'start'
        while t.is_alive():
            pass
        print t,'exiting'

        # for obj in listdir(path):
        #     if not self.copy(join(path, obj), join(dst, obj)):
        #         self.file_copied = False
        # if self.file_copied:
        #     self.logger.log("Directory {0} copied to {1}".format(os.path.basename(path), dst),
        #                     logging.INFO)



    def copy_file(self, path, dst):
        if self.check_regexp(path=path, regexp=self.regexp):
            if self.asking('\nDo u want to move this file: {0} to {1}?'.format(basename(path),
                                                                               dst)):
                if access(path, os.R_OK):
                    self.__copy_file(path, dst)
                    self.logger.log("Moved file {0} to the {1}".format(basename(path),
                                                                       dst), logging.INFO)
                    return True
                else:
                    self.logger.log("Permission Denied: {}".format(path), logging.ERROR,
                                    exception.PermissionDenied)

        else:
            return False


    def __copy_file(self, path, dst):
        if not self.is_dryrun:
            if self.is_progress:
                progress.show_progress(task=lambda: shutil.copyfile(path, dst),
                                       total_size=os.path.getsize(path),
                                       get_now_size=lambda: os.path.getsize(dst))
            else:
                shutil.copyfile(path, dst)


    def copy_symlink(self, src, dst):
        dest = os.path.dirname(dst)
        if not os.path.exists(dest):
            makedirs(dest)
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
        self.logger.log("Copy symlink \'{}\', to \'{}\'".format(src, dst), logging.INFO)

    def asking(self, msg):
        if self.is_interactive:
            print msg+'\n'
            answer = raw_input('[Y/n]\n')
            return answer != "n"
        else:
            return True

    def check_regexp(self, regexp, path):
        if regexp != None:
            rez = re.search(regexp, path)
            if rez != None:
                if rez.group(0) == path:
                    return True
            self.logger.log("File not copy '{}': Does not match the pattern.".format(path),
                            logging.INFO)
            return False
        else:
            return True

