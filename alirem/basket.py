#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
from os import listdir, mkdir
from os.path import join, exists, isfile, basename, isdir
import logging
import datetime
import alirem.basket_list as basketlist


def asking(msg, is_interactive):
    if is_interactive:
        print msg+'\n'
        answer = raw_input('[Y/n]\n')
        if answer != "n":
            return True
        else:
            return False
    else:
        return True

def copy_file(path, dst, is_dryrun, basket_list, basket_path):
    if not is_dryrun:
        shutil.copyfile(path, dst)
        basket_list.add(basename(path), path, basket_path, dst, datetime.datetime.now())
        basket_list.save()

def copy_dir(path, dst, is_dryrun, basket_list, basket_path):
    if not is_dryrun:
        shutil.copytree(path, dst)
        basket_list.add(basename(path), path, basket_path,
                        dst, datetime.datetime.now())
        basket_list.save()

def move_to_basket(basket_path, path, is_dir, is_recursive, logger, is_dryrun, is_interactive):
    basket_list = basketlist.BasketList()
    basket_list.load()

    if not exists(basket_path):
        mkdir(basket_path)
        logger.log("Basket was created", logging.INFO)
    if isfile(path):
        try:
            dst = join(basket_path, basename(path))
            dst = check_in_basket(basket_path, dst)
            if asking('\nDo u want to move this file: {} to basket?'.format(basename(path)),
                      is_interactive):
                copy_file(path, dst, is_dryrun, basket_list, basket_path)
                logger.log("Moved file {} to the basket".format(basename(path)), logging.INFO)
                return True
            else:
                return False
        except IOError:
            logger.log("IOError: permission denied: '{}'".format(basename(path)),
                       logging.ERROR)
            return False

    if isdir(path):
        dst = join(basket_path, basename(path))
        dst = check_in_basket(basket_path, dst)
        try:
            if (len(listdir(path)) != 0 and is_recursive#check correct flags
                    and not is_dir) or (len(listdir(path)) == 0 and is_dir):
                if asking('Do u want to move this directory: {} to basket?'.format(basename(path)),
                          is_interactive):
                    copy_dir(path, dst, is_dryrun, basket_list, basket_path)
                    logger.log("Moved directory {} to the basket".format(basename(path)),
                               logging.INFO)
                    return True
                else:
                    return False
        except OSError:
            logger.log("OSError: permission denied: '{}'".format(basename(path)),
                       logging.ERROR)
            return False



def check_in_basket(basket_path, path):#return new name for file(with index)
    path_check = join(basket_path, basename(path))

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
