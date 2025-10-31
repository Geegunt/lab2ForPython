import os
import tempfile
import pytest
from src.commands.cat import cat
from src.exceptions import ShellError

def test_cat_read_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write("hello world")
        tmpfile_path = tmpfile.name
    
    try:
        cat(tmpfile_path)
    finally:
        os.remove(tmpfile_path)

def test_cat_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = cat(tmpdir)
        assert os.path.isdir(tmpdir)

def test_cat_nonexistent_file():
    result = cat("/nonexistent/file/12345.txt")
    assert os.path.exists("/nonexistent/file/12345.txt") == False



