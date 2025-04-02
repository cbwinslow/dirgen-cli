import tempfile
from pathlib import Path
from directory_builder.core import create_structure, diff_structure

def test_diff_structure():
    structure = ["README.md", {"src": ["main.py"]}]
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # No structure yet, so everything is missing
        missing, extra = diff_structure(base, structure)
        assert len(missing) == 2  # 'README.md' + 'src'
        assert len(extra) == 0

        # Now create the structure
        create_structure(base, structure)
        missing, extra = diff_structure(base, structure)
        assert not missing
        assert not extra
