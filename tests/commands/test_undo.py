import os
import tempfile
import pytest
from src.commands.undo import undo
from src.commands.cp import cp
from src.commands.mv import mv

def test_undo_cp():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "source.txt")
        dst_file = os.path.join(tmpdir, "dest.txt")
        
        with open(src_file, 'w') as f:
            f.write("test")
        
        cp(src_file, dst_file)
        assert os.path.exists(dst_file)
        
        undo()
        assert not os.path.exists(dst_file)

def test_undo_mv():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "source.txt")
        dst_file = os.path.join(tmpdir, "dest.txt")
        
        with open(src_file, 'w') as f:
            f.write("test")
        
        mv(src_file, dst_file)
        assert not os.path.exists(src_file)
        assert os.path.exists(dst_file)
        
        undo()
        assert os.path.exists(src_file)
        assert not os.path.exists(dst_file)



