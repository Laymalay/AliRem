#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import core.remove as ar


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('path')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')
    removeParser.add_argument('-i', '--interactive', action='store_true')
    removeParser.add_argument('-b', '--basket', action='store_true')
    removeParser.add_argument('-p', '--basket_path', action='store', default='basket')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('path')

    namespace = parser.parse_args() #(sys.args[1:])

    return namespace


def alirem():
    args = createParser()
    handler = ar.HandlerRemove(args.dir, args.interactive, args.recursive,
                               args.basket, args.basket_path)
    if args.command == "remove":
        try:
            handler.run(args.path)
        except ar.MyException:
            print("ouuups")
    else:
        print("invalid operation")


if __name__ == '__main__':
    alirem()
    