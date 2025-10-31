import os
import tempfile
import tarfile
import pytest
from src.commands.tar_cmd import tar_folder, untar_archive

def test_tar_folder():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = os.path.join(tmpdir, "source")
        os.makedirs(src_dir)
        test_file = os.path.join(src_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        archive = os.path.join(tmpdir, "test.tar.gz")
        tar_folder(src_dir, archive)
        assert os.path.exists(archive)
        
        with tarfile.open(archive, 'r:gz') as tf:
            assert "source/test.txt" in tf.getnames()

def test_untar_archive(tmp_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        archive = os.path.join(tmpdir, "test.tar.gz")
        with tarfile.open(archive, 'w:gz') as tf:
            tf.add(test_file, "test.txt")
        
        os.remove(test_file)
        os.chdir(tmpdir)
        try:
            untar_archive(archive)
            assert os.path.exists("test.txt")
        finally:
            os.chdir(tmp_path)

