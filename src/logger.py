import logging
import os


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SRC_DIR, "shell.log")

def setup_logger():
    '''
    Настраивает логирование ждя оболочки

    Returns: None
    '''
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_command(command: str):
    '''
    Логирует выполненную команду в файл

    Args: command(str)
    Returns: None
    '''
    logging.info(command)

def log_error(message: str):
    '''
    Логирует ошибку в файл лога с подписью "ERROR"
    Args: message(str)
    Returns: None
    '''
    logging.info(f"ERROR: {message}")
