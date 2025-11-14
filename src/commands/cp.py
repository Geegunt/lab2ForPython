import os
import shutil
from src.logger import log_error

def cp(src, dst):
    '''
    Копирует файл или директорию

    Рекурсивно копирует директории со всем содержимым. Для файлов сохраняет
    метаданные (время изменения, права доступа). Если назначение - директория,
    файл копируется в эту директорию с исходным именем

    Args:
        src(str)
        dst(str)
    Returns:
        None
    '''
    try:
        from src.history import add_to_undo_stack
        if not os.path.exists(src):
            print(f"cp: {src}: Такого файла или каталога нет")
            log_error(f"cp: {src} Такого файла или каталога нет")
            return

        actual_dst = dst
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            if os.path.isdir(dst):
                actual_dst = os.path.join(dst, os.path.basename(src))
            shutil.copy2(src, actual_dst)

        add_to_undo_stack('cp', actual_dst)
        print(f"Скопировано: {src} -> {actual_dst}")
    except Exception as e:
        print(e)
        log_error(str(e))
