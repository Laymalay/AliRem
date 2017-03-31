#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
import logging
import datetime


import core.basket_list as b_list
def go_basket(basket_path, path, is_dir, is_recursive, logger):
    bs = b_list.Basket_list()
    bs.load()
    if not os.path.exists(basket_path):
        os.mkdir(basket_path)
        logger.log("Basket was created", logging.INFO)
    if os.path.isfile(path):
        file_path = os.path.join(basket_path, os.path.basename(path))
        file_path = check_in_basket(basket_path, file_path)
        shutil.copyfile(path, file_path)
        bs.add(os.path.basename(path), path, basket_path, file_path, datetime.datetime.now())
        bs.save()
        logger.log("Moved file {} to the basket".format(os.path.basename(path)), logging.INFO)
    if os.path.isdir(path):
        dir_path = os.path.join(basket_path, os.path.basename(path))
        dir_path = check_in_basket(basket_path, dir_path)
        if (len(os.listdir(path)) != 0 and is_recursive
                and not is_dir) or (len(os.listdir(path)) == 0 and is_dir):
            shutil.copytree(path, dir_path)
            bs.add(os.path.basename(path), path, basket_path, dir_path, datetime.datetime.now())
        bs.save()
        logger.log("Moved directory {} to the basket".format(os.path.basename(path)), logging.INFO)



def check_in_basket(basket_path, path):
    path_check = os.path.join(basket_path, os.path.basename(path))
    if os.path.exists(path_check):
        index = 1
        while True:
            if not os.path.exists(path_check+'({})'.format(index)):
                break
            index += 1
        new_name = path+'({})'.format(index)
    else:
        new_name = path

    return new_name
