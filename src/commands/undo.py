import os
import shutil
from src.logger import log_error

def undo():
    '''
    Отменяет последнюю операцию из стека отмены

    Поддерживает отмену следующих операций:
    cp, mv, rm

    Returns:
         None
    '''
    try:
        from src.history import get_last_undo, remove_last_undo
        last_undo = get_last_undo()

        if not last_undo:
            print("Нет команд для отмены")
            return

        cmd_type = last_undo['type']
        args = last_undo['args']

        if cmd_type == 'cp':
            target_path = args[0]
            if os.path.exists(target_path):
                if os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)
                print(f"Отменено копирование: {target_path}")

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
