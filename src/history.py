import os
from src.config import HISTORY_FILE


class HistoryManager:
    def __init__(self, history_file: str):
        self.history_file = history_file
        self.undo_stack = []

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        with open(self.history_file, 'r') as f:
            try:
                return [line.strip() for line in f if line.strip()]
            except:
                return []

    def save_history(self, history):
        with open(self.history_file, 'w') as f:
            for cmd in history:
                f.write(cmd + '\n')

    def add_to_history(self, command: str):
        history = self.load_history()
        history.append(command)
        self.save_history(history)

    def get_last_command(self):
        history = self.load_history()
        return history[-1] if history else None

    def remove_last_command(self):
        history = self.load_history()
        if history:
            history.pop()
            self.save_history(history)

    def show_history(self, n=10):
        history = self.load_history()
        start = max(0, len(history) - n)
        for i, cmd in enumerate(history[start:], start=start+1):
            print(f"{i}: {cmd}")

    def add_to_undo_stack(self, cmd_type, *args):
        self.undo_stack.append({'type': cmd_type, 'args': args})
        if len(self.undo_stack) > 10:
            self.undo_stack.pop(0)

    def get_last_undo(self):
        return self.undo_stack[-1] if self.undo_stack else None

    def remove_last_undo(self):
        if self.undo_stack:
            self.undo_stack.pop()


_history_manager = HistoryManager(HISTORY_FILE)


def load_history():
    return _history_manager.load_history()

def save_history(history):
    return _history_manager.save_history(history)

def add_to_history(command: str):
    return _history_manager.add_to_history(command)

def get_last_command():
    return _history_manager.get_last_command()

def remove_last_command():
    return _history_manager.remove_last_command()

def show_history(n=10):
    return _history_manager.show_history(n)

def add_to_undo_stack(cmd_type, *args):
    return _history_manager.add_to_undo_stack(cmd_type, *args)

def get_last_undo():
    return _history_manager.get_last_undo()

def remove_last_undo():
    return _history_manager.remove_last_undo()