#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pickle
import os
from os.path import exists, basename
import datetime
import alirem.getsize as getsize


class object_in_basket(object):
    def __init__(self, name, rm_path, basket_path, index_in_basket, time):
        self.rm_path = rm_path
        self.basket_path = basket_path
        self.index_in_basket = index_in_basket
        self.name = name
        self.time = time

class BasketList(object):
    def __init__(self):
        self.list_of_objects_in_basket = []

    def search(self, name, basket_path):
        for obj in self.list_of_objects_in_basket:
            if (basename(obj.index_in_basket) == name) and (
                    os.path.abspath(obj.basket_path) == os.path.abspath(basket_path)):
                return obj
        return None

    def remove(self, el):
        self.list_of_objects_in_basket.remove(el)

    def add(self, name, rm_path, basket_path, index_in_basket, time):
        el = object_in_basket(name, rm_path, basket_path, index_in_basket, time)
        self.list_of_objects_in_basket.append(el)

    def load(self):
        if not os.path.exists('basket_list.pickle'):
            open('basket_list.pickle', 'wb')
        else:
            with open('basket_list.pickle', 'rb') as f:
                if os.path.getsize('basket_list.pickle') > 0:
                    self.list_of_objects_in_basket = pickle.load(f)
                else:
                    self.list_of_objects_in_basket = []
                tmp_arr = []
                for el in self.list_of_objects_in_basket:
                    if exists(el.index_in_basket) or os.path.islink(el.index_in_basket):
                        tmp_arr.append(el)
                self.list_of_objects_in_basket = tmp_arr
    def save(self):
        with open('basket_list.pickle', 'wb') as f:
            pickle.dump(self.list_of_objects_in_basket, f)

    def get_list_of_objects_in_basket(self):
        return self.list_of_objects_in_basket

    def show(self):
        if len(self.list_of_objects_in_basket) > 10:
            size = 0
            for el in self.list_of_objects_in_basket:
                size += getsize.get_size(el.index_in_basket)
            print 'TOTAL SIZE:'+ str(size)

        else:
            if self.list_of_objects_in_basket == []:
                print 'EMPTY'
            print '\n'

            for el in self.list_of_objects_in_basket:
                print 'NAME: '+el.name
                print 'RM_PATH: '+el.rm_path
                print 'BASKET: '+el.basket_path
                print 'NAME IN BASKET: '+el.index_in_basket
                print 'TIME: '+str(el.time)
                print 'TIME IN BASKET(seconds): '+str((datetime.datetime.now()-el.time).seconds)
                print 'SIZE: '+str(getsize.get_size(el.index_in_basket))
                print '====================================='

        print '\n'
