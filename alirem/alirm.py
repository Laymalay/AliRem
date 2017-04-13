# !/usr/bin/python
# -*- coding: UTF-8

import alirem.remove as RemoveHandler
import alirem.restore as restore
import alirem.basket_cleaner as BasketCleaner
from alirem.logger import DefaultLogger

DEFAULT_TIME = 300
DEFAULT_MAXSIZE = 100000000

class Alirem(object):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = DefaultLogger()
        else:
            self.logger = logger

    def remove(self, path, is_dir=False,
               is_recursive=False, is_interactive=False, is_dryrun=False,
               is_basket=False, basket_path='basket', regexp=None,
               symlinks=False, is_progress=True):

        remove_handler = RemoveHandler.RemoveHandler(is_dir=is_dir, is_recursive=is_recursive,
                                                     is_interactive=is_interactive,
                                                     is_dryrun=is_dryrun,
                                                     is_basket=is_basket,
                                                     logger=self.logger,
                                                     basket_path=basket_path,
                                                     regexp=regexp,
                                                     symlinks=symlinks,
                                                     is_progress=is_progress)


        remove_handler.remove(path)

    def restore(self, restorename, basket_path='basket',
                is_merge=False, is_replace=False, is_progress=True):
        restore.restore(name=restorename, basket_path=basket_path,
                        logger=self.logger, is_merge=is_merge,
                        is_replace=is_replace, is_progress=is_progress)

    def check_basket_for_cleaning(self, is_show=False, mode='time', basket_path='basket',
                                  time=DEFAULT_TIME, size=DEFAULT_MAXSIZE):

        basket_handler = BasketCleaner.CheckBasketHandler(self.logger,
                                                          is_show,
                                                          basket_path,
                                                          mode,
                                                          time,
                                                          size)

        basket_handler.check_basket_for_cleaning()

    def get_basket_list(self):
        basket_handler = BasketCleaner.CheckBasketHandler(self.logger)
        basket_handler.get_objects_in_basket()

    def show_basket_list(self):
        basket_handler = BasketCleaner.CheckBasketHandler(self.logger)
        basket_handler.show_basket()

