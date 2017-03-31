#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import logging
import shutil
import core.basket_list as b_list


def restore(name, basket_path, is_force, logger):

    bs = b_list.BasketList()
    bs.load()
    for name_el in name:
        index_name = os.path.join(basket_path, name_el)
        element = bs.search(name_el, basket_path)
        if element is not None:
            dst = element.rm_path
            #name = new_file.name
            if os.path.isfile(index_name):
                if not os.path.exists(dst):#if not such file
                    shutil.copyfile(index_name, dst)
                    os.remove(index_name)
                    bs.remove(element)
                    logger.log("File {} restored".format(os.path.basename(dst)), logging.INFO)
                elif not is_force:#if file exists and force=False
                    logger.log("""File {} can not be restored. File with
                                  the same name already exists""".format(os.path.basename(dst)),
                               logging.WARNING)

                else:
                    if os.path.isfile(dst):
                        os.remove(dst)
                        logger.log("""Old file was replaced by restored
                                      file {}""".format(os.path.basename(dst)),
                                   logging.INFO)

                    else:
                        shutil.rmtree(dst)
                        logger.log("""Old directory was replaced by restored
                                      file {}""".format(os.path.basename(dst)),
                                   logging.INFO)
                    shutil.copyfile(index_name, dst)
                    os.remove(index_name)
                    bs.remove(element)
            if os.path.isdir(index_name):
                if not os.path.exists(dst):
                    shutil.copytree(index_name, dst)
                    shutil.rmtree(index_name)
                    bs.remove(element)
                    logger.log("Directory {} restored".format(os.path.basename(dst)), logging.INFO)
                elif not is_force:#if file exists and force=False
                    logger.log("""Directory {} can not be restored. Directory or file with
                                  the same name already exists""".format(os.path.basename(dst)),
                               logging.WARNING)

                else:
                    if os.path.isfile(dst):
                        os.remove(dst)
                        logger.log("""Old file was replaced by restored
                                      directory {}""".format(os.path.basename(dst)),
                                   logging.INFO)
                    else:
                        shutil.rmtree(dst)#delete file if exist the same name
                        logger.log("""Old directory was replaced by restored
                                      directory {}""".format(os.path.basename(dst)),
                                   logging.INFO)
                    shutil.copytree(index_name, dst)
                    shutil.rmtree(index_name)
                    bs.remove(element)
        else:
            logger.log("Cannot find such file {} in basket".format(name), logging.WARNING)
            bs.save()
