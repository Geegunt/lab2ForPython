import os
import zipfile
from src.logger import log_error

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



