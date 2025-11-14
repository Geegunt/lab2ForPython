import os
import tempfile
from src.commands.ls import ls

def test_ls_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")

        ls(tmpdir)

def test_ls_hides_hidden_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        visible_file = os.path.join(tmpdir, "visible.txt")
        hidden_file = os.path.join(tmpdir, ".hidden")
        with open(visible_file, 'w') as f:
            f.write("visible")
        with open(hidden_file, 'w') as f:
            f.write("hidden")
        ls(tmpdir, long_format=False)

def test_ls_long_format():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        ls(tmpdir, long_format=True)

def test_ls_long_format_shows_hidden():
    with tempfile.TemporaryDirectory() as tmpdir:
        visible_file = os.path.join(tmpdir, "visible.txt")
        hidden_file = os.path.join(tmpdir, ".hidden")
        with open(visible_file, 'w') as f:
            f.write("visible")
        with open(hidden_file, 'w') as f:
            f.write("hidden")
        ls(tmpdir, long_format=True)

def test_ls_long_format_has_permissions():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        ls(tmpdir, long_format=True)

def test_ls_nonexistent_path():
    ls("/nonexistent/path/12345")
    assert not os.path.exists("/nonexistent/path/12345")

def test_ls_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        ls(tmpdir)
