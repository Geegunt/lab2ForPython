import os
import tempfile
from src.commands.cd import cd

def test_cd_to_directory(tmp_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = tmp_path
        os.chdir(original_dir)
        cd(tmpdir)
        current = os.getcwd()
        assert os.path.samefile(current, tmpdir)

def test_cd_to_home(tmp_path):
    original_dir = tmp_path
    os.chdir(original_dir)
    cd('~')
    current = os.getcwd()
    assert os.path.samefile(current, os.path.expanduser('~'))

def test_cd_up(tmp_path):
    original_dir = tmp_path
    os.chdir(original_dir)
    parent_dir = os.path.dirname(original_dir)
    cd("..")
    current = os.getcwd()
    assert os.path.samefile(current, parent_dir)
