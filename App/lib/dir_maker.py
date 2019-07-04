import errno
import os
from datetime import datetime

def create_dir_with_uid(path, uid):
    mydir = os.path.join(
        path,
        uid +"-"+ datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    print(mydir)
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # This was not a "directory exist" error..
    return mydir
