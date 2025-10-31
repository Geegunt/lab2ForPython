import os
import shutil
from src.logger import log_error

def cp(src, dst):
    try:
        from src.history import add_to_undo_stack
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        add_to_undo_stack('cp', dst)
        print(f"Скопировано: {src} -> {dst}")
    except Exception as e:
        print(e)
        log_error(str(e))



