import os
from src.logger import log_error

def cd(path):
    '''
    Изменяет текущую рабочую директорию
    Поддерживает специальные пути:
    - '~' - домашняя директория пользователя
    - '..' - родительская директория
    Args:
        path(str)
    Returns:
        None
    Raises:
        Exceptions
    '''
    try:
        if path == '~':
            path = os.path.expanduser('~')
        elif path == "..":
            path = os.path.dirname(os.getcwd())
        os.chdir(path)
    except Exception as e:
        print(e)
        log_error(str(e))
