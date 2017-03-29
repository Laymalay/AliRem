import os
import shutil

class MyException(Exception):
    pass

class HandlerRemove(object):

    def __init__(self, is_dir, is_interactive, is_recursive, is_basket, basket_path):
        self.basket_path = basket_path
        self.is_dir = is_dir
        self.is_interactive = is_interactive
        self.is_recursive = is_recursive
        self.is_basket = is_basket


    def run(self, path):
        if self.is_basket:
            self.go_basket(path)
        self.remove(path)

    def go_basket(self, path):
        if not os.path.exists(self.basket_path):
            os.mkdir(self.basket_path)
        if os.path.isfile(path):
            file_path = os.path.join(self.basket_path, os.path.basename(path))
            shutil.copyfile(path, file_path)
        if os.path.isdir(path):
            dir_path = os.path.join(self.basket_path, os.path.basename(path))
            shutil.copytree(path, dir_path)
            print "a"

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
                if self.is_basket:
                    self.go_basket(path)
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
