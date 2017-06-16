#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pickle
import os
from os.path import exists, basename
import datetime
import alirem.getsize as getsize
import threading
class object_in_basket(object):
    def __init__(self, name, rm_path, basket_path, index_in_basket, time):
        self.rm_path = rm_path
        self.basket_path = basket_path
        self.index_in_basket = index_in_basket
        self.name = name
        self.time = time

class BasketList(object):
    def __init__(self, basket_path='basket'):#  basket_path='basket'
        self.list_of_objects_in_basket = []
        self.basket_list_path = os.path.join(basket_path, 'basket_list.pickle')
        self.lock = threading.Lock()

    def search(self, name, basket_path):
        for obj in self.list_of_objects_in_basket:
            if (basename(obj.index_in_basket) == name) and (
                    os.path.abspath(obj.basket_path) == os.path.abspath(obj.basket_path)):
                return obj
        return None

    def remove(self, el):
        self.list_of_objects_in_basket.remove(el)

    def add(self, name, rm_path, basket_path, index_in_basket, time):
        el = object_in_basket(name, rm_path, basket_path, index_in_basket, time)
        self.list_of_objects_in_basket.append(el)

    def load(self):
        have_it = False
        while not have_it:
            have_it = self.lock.acquire(False)
            try:
                if have_it:
                    if not os.path.exists(self.basket_list_path):
                        open(self.basket_list_path, 'wb')
                    else:
                        with open(self.basket_list_path, 'rb') as f:
                            if os.path.getsize(self.basket_list_path) > 0:
                                self.list_of_objects_in_basket = pickle.load(f)
                            else:
                                self.list_of_objects_in_basket = []
                            tmp_arr = []
                            for el in self.list_of_objects_in_basket:
                                if exists(el.index_in_basket) or os.path.islink(el.index_in_basket):
                                    tmp_arr.append(el)
                            self.list_of_objects_in_basket = tmp_arr
            finally:
                if have_it:
                    self.lock.release()

    def save(self):
        have_it = False
        while not have_it:
            have_it = self.lock.acquire(False)
            try:
                if have_it:
                    with open(self.basket_list_path, 'wb') as f:
                        pickle.dump(self.list_of_objects_in_basket, f)
            finally:
                if have_it:
                    self.lock.release()

    def get_list_of_objects_in_basket(self):
        return self.list_of_objects_in_basket

    def show(self):
        if len(self.list_of_objects_in_basket) > 100:
            size = 0
            for el in self.list_of_objects_in_basket:
                if getsize.get_size(el.index_in_basket) is not None:
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
                print 'TIME IN BASKET: '+str((datetime.datetime.now()-el.time))
                if getsize.get_size(el.index_in_basket) is not None:
                    print 'SIZE: '+str(getsize.get_size(el.index_in_basket))
                print '====================================='

        print '\n'
