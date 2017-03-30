import os
import shutil
import datetime
import core.basket_list as b_list
import core.getsize as getsize

def check_basket(is_show, basket_path, mode, time, size):
    basket_list = b_list.Basket_list()
    basket_list.load()
    if is_show:
        print 'BEFORE:'
        basket_list.show()
    if os.path.exists(basket_path):
        if mode == 'size':
            if getsize.get_size(basket_path) >= int(size):
                for obj in os.listdir(basket_path):
                    if os.path.isfile(os.path.join(basket_path, obj)):
                        os.remove(os.path.join(basket_path, obj))
                        basket_list.remove(basket_list.search(obj, basket_path))
                    else:
                        shutil.rmtree(os.path.join(basket_path, obj))
                        basket_list.remove(basket_list.search(obj, basket_path))
        elif mode == 'time':
            for obj in os.listdir(basket_path):
                if os.path.isfile(os.path.join(basket_path, obj)):
                    check_file(os.path.join(basket_path, obj), time, basket_list, basket_path)
                else:
                    check_dir(os.path.join(basket_path, obj), time, basket_list, basket_path)
    basket_list.save()
    if is_show:
        print 'AFTER: '
        basket_list.show()

def check_file(path, time, basket_list, basket_path):
    file_time = basket_list.search(os.path.basename(path), os.path.dirname(path)).time
    if (datetime.datetime.now()-file_time).seconds >= int(time):
        os.remove(path)
        basket_list.remove(basket_list.search(os.path.basename(path), basket_path))
def check_dir(path, time, basket_list, basket_path):
    dir_time = basket_list.search(os.path.basename(path), os.path.dirname(path)).time
    if (datetime.datetime.now()-dir_time).seconds >= int(time):
        shutil.rmtree(path)
        basket_list.remove(basket_list.search(os.path.basename(path), basket_path))
