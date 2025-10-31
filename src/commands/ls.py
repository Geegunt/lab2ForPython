import os
from src.logger import log_error
from src.exceptions import ShellError

def ls(path='.', long_format=False):
    try:
        if not os.path.exists(path):
            raise ShellError(f"ls: cannot access '{path}': No such file or directory")

        items = os.listdir(path)
        items.sort()
        for item in items:
            full_path = os.path.join(path, item)
            if long_format:
                if os.path.isdir(full_path):
                    size = "-"
                    typ = "dir"
                else:
                    size = str(os.path.getsize(full_path))
                    typ = "file"
                print(f"{typ:<4} {size:>8} {item}")
            else:
                print(item, end='  ')
        if not long_format:
            print()
    except Exception as e:
        print(f"ls: cannot open directory '{path}': {e}")
        log_error(f"ls: cannot open directory '{path}': {e}")


def run(args):
    long_format = False
    paths = []
    for arg in args:
        if arg == '-l':
            long_format = True
        elif arg.startswith('-'):
            print(f"ls: invalid option -- '{arg}'")
            log_error(f"ls: invalid option -- '{arg}'")
            return
        else:
            paths.append(arg)
    target = paths[0] if paths else '.'
    ls(target, long_format=long_format)

