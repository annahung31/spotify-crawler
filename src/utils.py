

import os

def check_exist(dirnames):
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)

