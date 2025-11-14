import os
import tempfile
from src.commands.grep import grep

def test_grep_in_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write("hello world\nfoo bar\nbaz")
        tmpfile_path = tmpfile.name
    try:
        grep("foo", tmpfile_path)
    finally:
        os.remove(tmpfile_path)

def test_grep_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        subdir = os.path.join(tmpdir, "sub")
        os.makedirs(subdir)
        test_file = os.path.join(subdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("hello world")
        grep("hello", tmpdir, recursive=True)

def test_grep_case_insensitive():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write("Hello World\nfoo bar")
        tmpfile_path = tmpfile.name
    try:
        grep("hello", tmpfile_path, case_insensitive=True)
    finally:
        os.remove(tmpfile_path)

def test_grep_not_found():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write("hello world")
        tmpfile_path = tmpfile.name
    try:
        grep("xyzabc", tmpfile_path)
    finally:
        os.remove(tmpfile_path)

def test_grep_directory_without_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("hello")
        grep("hello", tmpdir, recursive=False)

def test_grep_multiple_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "file1.txt")
        file2 = os.path.join(tmpdir, "file2.txt")
        with open(file1, 'w') as f:
            f.write("test content")
        with open(file2, 'w') as f:
            f.write("another test")
        grep("test", tmpdir, recursive=True)

def test_grep_regex_pattern():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write("hello123\nworld456\nfoo")
        tmpfile_path = tmpfile.name
    try:
        grep(r"\d+", tmpfile_path)  # Поиск цифр
    finally:
        os.remove(tmpfile_path)
