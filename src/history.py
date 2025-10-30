import os
import json

HISTORY_FILE = ".history"

undo_stack = []

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        try:
            return [line.strip() for line in f if line.strip()]
        except:
            return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        for cmd in history:
            f.write(cmd + '\n')

def add_to_history(command: str):
    history = load_history()
    history.append(command)
    save_history(history)

def get_last_command():
    history = load_history()
    return history[-1] if history else None

def remove_last_command():
    history = load_history()
    if history:
        history.pop()
        save_history(history)

def show_history(n=10):
    history = load_history()
    start = max(0, len(history) - n)
    for i, cmd in enumerate(history[start:], start=start+1):
        print(f"{i}: {cmd}")

def add_to_undo_stack(cmd_type, *args):
    global undo_stack
    undo_stack.append({'type': cmd_type, 'args': args})
    if len(undo_stack) > 10:
        undo_stack.pop(0)

def get_last_undo():
    global undo_stack
    return undo_stack[-1] if undo_stack else None

def remove_last_undo():
    global undo_stack
    if undo_stack:
        undo_stack.pop()