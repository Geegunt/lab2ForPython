import os
import tarfile
from src.logger import log_error

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



