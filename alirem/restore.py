#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os.path import join, exists, isfile, basename, isdir
from os import remove
import logging
import shutil
import alirem.basket_list as basketlist


def restore(name_el, basket_path, is_force, logger):

    basket_list = basketlist.BasketList()
    basket_list.load()
    index_name = join(basket_path, name_el)
    element = basket_list.search(name_el, basket_path)
    if element is not None:
        dst = element.rm_path
        #name = new_file.name

        if isfile(index_name):

            if not exists(dst):#if not such file
                shutil.copyfile(index_name, dst)
                remove(index_name)
                basket_list.remove(element)
                logger.log("File {} restored".format(basename(dst)), logging.INFO, 0)

            elif not is_force:#if file exists and force=False
                logger.log("""File {} can not be restored. File with
                                    the same name already exists""".format(basename(dst)),
                           logging.WARNING, 1)

            else:
                if isfile(dst):
                    remove(dst)
                    logger.log("""Old file was replaced by restored
                                        file {}""".format(basename(dst)),
                               logging.INFO, 0)

                else:
                    shutil.rmtree(dst)
                    logger.log("""Old directory was replaced by restored
                                        file {}""".format(basename(dst)),
                               logging.INFO, 0)
                shutil.copyfile(index_name, dst)
                remove(index_name)
                basket_list.remove(element)

        if isdir(index_name):

            if not exists(dst):
                shutil.copytree(index_name, dst)
                shutil.rmtree(index_name)
                basket_list.remove(element)
                logger.log("Directory {} restored".format(basename(dst)), logging.INFO, 0)

            elif not is_force:#if file exists and force=False
                logger.log("""Directory {} can not be restored. Directory or file with
                                the same name already exists""".format(basename(dst)),
                           logging.WARNING, 1)

            else:
                if isfile(dst):
                    remove(dst)
                    logger.log("""Old file was replaced by restored
                                    directory {}""".format(basename(dst)),
                               logging.INFO, 0)
                else:
                    shutil.rmtree(dst)#delete file if exist the same name
                    logger.log("""Old directory was replaced by restored
                                    directory {}""".format(basename(dst)),
                               logging.INFO, 0)
                shutil.copytree(index_name, dst)
                shutil.rmtree(index_name)
                basket_list.remove(element)
    else:
        logger.log("Cannot find such file {} in basket".format(name_el), logging.WARNING, 1)
        basket_list.save()
