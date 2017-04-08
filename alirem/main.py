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

def create_remove_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--showparam', action='store_true')
    parser.add_argument('--dryrun', action='store_true', default=None)
    parser.add_argument('-i', '--interactive', action='store_true', default=None)
    parser.add_argument('-f', '--force', action='store_true', default=None)
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
    parser.add_argument('removepath', nargs='+')
    parser.add_argument('-d', '--dir', action='store_true', help='is it dir')
    parser.add_argument('-r', '--recursive', action='store_true', help='is it not empty dir')
    parser.add_argument('-b', '--basket', action='store_true', default=None,
                        help='remove to basket')
    parser.add_argument('-p', '--basketpath', action='store', help='path to basket')
    parser.add_argument('--regexp', action='store', help='regexp for searching in file-tree')
    namespace = parser.parse_args()
    return namespace

def create_restore_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--showparam', action='store_true')
    parser.add_argument('--dryrun', action='store_true', default=None)
    parser.add_argument('-i', '--interactive', action='store_true', default=None)
    parser.add_argument('-f', '--force', action='store_true', default=None)
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
    parser.add_argument('restorename', nargs='+')
    parser.add_argument('-p', '--basketpath', action='store', help='path to basket')
    parser.add_argument('-m', '--merge', action='store_true', default=None,
                        help='merge directores')
    parser.add_argument('-r', '--replace', action='store_true', default=None,
                        help='replace existing files')
    namespace = parser.parse_args()
    return namespace


def create_basket_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--showparam', action='store_true')
    parser.add_argument('--dryrun', action='store_true', default=None)
    parser.add_argument('-i', '--interactive', action='store_true', default=None)
    parser.add_argument('-f', '--force', action='store_true', default=None)
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
    parser.add_argument('-m', '--clearmode', action='store', choices=['size', 'time'],
                             help='cleaning mode for basket')
    parser.add_argument('-t', '--deltatime', action='store', type=int,
                             help='file storage time in basket')
    parser.add_argument('-x', '--maxsize', action='store', type=int,
                             help='max size of basket')
    parser.add_argument('-p', '--basketpath', action='store',
                             help='path to basket')
    parser.add_argument('-s', '--show', action='store_true', default=None,
                             help='show the contents of the basket')
    namespace = parser.parse_args()
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




def remove():
    args = create_remove_parser()
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
                        default_config['logfilepath'], default_config['silent'],
                        default_config['force'])
    try:
        remove_handler = remover.RemoveHandler(is_dir=args.dir, is_recursive=args.recursive,
                                               is_interactive=default_config['interactive'],
                                               is_dryrun=default_config['dryrun'],
                                               is_basket=default_config['basket'],
                                               logger=logger,
                                               basket_path=default_config['basketpath'],
                                               regexp=args.regexp)
        for remove_path in args.removepath:
            remove_handler.run_remove(remove_path)
    except exception.Error as error:
        print error.exit_code
        exit(error.exit_code)

def restore():
    args = create_restore_parser()
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
                        default_config['logfilepath'], default_config['silent'],
                        default_config['force'])
    try:
        for restore_name in args.restorename:
            restorer.restore(restore_name,
                             basket_path=default_config['basketpath'],
                             logger=logger,
                             is_merge=default_config['merge'],
                             is_replace=default_config['replace'])
    except exception.Error as error:
        print error.exit_code
        exit(error.exit_code)

def basket():
    args = create_basket_parser()
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
                        default_config['logfilepath'], default_config['silent'],
                        default_config['force'])

    try:
        check_basket = CheckBasketForCleaning.CheckBasketHandler(logger,
                                                                 default_config['show'],
                                                                 default_config['basketpath'],
                                                                 default_config['clearmode'],
                                                                 default_config['deltatime'],
                                                                 default_config['maxsize'])
        check_basket.check_basket_for_cleaning()
    except exception.Error as error:
        print error.exit_code
        exit(error.exit_code)


def show_params(default_config):
    for key, value in default_config.iteritems():
        print key+':'+str(value)

if __name__ == '__main__':
    remove()
    restore()
    basket()
