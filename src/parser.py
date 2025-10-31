import sys
from src.logger import log_command, log_error
from src.history import add_to_history, show_history
from src.commands import cd, cat, cp, mv, rm
from src.commands.zip_cmd import zip_folder, unzip_archive
from src.commands.tar_cmd import tar_folder, untar_archive
from src.commands.grep import grep
from src.commands.undo import undo
from src.commands.ls import run as ls_run


def parse_command(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    add_to_history(user_input)

    try:
        if cmd == "ls":
            ls_run(args)
        elif cmd == "cd":
            if len(args) != 1:
                print("cd: invalid arguments")
                return
            cd(args[0])
        elif cmd == "cat":
            if not args:
                return
            cat(args[0])
        elif cmd == "cp":
            if len(args) < 2:
                return
            cp(args[0], args[1])
        elif cmd == "mv":
            if len(args) < 2:
                return
            mv(args[0], args[1])
        elif cmd == "rm":
            if not args:
                return
            recursive = "-r" in args
            path_arg = args[-1]
            rm(path_arg, recursive=recursive)
        elif cmd == "zip":
            if len(args) < 2:
                print("Использование: zip <folder> <archive.zip>")
                return
            zip_folder(args[0], args[1])
        elif cmd == "unzip":
            if not args:
                print("Использование: unzip <archive.zip>")
                return
            unzip_archive(args[0])
        elif cmd == "tar":
            if len(args) < 2:
                print("Использование: tar <folder> <archive.tar.gz>")
                return
            tar_folder(args[0], args[1])
        elif cmd == "untar":
            if not args:
                print("Использование: untar <archive.tar.gz>")
                return
            untar_archive(args[0])
        elif cmd == "grep":
            if len(args) < 2:
                print("Использование: grep <pattern> <path> [-r] [-i]")
                return
            recursive = "-r" in args
            case_insensitive = "-i" in args
            pattern = args[0]
            path = args[-1]
            grep(pattern, path, recursive=recursive, case_insensitive=case_insensitive)
        elif cmd == "history":
            n = int(args[0]) if args and args[0].isdigit() else 10
            show_history(n)
        elif cmd == "undo":
            undo()
        elif cmd == "exit":
            print("Выход")
            sys.exit(0)
        else:
            print(f"Неизвестная команда: {cmd}")
            log_error(f"Неизвестная команда: {cmd}")
        log_command(user_input)
    except Exception as e:
        print(e)
        log_error(e)


