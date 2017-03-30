import os
def get_dir_size(directory):
    total_size = os.path.getsize(directory)
    for item in os.listdir(directory):
        itempath = os.path.join(directory, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_dir_size(itempath)
    return total_size

def get_size(path):

    size = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    else:
        for obj in os.listdir(path):
            if os.path.isfile(os.path.join(path, obj)):
                size += os.path.getsize(os.path.join(path, obj))
            else:
                size += get_dir_size(os.path.join(path, obj))
        return size
