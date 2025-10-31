import os
from src.logger import log_error
from src.exceptions import ShellError

def cat(filename):
    try:
        if os.path.isdir(filename):
            raise ShellError("Ошибка. Это директория, а не файл.")
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(e)
        log_error(str(e))



