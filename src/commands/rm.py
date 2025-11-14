import os
import shutil
from src.logger import log_error
from src.exceptions import ShellError
from src.config import TRASH_DIR

def rm(path, recursive=False):
    '''
    Удаляет файл или директорию
    Файлы и директории не удаляются полностью, а перемещаются в папку .trash
    в директории src. Для удаления директорий требуется флаг -r  и подтверждение.

    Args:
         path(str)
         recursive(bool, optional)
    Returns:
        None
    Raises:
        ShellError
    '''
    try:
        from src.history import add_to_undo_stack
        if os.path.isdir(path):
            if not recursive:
                raise ShellError("Ошибка. Это директория. Используйте -r для рекурсивного удаления")
            if path in ['/', os.path.expanduser('~'), '..']:
                print("Запрещено удалять корневую или домашнюю директорию")
                log_error("rm: попытка удалить защищенную директорию")
                return
            confirm = input(f"Удалить директорию {path} рекурсивно? (y/n): ")
            if confirm.lower() == 'y':
                trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
                os.makedirs(TRASH_DIR, exist_ok=True)
                shutil.move(path, trash_path)
                add_to_undo_stack('rm', path, trash_path)
                print(f"Удалена директория: {path}")
            else:
                print("Отмена")
        else:
            trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
            os.makedirs(TRASH_DIR, exist_ok=True)
            shutil.move(path, trash_path)
            add_to_undo_stack('rm', path, trash_path)
            print(f"Удален файл: {path}")
    except Exception as e:
        print(e)
        log_error(str(e))
