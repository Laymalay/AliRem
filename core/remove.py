#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import core.basket as b

class MyException(Exception):
    pass

class HandlerRemove(object):

    def __init__(self, is_dir, is_recursive, is_basket, basket_path):
        self.basket_path = basket_path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.is_basket = is_basket

    def run(self, path):
        for unit in path:
            if self.is_basket:
                b.go_basket(self.basket_path, unit)
            self.remove(unit)
    def remove(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            self.remove_dir(path)

    def remove_dir(self, path):
        if not self.is_dir and not self.is_recursive:
            print("cannot remove '{}', it's dir".format(path))
        elif self.is_dir:
            if len(os.listdir(path)) != 0:
                print("not empty")
            else:
                os.rmdir(path)
        elif self.is_recursive:
            b = True
            for obj in os.listdir(path):
                try:
                    self.remove(path + "/" + obj)
                except OSError:
                    b = False
                except MyException:
                    b = False
            if b:
                os.rmdir(path)
            else:
                raise MyException()
