import os
from src.logger import log_error
from src.exceptions import ShellError

def cat(filename):
    '''
    Выводит содержимое файла в консоль

    Args:
        filename(str)
    Returns:
        None
    Raises:
        ShellError
        FileNotFoundError
        Exceptions
    '''
    try:
        if os.path.isdir(filename):
            raise ShellError("Ошибка. Это директория, а не файл.")
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(e)
        log_error(str(e))
