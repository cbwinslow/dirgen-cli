# tests/test_core.py
import tempfile
from pathlib import Path
from directory_builder.core import create_structure


def test_create_structure():
    structure = ["README.md", {"src": ["main.py", {"utils": []}]}, "tests/"]
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        create_structure(base, structure)
        assert (base / "README.md").exists()
        assert (base / "src" / "main.py").exists()
        assert (base / "src" / "utils").is_dir()
        assert (base / "tests").is_dir()
