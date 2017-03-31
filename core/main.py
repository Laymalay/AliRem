#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import argparse
import core.logger as log
import core.remove as ar
import core.restore as rs
import core.check_basket as CheckBasket


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser.add_argument('--configfile', action='store', default='config_file.json')
    parser.add_argument('-c', '--logmode_cmd', action='store')
    parser.add_argument('-f', '--logmode_file', action='store')
    parser.add_argument('-p', '--log_file_path', action='store')

    clearParser = subparsers.add_parser('clear')
    clearParser.add_argument('-m', '--clearmode', action='store')
    clearParser.add_argument('-t', '--deltatime', action='store', type=int)
    clearParser.add_argument('-s', '--size', action='store', type=int)
    clearParser.add_argument('-p', '--basket_path', action='store')
    clearParser.add_argument('-l', '--show', action='store_true')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('path', nargs='+')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')
    removeParser.add_argument('-b', '--basket', action='store_true')
    removeParser.add_argument('-p', '--basket_path', action='store')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('name', nargs='+')
    restoreParser.add_argument('-p', '--basket_path', action='store')
    restoreParser.add_argument('-f', '--force', action='store_true')
    namespace = parser.parse_args() #(sys.args[1:])
    return namespace

def activate_mode(config, cmd):
    for k, v in cmd.iteritems():
        if v is None:
            cmd[k] = config.get(k)
        if v is False:
            cmd[k] = config.get(k)
def alirem():

    args = createParser()
    with open(args.configfile) as config_file:
        config = json.load(config_file)

    activate_mode(config, vars(args))
    logger = log.Logger(args.logmode_file, args.logmode_cmd, args.log_file_path)

    if args.command == "clear":
        check_basket = CheckBasket.CheckBasket(logger, args.show, args.basket_path, args.clearmode,
                                               args.deltatime, args.size)
        check_basket.check_basket()
    elif args.command == "remove":
        handler = ar.HandlerRemove(args.dir, args.recursive,
                                   args.basket, args.basket_path, logger)
        try:
            handler.run(args.path)
        except ar.MyException:
            print("ouuups")
    elif args.command == "restore":
        rs.restore(args.name, args.basket_path, args.force, logger)
    else:
        print("invalid operation")

if __name__ == '__main__':
    alirem()
