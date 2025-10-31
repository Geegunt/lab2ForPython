import os
import tempfile
import pytest
from src.commands.rm import rm

def test_rm_file(monkeypatch):
    import builtins
    original_input = builtins.input
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        # mock input to skip confirmation if any
        def mock_input(prompt):
            return 'y'
        monkeypatch.setattr(builtins, 'input', mock_input)
        
        rm(test_file)
        assert not os.path.exists(test_file)

def test_rm_directory_without_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "test_dir")
        os.makedirs(test_dir)
        
        rm(test_dir)
        assert os.path.exists(test_dir)

def test_rm_directory_recursive(monkeypatch):
    import builtins
    
    def mock_input(prompt):
        return 'y'
    monkeypatch.setattr(builtins, 'input', mock_input)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "test_dir")
        os.makedirs(test_dir)
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        rm(test_dir, recursive=True)
        assert not os.path.exists(test_dir)

