from os.path import join, dirname, exists, isfile, basename
from os import listdir, remove
import logging
import shutil
import datetime
import alirem.basket_list as b_list
import alirem.getsize as getsize
import alirem.exception as exception
import isodate

class CheckBasketHandler(object):
    def __init__(self, logger, basket_path, is_show=True,
                 mode='size', time='PT1H', size=1000):
        self.logger = logger
        self.is_show = is_show
        self.basket_path = basket_path
        self.mode = mode
        self.time = time
        self.size = size
        self.basket_list = b_list.BasketList(basket_path)
        self.basket_list.load()

    def show_basket(self):
        if self.is_show:
            self.basket_list.show()

    def get_objects_in_basket(self):
        return self.basket_list.get_list_of_objects_in_basket()

    def check_basket_for_cleaning(self):
        self.show_basket()
        if exists(self.basket_path):

            if self.mode == 'size':
                if getsize.get_size(self.basket_path) >= int(self.size):
                    for obj in listdir(self.basket_path):
                        if isfile(join(self.basket_path, obj)):
                            remove(join(self.basket_path, obj))
                            self.basket_list.remove(self.basket_list.search(obj, self.basket_path))
                        else:
                            shutil.rmtree(join(self.basket_path, obj))
                            self.basket_list.remove(self.basket_list.search(obj, self.basket_path))

            elif self.mode == 'time':
                for obj in listdir(self.basket_path):
                    if obj != 'basket_list.pickle':
                        if isfile(join(self.basket_path, obj)):
                            self.checking_file_for_deletion(join(self.basket_path, obj), self.time,
                                                            self.basket_list, self.basket_path)
                        else:
                            self.checking_dir_for_deletion(join(self.basket_path, obj), self.time,
                                                            self.basket_list, self.basket_path)

        else:
            self.logger.log("Basket doesn't exist", logging.ERROR, exception.BasketDoesNotExists)
        self.basket_list.save()

    def checking_file_for_deletion(self, path, time, basket_list, basket_path):
        file_time = basket_list.search(basename(path), dirname(path)).time
        if (datetime.datetime.now()-file_time) >= isodate.parse_duration(time):
            remove(path)
            self.logger.log("Remove file {}".format(basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(basename(path), basket_path))
         
    def checking_dir_for_deletion(self, path, time, basket_list, basket_path):
        dir_time = basket_list.search(basename(path), dirname(path)).time
        if (datetime.datetime.now()-dir_time) >= isodate.parse_duration(time):
            shutil.rmtree(path)
            self.logger.log("Remove dir {}".format(basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(basename(path), basket_path))
