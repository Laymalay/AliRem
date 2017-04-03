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

    parser.add_argument('--configfile', action='store')
    parser.add_argument('--logfilepath', action='store')
    parser.add_argument('--silent', action='store_true', default=None)
    parser.add_argument('--logmodecmd', action='store',
                        choices=['info', 'debug', 'warning', 'error'])
    parser.add_argument('--logmodefile', action='store',
                        choices=['info', 'debug', 'warning', 'error'], default=None)

    clearParser = subparsers.add_parser('clear')
    clearParser.add_argument('-m', '--clearmode', action='store', choices=['size', 'time'])
    clearParser.add_argument('-t', '--deltatime', action='store', type=int)
    clearParser.add_argument('-s', '--maxsize', action='store', type=int)
    clearParser.add_argument('-p', '--basketpath', action='store')
    clearParser.add_argument('-l', '--show', action='store_true', default=None)

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('removepath', nargs='+')
    removeParser.add_argument('-d', '--dir', action='store_true')
    removeParser.add_argument('-r', '--recursive', action='store_true')
    removeParser.add_argument('-b', '--basket', action='store_true', default=None)
    removeParser.add_argument('-p', '--basketpath', action='store')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('restorename', nargs='+')
    restoreParser.add_argument('-p', '--basketpath', action='store')
    restoreParser.add_argument('-f', '--force', action='store_true', default=None)
    namespace = parser.parse_args() #(sys.args[1:])
    return namespace

def sync_params(cmd, default_config, config=None):
    if config is not None:
        #Overlap default_config by config
        for key, value in default_config.iteritems():
            if value != config.get(key) and config.get(key) is not None:
                default_config[key] = config.get(key)
    for key, value in default_config.iteritems():
        if value != cmd.get(key) and cmd.get(key) is not None:
            default_config[key] = cmd.get(key)

def alirem():

    args = createParser()
    config = None
    if args.configfile is not None:
        with open(args.configfile) as config_file:
            config = json.load(config_file)

    with open('config_file_default.json') as default_config_file:
        default_config = json.load(default_config_file)

    sync_params(vars(args), default_config, config)

    for key, value in default_config.iteritems():
        print key+':'+str(value)

    logger = log.Logger(default_config['logmodefile'], default_config['logmodecmd'],
                        default_config['logfilepath'], default_config['silent'])

    if args.command == "clear":
        check_basket = CheckBasketForCleaning.CheckBasketHandler(logger,
                                                                 default_config['show'],
                                                                 default_config['basketpath'],
                                                                 default_config['clearmode'],
                                                                 default_config['deltatime'],
                                                                 default_config['maxsize'])
        check_basket.check_basket_for_cleaning()
    elif args.command == "remove":
        remove_handler = remover.RemoveHandler(args.dir, args.recursive,
                                               default_config['basket'],
                                               default_config['basketpath'], logger)
        try:
            for remove_path in args.removepath:
                remove_handler.run_remove(remove_path)
        except remover.MyException:
            logger.log("MyException", logging.ERROR)

    elif args.command == "restore":
        for restore_name in args.restorename:
            restorer.restore(restore_name, default_config['basketpath'],
                             default_config['force'], logger)
    else:
        logger.log("Invalid operation", logging.ERROR)

if __name__ == '__main__':
    alirem()
