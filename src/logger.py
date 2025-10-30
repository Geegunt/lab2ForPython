import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        filename='shell.log',
        level=logging.INFO,
        format='%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_command(command: str):
    logging.info(command)

def log_error(message: str):
    logging.info(f"ERROR: {message}")