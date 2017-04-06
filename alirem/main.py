#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import argparse
import logging
import alirem.logger as log
import alirem.remove as remover
import alirem.restore as restorer
import alirem.check_basket_for_cleaning as CheckBasketForCleaning
import alirem.exception as exception


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    parser.add_argument('--showparam', action='store_true')
    parser.add_argument('--dryrun', action='store_true', default=None)
    parser.add_argument('-i', '--interactive', action='store_true', default=None)
    parser.add_argument('--configfile', action='store', help='path to config file')
    parser.add_argument('--logfilepath', action='store',
                        help='path to logging file without file extension')
    parser.add_argument('--silent', action='store_true', default=None,
                        help='silent mode')
    parser.add_argument('--logmodecmd', action='store',
                        choices=['info', 'debug', 'warning', 'error'],
                        help='logging level for file')
    parser.add_argument('--logmodefile', action='store',
                        choices=['info', 'debug', 'warning', 'error'], default=None,
                        help='logging level for cmd')

    clearParser = subparsers.add_parser('basket')
    clearParser.add_argument('-m', '--clearmode', action='store', choices=['size', 'time'],
                             help='cleaning mode for basket')
    clearParser.add_argument('-t', '--deltatime', action='store', type=int,
                             help='file storage time in basket')
    clearParser.add_argument('-x', '--maxsize', action='store', type=int,
                             help='max size of basket')
    clearParser.add_argument('-p', '--basketpath', action='store',
                             help='path to basket')
    clearParser.add_argument('-s', '--show', action='store_true', default=None,
                             help='show the contents of the basket')

    removeParser = subparsers.add_parser('remove')
    removeParser.add_argument('removepath', nargs='+')
    removeParser.add_argument('-d', '--dir', action='store_true', help='is it dir')
    removeParser.add_argument('-r', '--recursive', action='store_true', help='is it not empty dir')
    removeParser.add_argument('-b', '--basket', action='store_true', default=None,
                              help='remove to basket')
    removeParser.add_argument('-p', '--basketpath', action='store', help='path to basket')
    removeParser.add_argument('-f', '--forceremove', action='store_true', default=None,
                              help='force remove')

    restoreParser = subparsers.add_parser('restore')
    restoreParser.add_argument('restorename', nargs='+')
    restoreParser.add_argument('-p', '--basketpath', action='store', help='path to basket')
    restoreParser.add_argument('-f', '--forcerestore', action='store_true', default=None,
                               help='force restore')
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


    if args.configfile is not None:
        with open(args.configfile) as config_file:
            config = json.load(config_file)
    else:
        config = None
    with open('config_file_default.json') as default_config_file:
        default_config = json.load(default_config_file)

    sync_params(vars(args), default_config, config)

    if args.showparam:
        show_params(default_config)

    logger = log.Logger(default_config['logmodefile'], default_config['logmodecmd'],
                        default_config['logfilepath'], default_config['silent'])
    try:
        if args.command == "basket":
            check_basket = CheckBasketForCleaning.CheckBasketHandler(logger,
                                                                     default_config['show'],
                                                                     default_config['basketpath'],
                                                                     default_config['clearmode'],
                                                                     default_config['deltatime'],
                                                                     default_config['maxsize'])
            check_basket.check_basket_for_cleaning()
        elif args.command == "remove":
            remove_handler = remover.RemoveHandler(args.dir, args.recursive,
                                                   default_config['interactive'],
                                                   default_config['dryrun'],
                                                   default_config['basket'],
                                                   logger,
                                                   default_config['forceremove'],
                                                   default_config['basketpath'])

            for remove_path in args.removepath:
                remove_handler.run_remove(remove_path)


        elif args.command == "restore":
            for restore_name in args.restorename:
                restorer.restore(restore_name, default_config['basketpath'],
                                 default_config['forcerestore'], logger)
        else:
            logger.log("Invalid operation", logging.ERROR, exception.InvalidOperation)

    except exception.Error as error:
        print error.exit_code
        exit(error.exit_code)

def show_params(default_config):
    for key, value in default_config.iteritems():
        print key+':'+str(value)

if __name__ == '__main__':
    alirem()

