#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import toml


def get_defaultconfig_json():
    return  '''
{
    "clearmode":"size",
    "deltatime": 120,
    "maxsize":100,
    "basketpath":"basket",
    "basket":false,
    "force":false,
    "logmodecmd":"INFO",
    "logmodefile":null,
    "logfilepath":"alirem",
    "silent":false,
    "show":true,
    "dryrun":false,
    "interactive":false,
    "merge":false,
    "replace":false,
    "symlinks":false,
    "progress":false
}
'''
def get_defaultconfig_toml():
    return '''
    clearmode="size"
    deltatime= 120
    maxsize=100
    basketpath="basket"
    basket=false
    force=false
    logmodecmd="INFO"
    logfilepath="alirem"
    silent=false
    show=true
    dryrun=false
    interactive=false
    merge=false
    replace=false
    symlinks=false
    progress=false
    '''
def load_defaultconfig_file_json(path):
    if not os.path.exists(path):
        with open(path, "w") as config_file:
            config_file.write(get_defaultconfig_json())
    with open(path) as config_file:
        return json.load(config_file)

def load_defaultconfig_file_toml(path):
    if not os.path.exists(path):
        with open(path, "w") as config_file:
            config_file.write(get_defaultconfig_toml())
    with open(path) as config_file:
        return toml.load(config_file)

def load_config_file_json(path):
    if path is not None:
        with open(path) as config:
            return json.load(config)
    else:
        return None

def load_config_file_toml(path):
    if path is not None:
        with open(path) as config:
            return toml.load(config)
    else:
        return None
