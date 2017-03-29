#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
import core.basket_list as b_list
def go_basket(basket_path, path):
    bs = b_list.Basket_list()
    bs.load()
    if not os.path.exists(basket_path):
        os.mkdir(basket_path)
    if os.path.isfile(path):
        file_path = os.path.join(basket_path, os.path.basename(path))
        file_path = check_in_basket(basket_path, file_path)
        shutil.copyfile(path, file_path)
        bs.add(os.path.basename(path), path, basket_path, file_path)
        bs.save()
    if os.path.isdir(path):
        dir_path = os.path.join(basket_path, os.path.basename(path))
        dir_path = check_in_basket(basket_path, dir_path)
        shutil.copytree(path, dir_path)
        bs.add(os.path.basename(path), path, basket_path, dir_path)
        bs.save()



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