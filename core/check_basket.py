import os
import shutil
import datetime
import core.basket_list as b_list

def get_dir_size(directory):
    total_size = os.path.getsize(directory)
    for item in os.listdir(directory):
        itempath = os.path.join(directory, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_dir_size(itempath)
    return total_size

def get_size(basket_path):
    size = 0
    for obj in os.listdir(basket_path):
        if os.path.isfile(os.path.join(basket_path, obj)):
            size += os.path.getsize(os.path.join(basket_path, obj))
        else:
            size += get_dir_size(os.path.join(basket_path, obj))
    return size
def check_basket(is_show, basket_path, mode, time, size):
    basket_list = b_list.Basket_list()
    basket_list.load()
    if is_show:
        print 'BEFORE:'
        basket_list.show()
    if os.path.exists(basket_path):
        if mode == 'size':
            if get_size(basket_path) >= int(size):
                for obj in os.listdir(basket_path):
                    if os.path.isfile(os.path.join(basket_path, obj)):
                        os.remove(os.path.join(basket_path, obj))
                        basket_list.remove(basket_list.search(obj, basket_path))
                    else:
                        shutil.rmtree(os.path.join(basket_path, obj))
                        basket_list.remove(basket_list.search(obj, basket_path))
        elif mode == 'time':
            for obj in os.listdir(basket_path):
                if os.path.isfile(obj):
                    check_file(obj, time, basket_list, basket_path)
                else:
                    check_dir(obj, time, basket_list, basket_path)
    basket_list.save()
    if is_show:
        print 'AFTER: '
        basket_list.show()

def check_file(path, time, basket_list, basket_path):
    file_time = basket_list.search(path, os.path.dirname(path)).time
    if (datetime.datetime.now()-file_time).seconds >= time:
        os.remove(path)
        basket_list.remove(basket_list.search(path, basket_path))
def check_dir(path, time, basket_list, basket_path):
    dir_time = basket_list.search(path, os.path.dirname(path)).time
    if (datetime.datetime.now()-dir_time).seconds >= time:
        shutil.rmtree(path)
        basket_list.remove(basket_list.search(path, basket_path))
