#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import os
import shutil

shutil.rmtree


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('path')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('path')

    namespace = parser.parse_args() #(sys.args[1:])

    return namespace
class MyException(Exception):
    pass
class HandlerRemove(object):
    def remove_dir(self, path):
        if not self.is_dir and not self.is_recursive:
            print("cannot remove '{}', it's dir".format(path))
        elif self.is_dir:
            if os.listdir(path) != 0:
                print("not empty")
            else:
                os.rmdir(path)
        elif self.is_recursive:
            b = True
            for obj in os.listdir(path):
                try:
                    self.run_remove(path + "/" + obj)
                except OSError:
                    b = False
                except MyException:
                    b = False

            if b:
                os.rmdir(path)
            else:
                raise MyException()

    def run_remove(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            self.remove_dir(path)

    def __init__(self, is_dir, is_interactive, is_recursive):
        self.is_dir = is_dir
        self.is_interactive = is_interactive
        self.is_recursive = is_recursive


    # def run_restore (namespace):
    #     print(os.path.isfile(namespace.remove))
    #     print(os.path.isdir(namespace.remove))

if __name__ == '__main__':
    args = createParser()



    handler = HandlerRemove(args.dir, False, args.recursive)
    if args.command == "remove":
        try:
            handler.run_remove(args.path)
        except MyException:
            print("ouuups")
    else:
        print("invalid operation")
