import logging
from pathlib import Path
from typing import Iterable

_log = logging.getLogger(__name__)


def scan_directory(
    directory: Path, excluded_dirs: list[str] = None, min_size: int = 100
) -> list[Path]:
    """
    Recursively scan a directory for Markdown (.md) files, returning a list of paths relative to the base directory.

    Parameters:
    - directory (Path): The base directory from which the search begins.
    - excluded_dirs (list[str]): A list of RELATIVE directories to exclude from the search.
      Any .md file located within these directories or their subdirectories will not be included in the result.
    - min_size (int, optional): The minimum file size (in bytes) for a file to be included. Defaults to 100 bytes.

    Returns:
    - list[Path]: A list of relative paths of Markdown files that meet the size criteria and are not in excluded directories.

    The exclusion of directories works on a hierarchical basis. If a directory is listed in 'excluded_dirs',
    all its subdirectories are implicitly excluded as well. For example, if 'excluded_dirs' contains '/path/to/exclude',
    then '/path/to/exclude/subdir1' and '/path/to/exclude/subdir2' are also excluded.
    """
    if excluded_dirs is None:
        excluded_dirs = []
    return [
        f.relative_to(directory)
        for f in directory.rglob("*.md")
        if f.stat().st_size >= min_size  # and f.is_symlink() is False
        and all(
            directory / Path(excluded) not in f.parents for excluded in excluded_dirs
        )
    ]
