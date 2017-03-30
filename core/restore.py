import os
import shutil
import core.basket_list as b_list


def restore(name, basket_path, is_force):

    bs = b_list.Basket_list()
    bs.load()#!!!!!!!!!!!
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
                elif not is_force:#if file exists and force=False
                    print ('Such file={} already exists'.format(os.path.basename(dst)))
                    print ('If you want to replace this file use -f')
                else:
                    os.remove(dst)
                    shutil.copyfile(index_name, dst)
                    os.remove(index_name)
                    bs.remove(element)
            if os.path.isdir(index_name):
                if not os.path.exists(dst):
                    shutil.copytree(index_name, dst)
                    shutil.rmtree(index_name)
                    bs.remove(element)
                elif not is_force:#if file exists and force=False
                    print ('Such dir={} already exists'.format(os.path.basename(dst)))
                    print ('If you want to replace this directory use -f')
                else:
                    shutil.rmtree(dst)#delete file if exist the same name
                    shutil.copytree(index_name, dst)
                    shutil.rmtree(index_name)
                    bs.remove(element)

            bs.save()
