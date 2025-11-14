import os
from src.logger import setup_logger
from src.parser import parse_command

def main() -> None:
    '''
    Главная функция
    Инициализирует логирование, выводит приветственное сообщение и запускает
    бесконечный цикл обработки команд пользователя

    Returns:
        None
    Raises:
        KeyboardInterrupt: Обрабатывается для корректного выхода при Ctrl+C
        EOFError: Обрабатывается для корректного выхода при Ctrl+D
    '''
    setup_logger()
    print("Добро пожаловать в оболочку, введите команду или 'exit' для выхода")
    print("Доступные команды: ls, cd, cat, cp, mv, rm [-r], zip, unzip, tar, untar, grep, history, undo, exit")
    while True:
        try:
            prompt = f"{os.getcwd()}$"
            user_input = input(prompt)
            parse_command(user_input)
        except KeyboardInterrupt:
            print("Выход")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
