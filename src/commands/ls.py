import os
import stat
from datetime import datetime
from src.logger import log_error
from src.exceptions import ShellError

def get_permissions(file_path):
    '''Получает права доступа в формате rwxrwxrwx
    Args:
        file_path(str)
    Returns:
        str
    '''
    st = os.stat(file_path)
    mode = st.st_mode
    permissions = []

    # Проверяем права для владельца (owner)
    permissions.append('r' if mode & stat.S_IRUSR else '-')
    permissions.append('w' if mode & stat.S_IWUSR else '-')
    permissions.append('x' if mode & stat.S_IXUSR else '-')

    # Проверяем права для группы (group)
    permissions.append('r' if mode & stat.S_IRGRP else '-')
    permissions.append('w' if mode & stat.S_IWGRP else '-')
    permissions.append('x' if mode & stat.S_IXGRP else '-')

    # Проверяем права для остальных (others)
    permissions.append('r' if mode & stat.S_IROTH else '-')
    permissions.append('w' if mode & stat.S_IWOTH else '-')
    permissions.append('x' if mode & stat.S_IXOTH else '-')

    return ''.join(permissions)

def ls(path='.', long_format=False):
    '''
    Выводит содержимое директории
    Показывает список файлов и папок в указанной директории. При обычном режиме
    скрывает файлы, начинающиеся с точки. В режиме -l показывает все файлы с
    подробной информацией: имя, размер, дата изменения, права доступа
    Args:
        path(str, optional)
        long_format(bool, optional)
    Returns:
        None
    Raises:
        ShellError
    '''
    try:
        if not os.path.exists(path):
            raise ShellError(f"ls: Невозможно получить доступ к '{path}': Такого файла или каталога нет")

        items = os.listdir(path)

        # Фильтруем скрытые файлы (начинающиеся с точки), если не long_format
        if not long_format:
            items = [item for item in items if not item.startswith('.')]

        items.sort()

        for item in items:
            full_path = os.path.join(path, item)
            if long_format:
                # Получаем информацию о файле
                file_stat = os.stat(full_path)
                size = file_stat.st_size if os.path.isfile(full_path) else "-"

                # Получаем дату изменения
                mtime = datetime.fromtimestamp(file_stat.st_mtime)
                date_str = mtime.strftime('%Y-%m-%d %H:%M:%S')

                # Получаем права доступа
                permissions = get_permissions(full_path)

                # Форматируем вывод: имя размер дата права_доступа
                print(f"{item:<20} {str(size):>10} {date_str} {permissions}")
            else:
                print(item, end='  ')
        if not long_format:
            print()
    except Exception as e:
        print(f"ls: невозможно открыть каталог: '{path}': {e}")
        log_error(f"ls: невозможно открыть каталог: '{path}': {e}")


def run(args):
    '''
    Обрабатывает аргументы и вызывает функцию
    Args:
         args(list)
    Returns:
        None
    '''
    long_format = False
    paths = []
    for arg in args:
        if arg == '-l':
            long_format = True
        elif arg.startswith('-'):
            print(f"ls: неверный вариант ввода -- '{arg}'")
            log_error(f"ls: неверный вариант ввода -- '{arg}'")
            return
        else:
            paths.append(arg)
    target = paths[0] if paths else '.'
    ls(target, long_format=long_format)
