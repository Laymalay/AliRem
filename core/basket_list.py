import pickle
import os
class element(object):
    def __init__(self, name, rm_path, basket_path, index_in_basket, time):
        self.rm_path = rm_path
        self.basket_path = basket_path
        self.index_in_basket = index_in_basket
        self.name = name
        self.time = time

class Basket_list(object):
    def __init__(self):
        self.array = []
    def search(self, name, basket_path):
        for el in self.array:
            if (os.path.basename(el.index_in_basket) == name) and (
                    el.basket_path == os.path.basename(basket_path)):
                return el
        return None

    def remove(self, el):
        self.array.remove(el)
    def add(self, name, rm_path, basket_path, index_in_basket, time):
        el = element(name, rm_path, basket_path, index_in_basket, time)
        self.array.append(el)
    def load(self):
        with open('basket_list.pickle', 'rb') as f:
            if os.path.getsize('basket_list.pickle') > 0:
                self.array = pickle.load(f)
            else:
                self.array = []
    def save(self):
        with open('basket_list.pickle', 'wb') as f:
            pickle.dump(self.array, f)
    def show(self):
        if self.array == []:
            print 'EMPTY'
        print '\n'
        for el in self.array:

            print 'NAME: '+el.name
            print 'RM_PATH: '+el.rm_path
            print 'BASKET: '+el.basket_path
            print 'NAME IN BASKET: '+el.index_in_basket
            print 'TIME: '+str(el.time)
            print '====================================='
        print '\n'
