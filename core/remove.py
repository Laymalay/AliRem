import os

class MyException(Exception):
    pass

class HandlerRemove(object):
    def interact_remove(self, path):
        if os.path.isfile(path):
            im = raw_input('Do u want to remove this file named {} [Y/n]?'.format(path))
            if im is 'y':
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

    def run(self, path):
        if self.is_interactive:
            self.interact_remove(path)
        else:
            self.remove(path)

    def remove(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            self.remove_dir(path)

    def __init__(self, is_dir, is_interactive, is_recursive):
        self.is_dir = is_dir
        self.is_interactive = is_interactive
        self.is_recursive = is_recursive
# def remove_empty_dir(path):
#     if len(os.listdir(path)) != 0:
#         print("not empty")
#     else:
#         os.rmdir(path)

# def remove_dir(path):
#     b = True
#     if len(os.listdir(path)) == 0:
#         os.rmdir(path)
#     else:
#         for obj in os.listdir(path):
#             try:
#                 if os.path.isfile(path + "/" + obj):
#                     remove_file(path + "/" + obj)
#                 if os.path.isdir(path + "/" + obj):
#                     remove_dir(path + "/" + obj)
#             except OSError:
#                 b = False
#             except MyException:
#                 b = False
#         if b:
#             os.rmdir(path)
#         else:
#             raise MyException()

# def remove_file(path):
#     if os.path.isfile(path):
#         os.remove(path)
#     else:
#         print("cannot remove '{}', it's dirr".format(path))


