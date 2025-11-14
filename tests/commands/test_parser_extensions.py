import os
import tempfile
from src.parser import parse_command

def test_zip_auto_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            test_folder = "test_folder"
            os.makedirs(test_folder)
            parse_command("zip test_folder archive")
            assert os.path.exists("archive.zip")
        finally:
            os.chdir(original_dir)

def test_tar_auto_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            test_folder = "test_folder"
            os.makedirs(test_folder)
            parse_command("tar test_folder archive")
            assert os.path.exists("archive.tar.gz")
        finally:
            os.chdir(original_dir)

def test_unzip_auto_extension():
    import zipfile
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            with zipfile.ZipFile("test.zip", 'w') as zf:
                zf.writestr("test.txt", "content")
            parse_command("unzip test")
            assert os.path.exists("test")
        finally:
            os.chdir(original_dir)

def test_untar_auto_extension():
    import tarfile
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        try:
            os.chdir(tmpdir)
            test_file = os.path.join(tmpdir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("content")
            with tarfile.open("test.tar.gz", 'w:gz') as tf:
                tf.add(test_file, arcname="test.txt")
            parse_command("untar test")
            assert os.path.exists("test")
        finally:
            os.chdir(original_dir)
