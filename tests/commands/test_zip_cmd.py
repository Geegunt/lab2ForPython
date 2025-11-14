import os
import tempfile
import zipfile
from src.commands.zip_cmd import zip_folder, unzip_archive

def test_zip_folder():
    with tempfile.TemporaryDirectory() as tmpdir:
        src_dir = os.path.join(tmpdir, "source")
        os.makedirs(src_dir)
        test_file = os.path.join(src_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        archive = os.path.join(tmpdir, "test.zip")
        zip_folder(src_dir, archive)
        assert os.path.exists(archive)
        with zipfile.ZipFile(archive, 'r') as zf:
            names = zf.namelist()
            assert any("test.txt" in name for name in names)

def test_unzip_archive(tmp_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        archive = os.path.join(tmpdir, "test.zip")
        with zipfile.ZipFile(archive, 'w') as zf:
            zf.write(test_file, "test.txt")
        os.remove(test_file)
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            unzip_archive(archive)
            assert os.path.exists("test")
        finally:
            os.chdir(original_dir)
