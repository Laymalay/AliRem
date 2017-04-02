#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import join, isfile, getsize, isdir


def get_dir_size(directory):
    total_size = 0
    for item in listdir(directory):
        itempath = join(directory, item)
        if isfile(itempath):
            total_size += getsize(itempath)
        elif isdir(itempath):
            total_size += get_dir_size(itempath)
    return total_size

def get_size(path):

    size = 0
    if isfile(path):
        return getsize(path)
    else:
        for obj in listdir(path):
            if isfile(join(path, obj)):
                size += getsize(join(path, obj))
            else:
                size += get_dir_size(join(path, obj))
        return size
