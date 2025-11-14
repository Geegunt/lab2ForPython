import os
import shutil
import zipfile
from src.logger import log_error

def zip_folder(folder, archive_name):
    '''
    Создаёт ZIP-архив из директории
    Рекурсивно обходит директорию и добавляет все файлы в ZIP-архив с сжатием.
    Сохраняет структуру директорий внутри архива

    Args:
        folder (str)
        archive_name (str)
    Returns:
        None
    '''
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
    '''
    Распаковывает ZIP-архив
    Создает папку с именем архива (без расширения .zip) и распаковывает туда
    содержимое
    Args:
        archive_name (str)
    Returns:
        None
    '''
    try:
        if not os.path.exists(archive_name):
            print(f"Ошибка: архив {archive_name} не существует")
            log_error(f"unzip: архив {archive_name} не существует")
            return

        # Получаем имя папки из имени архива (убираем расширение .zip)
        folder_name = archive_name
        if folder_name.endswith('.zip'):
            folder_name = folder_name[:-4]  # Убираем .zip

        # Создаем папку с именем архива (без расширения)
        os.makedirs(folder_name, exist_ok=True)

        # Распаковываем архив и проверяем структуру
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            # Получаем список всех файлов в архиве
            file_list = zipf.namelist()

            # Проверяем, есть ли одна папка на верхнем уровне
            top_level_items = set()
            for name in file_list:
                # Получаем первый элемент пути (верхний уровень)
                first_part = name.split('/')[0] if '/' in name else name.split('\\')[0]
                if first_part:  # Игнорируем пустые имена
                    top_level_items.add(first_part)

            # Если есть только одна папка на верхнем уровне, распаковываем её содержимое напрямую
            if len(top_level_items) == 1:
                top_folder = list(top_level_items)[0]
                # Распаковываем во временную папку
                temp_extract = folder_name + '_temp'
                zipf.extractall(temp_extract)

                # Перемещаем содержимое из temp_extract/top_folder в folder_name
                source_path = os.path.join(temp_extract, top_folder)
                if os.path.exists(source_path):
                    # Перемещаем все содержимое
                    for item in os.listdir(source_path):
                        src = os.path.join(source_path, item)
                        dst = os.path.join(folder_name, item)
                        if os.path.exists(dst):
                            if os.path.isdir(dst):
                                shutil.rmtree(dst)
                            else:
                                os.remove(dst)
                        shutil.move(src, dst)

                    # Удаляем временную папку
                    shutil.rmtree(temp_extract)
                else:
                    # Если структура неожиданная, просто распаковываем как есть
                    zipf.extractall(folder_name)
            else:
                # Если несколько элементов на верхнем уровне, распаковываем как есть
                zipf.extractall(folder_name)

        print(f"Архив {archive_name} распакован в папку {folder_name}")
    except Exception as e:
        print(e)
        log_error(str(e))
