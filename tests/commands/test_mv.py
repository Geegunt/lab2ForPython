import os
import tempfile
from src.commands.mv import mv

def test_mv_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "source.txt")
        dst_file = os.path.join(tmpdir, "dest.txt")
        with open(src_file, 'w') as f:
            f.write("test content")
        mv(src_file, dst_file)
        assert not os.path.exists(src_file)
        assert os.path.exists(dst_file)
        with open(dst_file, 'r') as f:
            assert f.read() == "test content"

def test_mv_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = os.path.join(tmpdir, "source_dir")
        dst_dir = os.path.join(tmpdir, "dest_dir")
        os.makedirs(src_dir)
        test_file = os.path.join(src_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        mv(src_dir, dst_dir)
        assert not os.path.exists(src_dir)
        assert os.path.exists(dst_dir)
        assert os.path.exists(os.path.join(dst_dir, "test.txt"))
