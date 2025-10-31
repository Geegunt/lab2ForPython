import os
import re
from src.logger import log_error

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



