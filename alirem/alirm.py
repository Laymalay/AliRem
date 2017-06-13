# !/usr/bin/python
# -*- coding: UTF-8
import os.path
import alirem.remove as RemoveHandler
import alirem.restore as restore
import alirem.basket_cleaner as BasketCleaner
from alirem.logger import DefaultLogger
from alirem.basket_handler import create_basket

DEFAULT_TIME = 'PT1H'
DEFAULT_MAXSIZE = 100000000

class Alirem(object):
    """
        Alirem is a utility for deleting files, directories and links.
        Also user can delete file objects to basket and then restore them.
        Keyword Arguments:
        -logger -- logger to log all actions
    """
    def __init__(self, logger=None):
        if logger is None:
            self.logger = DefaultLogger()
        else:
            self.logger = logger

    def remove(self, path, is_dir=False,
               is_recursive=False, is_interactive=False, is_dryrun=False,
               is_basket=True, basket_path='basket', regexp=None,
               symlinks=False, is_progress=True):

        """
        Delete objects
            is_dir -- objects is directory
            is_recursive -- objects is not empty directory
            is_interactive -- interactive mode
            is_dryrun -- dryrun mode
            is_basket -- move to basket
            basket_path -- path to basket
            regexp -- regexp to delete objects in file tree
            symlinks -- go to symlinks
            is_progress -- show progress
        """
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
        """ Restore object
        - restorename -- name of object
        - basket_path -- path to basket
        - is_merge -- merge directories
        - is_replace -- replace directories
        - is_progress -- show progress
        """
        return restore.restore(name=restorename, basket_path=basket_path,
                               logger=self.logger, is_merge=is_merge,
                               is_replace=is_replace, is_progress=is_progress)

    def check_basket_for_cleaning(self, is_show=False, mode='time', basket_path='basket',
                                  time=DEFAULT_TIME, size=DEFAULT_MAXSIZE):
        """Clean basket
         - is_show --show basket
         - mode -- mode for cleaning
         - basket_path -- path to basket
         - time --deltatime
         - size -- max size of basket
        """
        basket_handler = BasketCleaner.CheckBasketHandler(self.logger,
                                                          is_show=is_show,
                                                          basket_path=basket_path,
                                                          mode=mode,
                                                          time=time,
                                                          size=size)
        basket_handler.check_basket_for_cleaning()
        return basket_path,time,mode,size

    def get_basket_list(self, basket_path):
        """Return array of objects in basket"""
        basket_handler = BasketCleaner.CheckBasketHandler(basket_path=basket_path,
                                                          logger=self.logger)
        return basket_handler.get_objects_in_basket()

    def create_basket(self, basket_path):
        """Create new basket"""
        if not os.path.exists(os.path.abspath(basket_path)):
            create_basket(basket_path=os.path.abspath(basket_path), logger=self.logger)
            return True
        else:
            return False

    def show_basket_list(self, basket_path):
        """Show objects in basket"""
        print basket_path
        basket_handler = BasketCleaner.CheckBasketHandler(self.logger, basket_path)
        basket_handler.show_basket()
