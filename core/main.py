#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import core.remove as ar
import core.restore as rs
import core.check_basket as check_basket


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    clearParser = subparsers.add_parser('clear')
    clearParser.add_argument('-m', '--clearmode', action='store', default='time')
    clearParser.add_argument('-t', '--deltatime', action='store', default='120')
    clearParser.add_argument('-s', '--size', action='store', default='0')
    clearParser.add_argument('-p', '--basket_path', action='store', default='basket')
    clearParser.add_argument('-l', '--show', action='store_true')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('path', nargs='+')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')
    removeParser.add_argument('-b', '--basket', action='store_true')
    removeParser.add_argument('-p', '--basket_path', action='store', default='basket')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('name', nargs='+')
    restoreParser.add_argument('-p', '--basket_path', action='store', default='basket')
    restoreParser.add_argument('-f', '--force', action='store_true')
    namespace = parser.parse_args() #(sys.args[1:])

    return namespace


def alirem():
    args = createParser()
    if args.command == "clear":
        check_basket.check_basket(args.show, args.basket_path, args.clearmode,
                                  args.deltatime, args.size)
    elif args.command == "remove":
        handler = ar.HandlerRemove(args.dir, args.recursive,
                                   args.basket, args.basket_path)
        try:
            handler.run(args.path)
        except ar.MyException:
            print("ouuups")
    elif args.command == "restore":
        rs.restore(args.name, args.basket_path, args.force)
    else:
        print("invalid operation")

if __name__ == '__main__':
    alirem()
