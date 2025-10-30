import os
import shutil
import zipfile
import tarfile
import re

from src.logger import log_error
from src.exceptions import ShellError

def ls(path='.', long_format=False):
    try:
        if not os.path.exists(path):
            raise ShellError(f"ls: cannot access '{path}': No such file or directory")

        items = os.listdir(path)
        items.sort()
        for item in items:
            full_path = os.path.join(path, item)
            if long_format:
                if os.path.isdir(full_path):
                    size = "-"
                    typ = "dir"
                else:
                    size = str(os.path.getsize(full_path))
                    typ = "file"
                print(f"{typ:<4} {size:>8} {item}")
            else:
                print(item, end='  ')
        if not long_format:
            print()
    except Exception as e:
        print(f"ls: cannot open directory '{path}': {e}")
        log_error(f"ls: cannot open directory '{path}': {e}")

def cd(path):
    try:
        if path == '~':
            path = os.path.expanduser('~')
        elif path == "..":
            path = os.path.dirname(os.getcwd())
        os.chdir(path)
    except Exception as e:
        print(e)
        log_error(str(e))

def cat(filename):
    try:
        if os.path.isdir(filename):
            raise ShellError("Ошибка. Это директория, а не файл.")
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(e)
        log_error(str(e))

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

def mv(src, dst):
    try:
        from src.history import add_to_undo_stack
        add_to_undo_stack('mv', src, dst)
        shutil.move(src, dst)
        print(f"Перемещено: {src} -> {dst}")
    except Exception as e:
        print(e)
        log_error(str(e))

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

def zip_folder(folder, archive_name):
    try:
        if not os.path.exists(folder):
            print(f"Ошибка: каталог {folder} не существует")
            log_error(f"zip: каталог {folder} не существует")
            return
        
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folder))
                    zipf.write(file_path, arcname)
        
        print(f"Архив {archive_name} создан успешно")
    except Exception as e:
        print(e)
        log_error(str(e))

def unzip_archive(archive_name):
    try:
        if not os.path.exists(archive_name):
            print(f"Ошибка: архив {archive_name} не существует")
            log_error(f"unzip: архив {archive_name} не существует")
            return
        
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            zipf.extractall('.')
        
        print(f"Архив {archive_name} распакован успешно")
    except Exception as e:
        print(e)
        log_error(str(e))

def tar_folder(folder, archive_name):
    try:
        if not os.path.exists(folder):
            print(f"Ошибка: каталог {folder} не существует")
            log_error(f"tar: каталог {folder} не существует")
            return
        
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(folder, arcname=os.path.basename(folder))
        
        print(f"Архив {archive_name} создан успешно")
    except Exception as e:
        print(e)
        log_error(str(e))

def untar_archive(archive_name):
    try:
        if not os.path.exists(archive_name):
            print(f"Ошибка: архив {archive_name} не существует")
            log_error(f"untar: архив {archive_name} не существует")
            return
        
        with tarfile.open(archive_name, 'r:gz') as tar:
            tar.extractall('.')
        
        print(f"Архив {archive_name} распакован успешно")
    except Exception as e:
        print(e)
        log_error(str(e))

def grep(pattern, path, recursive=False, case_insensitive=False):
    try:
        if not os.path.exists(path):
            print(f"grep: {path}: No such file or directory")
            log_error(f"grep: {path} не существует")
            return
        
        files_to_search = []
        if os.path.isfile(path):
            files_to_search = [path]
        elif recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    files_to_search.append(os.path.join(root, file))
        else:
            print("grep: нужно использовать -r для поиска в каталоге")
            log_error("grep: нужно использовать -r для поиска в каталоге")
            return
        
        flags = 0
        if case_insensitive:
            flags = re.IGNORECASE
        
        found_anything = False
        for file_path in files_to_search:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(pattern, line, flags):
                            print(f"{file_path}:{line_num}:{line.rstrip()}")
                            found_anything = True
            except:
                continue
        
        if not found_anything:
            print(f"Совпадений не найдено")
    except Exception as e:
        print(e)
        log_error(str(e))

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
