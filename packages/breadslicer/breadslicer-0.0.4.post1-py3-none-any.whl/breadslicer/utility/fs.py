import os
from pathlib import Path
from typing import List


def remove_directory(path: Path) -> None:
    for p in path.iterdir():
        remove_paths([p])
    path.rmdir()


def remove_paths(paths: List[Path]) -> None:
    for path in paths:
        if path.exists():
            path.unlink() if path.is_file() else remove_directory(path)


def rename_path(src_path: Path, dst_path: Path) -> None:
    os.rename(src_path, dst_path)


def cwd(path: Path) -> None:
    os.chdir(path)
