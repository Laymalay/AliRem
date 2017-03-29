import os
import shutil
import core.basket_list as b_list


def restore(name, basket_path):

    bs = b_list.Basket_list()
    bs.load()#!!!!!!!!!!!
    for name_el in name:
        index_name = os.path.join(basket_path, name_el)
        element = bs.search(name_el, basket_path)
        if element is not None:
            dst = element.rm_path
            #name = new_file.name
            if os.path.isfile(index_name):
                shutil.copyfile(index_name, dst)
                os.remove(index_name)
            if os.path.isdir(index_name):
                shutil.copytree(index_name, dst)
                shutil.rmtree(index_name)
            bs.remove(element)
            bs.save()
