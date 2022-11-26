import os


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
