#!/usr/bin/python
# -*- coding: UTF-8
import alirem.remove as RemoveHandler
import alirem.restore as restore
import alirem.check_basket_for_cleaning as BasketHandler
import alirem.logger as logger
class Alirem(object):
    def __init__(self, basket_path='basket',
                 mode='size',
                 time=120, size=1000,
                 mode_for_file='info', mode_for_cmd='info',
                 path_log='example', is_silent=False):

        self.basket_path = basket_path
        self.mode = mode
        self.time = time
        self.size = size
        self.logger = logger.Logger(mode_for_file, mode_for_cmd, path_log, is_silent)

    def remove(self, remove_path, is_dir=False, is_recursive=False, is_basket=True):
        remove_handler = RemoveHandler.RemoveHandler(is_dir,
                                                     is_recursive,
                                                     is_basket,
                                                     self.basket_path,
                                                     self.logger)
        remove_handler.run_remove(remove_path)

    def restore(self, name, is_force=True):
        restore.restore(name, self.basket_path, is_force, self.logger)

    def check_basket_for_cleaning(self, is_show):
        basket_handler = BasketHandler.CheckBasketHandler(self.logger,
                                                          is_show,
                                                          self.basket_path,
                                                          self.mode,
                                                          self.time,
                                                          self.size)
        basket_handler.check_basket_for_cleaning()

