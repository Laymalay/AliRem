import os
import logging
import shutil
import datetime
import core.basket_list as b_list
import core.getsize as getsize

class CheckBasket(object):

    def __init__(self, logger, is_show, basket_path, mode, time, size):
        self.logger = logger
        self.is_show = is_show
        self.basket_path = basket_path
        self.mode = mode
        self.time = time
        self.size = size

    def check_basket(self):
        basket_list = b_list.Basket_list()
        basket_list.load()
        if self.is_show:
            print 'BEFORE:'
            basket_list.show()
        if os.path.exists(self.basket_path):
            if self.mode == 'size':
                if getsize.get_size(self.basket_path) >= int(self.size):
                    for obj in os.listdir(self.basket_path):
                        if os.path.isfile(os.path.join(self.basket_path, obj)):
                            os.remove(os.path.join(self.basket_path, obj))
                            basket_list.remove(basket_list.search(obj, self.basket_path))
                        else:
                            shutil.rmtree(os.path.join(self.basket_path, obj))
                            basket_list.remove(basket_list.search(obj, self.basket_path))
            elif self.mode == 'time':
                for obj in os.listdir(self.basket_path):
                    if os.path.isfile(os.path.join(self.basket_path, obj)):
                        self.check_file(os.path.join(self.basket_path, obj), self.time,
                                        basket_list, self.basket_path)
                    else:
                        self.check_dir(os.path.join(self.basket_path, obj), self.time,
                                       basket_list, self.basket_path)
        else:
            self.logger.log("Basket doesn't exist", logging.ERROR)
        basket_list.save()
        if self.is_show:
            print 'AFTER: '
            basket_list.show()

    def check_file(self, path, time, basket_list, basket_path):
        file_time = basket_list.search(os.path.basename(path), os.path.dirname(path)).time
        if (datetime.datetime.now()-file_time).seconds >= int(time):
            os.remove(path)
            self.logger.log("Remove file {}".format(os.path.basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(os.path.basename(path), basket_path))
    def check_dir(self, path, time, basket_list, basket_path):
        dir_time = basket_list.search(os.path.basename(path), os.path.dirname(path)).time
        if (datetime.datetime.now()-dir_time).seconds >= int(time):
            shutil.rmtree(path)
            self.logger.log("Remove dir {}".format(os.path.basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(os.path.basename(path), basket_path))
