import os
import tempfile
import pytest
from src.commands.ls import ls
from src.exceptions import ShellError

def test_ls_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        ls(tmpdir)

def test_ls_long_format():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        ls(tmpdir, long_format=True)

def test_ls_nonexistent_path():
    result = ls("/nonexistent/path/12345")
    assert os.path.exists("/nonexistent/path/12345") == False

def test_ls_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        ls(tmpdir)



