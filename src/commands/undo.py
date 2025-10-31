import os
import shutil
from src.logger import log_error

def undo():
    try:
        from src.history import get_last_undo, remove_last_undo
        last_undo = get_last_undo()
        
        if not last_undo:
            print("Нет команд для отмены")
            return
        
        cmd_type = last_undo['type']
        args = last_undo['args']
        
        if cmd_type == 'cp':
            if os.path.exists(args[0]):
                if os.path.isdir(args[0]):
                    shutil.rmtree(args[0])
                else:
                    os.remove(args[0])
                print(f"Отменено копирование: {args[0]}")
        
        elif cmd_type == 'mv':
            if os.path.exists(args[1]):
                shutil.move(args[1], args[0])
                print(f"Отменено перемещение: {args[1]} -> {args[0]}")
        
        elif cmd_type == 'rm':
            if os.path.exists(args[1]):
                shutil.move(args[1], args[0])
                print(f"Отменено удаление: восстановлено {args[0]}")
        
        remove_last_undo()
    except Exception as e:
        print(e)
        log_error(str(e))



