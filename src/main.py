import os
from src.logger import setup_logger
from src.parser import parse_command

def main() -> None:
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
