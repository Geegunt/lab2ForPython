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
    '''
    Функция парсит и выполнят команду пользователя

    Разбивает входную строку на команду и аргументы, валидирует их количество,
    вызывает соответствующую функцию команды и логирует результат выполнения.
    Автоматически добавляет расширения для архивов (zip, tar) если они не указаны

    :param user_input:
    :return None:
    '''
    parts = user_input.strip().split()
    if not parts:
        return
    cmd = parts[0].lower()
    args = parts[1:]

    add_to_history(user_input)

    try:
        if cmd == "ls":
            ls_run(args)
        elif cmd == "cd":
            if len(args) != 1:
                print("cd: неверный аргумент")
                log_error("cd: неверный аргумент")
                return
            cd(args[0])
        elif cmd == "cat":
            if not args:
                print("cat: требуется аргумент")
                log_error("cat: требуется аргумент")
                return
            cat(args[0])
        elif cmd == "cp":
            if len(args) == 0:
                print("cp: требуется 2 аргумента")
                log_error("cp: требуется 2 аргумента")
                return
            if len(args) == 1:
                print("cp: недостаточно аргументов")
                log_error("cp: недостаточно аргументов")
                return
            if len(args) > 2:
                print("cp: слишком много аргументов")
                log_error("cp: слишком много аргументов")
                return
            cp(args[0], args[1])
        elif cmd == "mv":
            if len(args) < 2:
                print("mv: требуется 2 аргумента")
                log_error("mv: требуется 2 аргумента")
                return
            mv(args[0], args[1])
        elif cmd == "rm":
            if not args:
                print("rm: требуется аргумент")
                log_error("rm: требуется аргумент")
                return
            valid_args = [arg for arg in args if not arg.startswith('-')]
            if not valid_args:
                print("rm: требуется указать путь")
                log_error("rm: требуется указать путь")
                return
            recursive = "-r" in args
            path_arg = valid_args[-1]
            rm(path_arg, recursive=recursive)
        elif cmd == "zip":
            if len(args) < 2:
                print("Использование: zip <folder> <archive.zip>")
                log_error("zip: недостаточно аргументов")
                return
            archive_name = args[1]
            # Автоматически добавляем расширение .zip, если не указано
            if not archive_name.endswith('.zip'):
                archive_name = archive_name + '.zip'
            zip_folder(args[0], archive_name)
        elif cmd == "unzip":
            if not args:
                print("Использование: unzip <archive.zip>")
                log_error("unzip: требуется аргумент")
                return
            archive_name = args[0]
            # Автоматически добавляем расширение .zip, если не указано
            if not archive_name.endswith('.zip'):
                archive_name = archive_name + '.zip'
            unzip_archive(archive_name)
        elif cmd == "tar":
            if len(args) < 2:
                print("Использование: tar <folder> <archive.tar.gz>")
                log_error("tar: недостаточно аргументов")
                return
            archive_name = args[1]
            # Автоматически добавляем расширение .tar.gz, если не указано
            if not archive_name.endswith('.tar') and not archive_name.endswith('.tar.gz'):
                archive_name = archive_name + '.tar.gz'
            tar_folder(args[0], archive_name)
        elif cmd == "untar":
            if not args:
                print("Использование: untar <archive.tar.gz>")
                log_error("untar: требуется аргумент")
                return
            archive_name = args[0]
            # Автоматически добавляем расширение .tar.gz, если не указано
            if not archive_name.endswith('.tar') and not archive_name.endswith('.tar.gz'):
                archive_name = archive_name + '.tar.gz'
            untar_archive(archive_name)
        elif cmd == "grep":
            if len(args) < 2:
                print("Использование: grep <pattern> <path> [-r] [-i]")
                log_error("grep: недостаточно аргументов")
                return
            valid_flags = [arg for arg in args if arg.startswith('-')]
            recursive = "-r" in valid_flags
            case_insensitive = "-i" in valid_flags
            non_flag_args = [arg for arg in args if not arg.startswith('-')]
            if len(non_flag_args) < 2:
                print("grep: требуется указать pattern и path")
                log_error("grep: требуется указать pattern и path")
                return
            pattern = non_flag_args[0]
            path = non_flag_args[-1]
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
        log_error(str(e))
