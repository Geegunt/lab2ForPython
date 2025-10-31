import os
import tempfile
import pytest
from src.commands.cp import cp

def test_cp_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "source.txt")
        dst_file = os.path.join(tmpdir, "dest.txt")
        
        with open(src_file, 'w') as f:
            f.write("test content")
        
        cp(src_file, dst_file)
        assert os.path.exists(dst_file)
        with open(dst_file, 'r') as f:
            assert f.read() == "test content"

def test_cp_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = os.path.join(tmpdir, "source_dir")
        dst_dir = os.path.join(tmpdir, "dest_dir")
        
        os.makedirs(src_dir)
        test_file = os.path.join(src_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        cp(src_dir, dst_dir)
        assert os.path.exists(dst_dir)
        assert os.path.exists(os.path.join(dst_dir, "test.txt"))



