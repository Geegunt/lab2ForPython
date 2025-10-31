import os
import shutil
from src.logger import log_error
from src.exceptions import ShellError

def rm(path, recursive=False):
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
                trash_path = os.path.join('.trash', os.path.basename(path))
                os.makedirs('.trash', exist_ok=True)
                shutil.move(path, trash_path)
                add_to_undo_stack('rm', path, trash_path)
                print(f"Удалена директория: {path}")
            else:
                print("Отмена")
        else:
            trash_path = os.path.join('.trash', os.path.basename(path))
            os.makedirs('.trash', exist_ok=True)
            shutil.move(path, trash_path)
            add_to_undo_stack('rm', path, trash_path)
            print(f"Удален файл: {path}")
    except Exception as e:
        print(e)
        log_error(str(e))



