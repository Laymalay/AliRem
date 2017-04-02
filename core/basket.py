#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
from os import listdir, mkdir
from os.path import join, exists, isfile, basename, isdir
import logging
import datetime
import alirem.core.basket_list as basketlist

def move_to_basket(basket_path, path, is_dir, is_recursive, logger):
    basket_list = basketlist.BasketList()
    basket_list.load()

    if not exists(basket_path):
        mkdir(basket_path)
        logger.log("Basket was created", logging.INFO)
    if isfile(path):
        try:
            file_path = join(basket_path, basename(path))
            file_path = check_in_basket(basket_path, file_path)
            shutil.copyfile(path, file_path)
            basket_list.add(basename(path), path, basket_path, file_path, datetime.datetime.now())
            basket_list.save()
            logger.log("Moved file {} to the basket".format(basename(path)), logging.INFO)
            return True
        except IOError:
            logger.log("IOError: permission denied: '{}'".format(basename(path)),
                       logging.ERROR)
            return False
    if isdir(path):
        dir_path = join(basket_path, basename(path))
        dir_path = check_in_basket(basket_path, dir_path)
        try:
            if (len(listdir(path)) != 0 and is_recursive#check correct flags
                    and not is_dir) or (len(listdir(path)) == 0 and is_dir):
                shutil.copytree(path, dir_path)
                basket_list.add(basename(path), path, basket_path,
                                dir_path, datetime.datetime.now())
            basket_list.save()
            logger.log("Moved directory {} to the basket".format(basename(path)),
                       logging.INFO)
            return True
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
