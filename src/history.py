import os
from src.config import HISTORY_FILE

#Cтек отмены операций (максимум 10 элементов)
_undo_stack = []


def load_history():
    """
    Загружает историю команд из файла
    Returns:
        list
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        try:
            return [line.strip() for line in f if line.strip()]
        except Exception:
            return []


def save_history(history):
    """
    Сохраняет историю команд в файл

    Args:
        history (list)
    Returns:
        None
    """
    with open(HISTORY_FILE, 'w') as f:
        for cmd in history:
            f.write(cmd + '\n')


def add_to_history(command: str):
    """
    Добавляет команду в историю и сохраняет в файл.

    Args:
        command (str)
    Returns:
        None
    """
    history = load_history()
    history.append(command)
    save_history(history)


def get_last_command():
    """
    Получает последнюю команду из истории
    Returns:
        str or None
    """
    history = load_history()
    return history[-1] if history else None


def remove_last_command():
    """
    Удаляет последнюю команду из истории и сохраняет изменения

    Returns:
        None
    """
    history = load_history()
    if history:
        history.pop()
        save_history(history)


def show_history(n=10):
    """
    Выводит последние n команд из истории с номерами

    Args:
        n (int, optional)

    Returns:
        None
    """
    history = load_history()
    start = max(0, len(history) - n)
    for i, cmd in enumerate(history[start:], start=start+1):
        print(f"{i}: {cmd}")


def add_to_undo_stack(cmd_type, *args):
    """
    Добавляет операцию в стек отмены
    Если стек превышает 10 элементов, удаляет самую старую операцию

    Args:
        cmd_type (str)
        *args
    Returns:
        None
    """
    global _undo_stack
    _undo_stack.append({'type': cmd_type, 'args': args})
    if len(_undo_stack) > 10:
        _undo_stack.pop(0)


def get_last_undo():
    """
    Получает последнюю операцию из стека отмены

    Returns:
        dict or None
    """
    return _undo_stack[-1] if _undo_stack else None


def remove_last_undo():
    """
    Удаляет последнюю операцию из стека отмены

    Returns:
        None
    """
    global _undo_stack
    if _undo_stack:
        _undo_stack.pop()
