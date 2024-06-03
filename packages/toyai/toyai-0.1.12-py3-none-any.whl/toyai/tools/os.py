import os


def mkdir(filename):
    dir = os.path.dirname(filename)
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    return f"{filename}"
