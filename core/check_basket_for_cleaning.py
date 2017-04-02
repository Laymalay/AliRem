from os.path import join, dirname, exists, isfile, basename
from os import listdir, remove
import logging
import shutil
import datetime
import alirem.core.basket_list as b_list
import alirem.core.getsize as getsize

class CheckBasketHandler(object):
    def __init__(self, logger, is_show, basket_path, mode, time, size):
        #TODO:add defaul value, if there is no such param in config & cmd
        self.logger = logger
        self.is_show = is_show
        self.basket_path = basket_path
        self.mode = mode
        self.time = time
        self.size = size

    def check_basket_for_cleaning(self):
        basket_list = b_list.BasketList()
        basket_list.load()
        if self.is_show:
            print 'BEFORE:'
            basket_list.show()

        if exists(self.basket_path):

            if self.mode == 'size':
                if getsize.get_size(self.basket_path) >= int(self.size):
                    for obj in listdir(self.basket_path):
                        if isfile(join(self.basket_path, obj)):
                            remove(join(self.basket_path, obj))
                            basket_list.remove(basket_list.search(obj, self.basket_path))
                        else:
                            shutil.rmtree(join(self.basket_path, obj))
                            basket_list.remove(basket_list.search(obj, self.basket_path))

            elif self.mode == 'time':
                for obj in listdir(self.basket_path):
                    if isfile(join(self.basket_path, obj)):
                        self.checking_file_for_deletion(join(self.basket_path, obj), self.time,
                                                        basket_list, self.basket_path)
                    else:
                        self.checking_dir_for_deletion(join(self.basket_path, obj), self.time,
                                                       basket_list, self.basket_path)

        else:
            self.logger.log("Basket doesn't exist", logging.ERROR)
        basket_list.save()
        if self.is_show:
            print 'AFTER: '
            basket_list.show()

    def checking_file_for_deletion(self, path, time, basket_list, basket_path):
        file_time = basket_list.search(basename(path), dirname(path)).time
        if (datetime.datetime.now()-file_time).seconds >= int(time):
            remove(path)
            self.logger.log("Remove file {}".format(basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(basename(path), basket_path))

    def checking_dir_for_deletion(self, path, time, basket_list, basket_path):
        dir_time = basket_list.search(basename(path), dirname(path)).time
        if (datetime.datetime.now()-dir_time).seconds >= int(time):
            shutil.rmtree(path)
            self.logger.log("Remove dir {}".format(basename(path)), logging.INFO)
            basket_list.remove(basket_list.search(basename(path), basket_path))
