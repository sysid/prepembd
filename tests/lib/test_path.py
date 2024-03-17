import tempfile
from pathlib import Path

import pytest

from prepembd.lib.path import scan_directory


@pytest.fixture
def create_test_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        base_dir = Path(tmpdirname)
        (base_dir / "dir1").mkdir()
        (base_dir / "dir2").mkdir()
        (base_dir / "excluded").mkdir()
        (base_dir / "excluded/dir3").mkdir()
        (base_dir / "dir1" / "test1.md").write_text("Content")
        (base_dir / "dir2" / "test2.md").write_text("Content")
        (base_dir / "dir2" / "empty.md").write_text("")  # Empty file
        (base_dir / "excluded" / "test3.md").write_text("Content")
        (base_dir / "excluded/dir3" / "test4.md").write_text("Content")
        yield base_dir


def test_scan_directory(create_test_directory):
    base_dir = create_test_directory
    excluded_dirs = [Path("excluded")]
    result = scan_directory(base_dir, excluded_dirs, min_size=1)
    assert len(result) == 2
    assert Path("dir1/test1.md") in result
    assert Path("dir2/test2.md") in result
    assert Path("dir2/empty.md") not in result  # Because it's empty
    assert Path("excluded/test3.md") not in result  # Because it's excluded
