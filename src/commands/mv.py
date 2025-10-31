import shutil
from src.logger import log_error

def mv(src, dst):
    try:
        from src.history import add_to_undo_stack
        add_to_undo_stack('mv', src, dst)
        shutil.move(src, dst)
        print(f"Перемещено: {src} -> {dst}")
    except Exception as e:
        print(e)
        log_error(str(e))



