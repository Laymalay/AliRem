#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import argparse
import logging
import alirem.core.logger as log
import alirem.core.remove as remover
import alirem.core.restore as restorer
import alirem.core.check_basket_for_cleaning as CheckBasketForCleaning


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # TODO: Change path for log file, cause class logger will add .log or .json later + config file
    parser.add_argument('--configfile', action='store', default='config_file.json')
    parser.add_argument('-c', '--logmodecmd', action='store',
                        choices=['info', 'debug', 'warning', 'error'])
    parser.add_argument('-f', '--logmodefile', action='store',
                        choices=['info', 'debug', 'warning', 'error'])
    parser.add_argument('-p', '--logfilepath', action='store')
    parser.add_argument('--silent', action='store_true')

    clearParser = subparsers.add_parser('clear')
    clearParser.add_argument('-m', '--clearmode', action='store')
    clearParser.add_argument('-t', '--deltatime', action='store', type=int)
    clearParser.add_argument('-s', '--maxsize', action='store', type=int)
    clearParser.add_argument('-p', '--basketpath', action='store')
    clearParser.add_argument('-l', '--show', action='store_true')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('path', nargs='+')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')
    removeParser.add_argument('-b', '--basket', action='store_true')
    removeParser.add_argument('-p', '--basketpath', action='store')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('name', nargs='+')
    restoreParser.add_argument('-p', '--basketpath', action='store')
    restoreParser.add_argument('-f', '--force', action='store_true')
    namespace = parser.parse_args() #(sys.args[1:])
    return namespace

def activate_mode(config, cmd):
#TODO:swap congig and cmd and use later only congig[param] or config.get("param")
    for k, v in cmd.iteritems():
        if v is None:
            cmd[k] = config.get(k)
        if not v:
            cmd[k] = config.get(k)

def alirem():

    args = createParser()
    with open(args.configfile) as config_file:
        config = json.load(config_file)

    activate_mode(config, vars(args))
    logger = log.Logger(args.logmodefile, args.logmodecmd, args.logfilepath, args.silent)

    if args.command == "clear":
        check_basket_for_cleaning = CheckBasketForCleaning.CheckBasketHandler(logger, args.show,
                                                                              args.basketpath,
                                                                              args.clearmode,
                                                                              args.deltatime,
                                                                              args.maxsize)
        check_basket_for_cleaning.check_basket_for_cleaning()
    elif args.command == "remove":
        remove_handler = remover.RemoveHandler(args.dir, args.recursive,
                                               args.basket, args.basketpath, logger)
        try:
            for path in args.path:
                remove_handler.run_remove(path)
        except remover.MyException:
            logger.log("MyException", logging.ERROR)
    elif args.command == "restore":
        restorer.restore(args.name, args.basketpath, args.force, logger)
    else:
        logger.log("Invalid operation", logging.ERROR)

if __name__ == '__main__':
    alirem()
