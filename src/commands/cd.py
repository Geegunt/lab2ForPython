import os
from src.logger import log_error

def cd(path):
    try:
        if path == '~':
            path = os.path.expanduser('~')
        elif path == "..":
            path = os.path.dirname(os.getcwd())
        os.chdir(path)
    except Exception as e:
        print(e)
        log_error(str(e))



