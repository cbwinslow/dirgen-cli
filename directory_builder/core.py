# directory_builder/core.py
import os
from pathlib import Path


class DirectoryBuilderError(Exception):
    """Base exception for directory builder errors."""

    pass


def create_structure(base_path, structure, overwrite=False, dry_run=False):
    """
    Recursively create a project structure from a list.

    Args:
        base_path (Path): Base directory to create structure in.
        structure (list): List representing file/folder hierarchy.
        overwrite (bool): Whether to overwrite existing files.
        dry_run (bool): If True, only log actions without making changes.

    Raises:
        DirectoryBuilderError: If any unexpected error occurs.
    """
    try:
        for item in structure:
            if isinstance(item, str):
                target = Path(base_path) / item
                # If item has a '.' we assume it's a file, otherwise a folder
                if "." in item:
                    # File
                    if target.exists() and not overwrite:
                        # Skip if file exists and overwrite=False
                        continue
                    if dry_run:
                        print(f"[Dry Run] Would create file: {target}")
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.touch()
                else:
                    # Directory
                    if dry_run:
                        print(f"[Dry Run] Would create folder: {target}")
                    else:
                        target.mkdir(parents=True, exist_ok=True)
            elif isinstance(item, dict):
                # Key is folder name, value is a nested list structure
                for key, value in item.items():
                    sub_path = Path(base_path) / key
                    if dry_run:
                        print(f"[Dry Run] Would create folder: {sub_path}")
                    else:
                        sub_path.mkdir(parents=True, exist_ok=True)
                    create_structure(
                        sub_path, value, overwrite=overwrite, dry_run=dry_run
                    )
    except PermissionError as pe:
        raise DirectoryBuilderError(
            f"Permission denied: {pe}. Try using a directory in your home folder."
        )
    except Exception as e:
        raise DirectoryBuilderError(f"Unexpected error while building structure: {e}")


def flatten_structure(structure, prefix=""):
    """
    Flatten the structure into a list of relative paths.
    """
    result = []
    for item in structure:
        if isinstance(item, str):
            result.append(str(Path(prefix) / item))
        elif isinstance(item, dict):
            for key, subitems in item.items():
                result.append(str(Path(prefix) / key))
                result.extend(flatten_structure(subitems, prefix=Path(prefix) / key))
    return result


def diff_structure(base_path, structure):
    """
    Generate a diff between the desired structure and actual file system.

    Returns:
        missing_paths (list): Paths that would be created
        extra_paths (list): Paths that exist but aren't defined in the structure
    """
    desired = set(flatten_structure(structure))
    actual = set(p.relative_to(base_path).as_posix() for p in base_path.rglob("*"))

    missing = desired - actual
    extra = actual - desired
    return sorted(missing), sorted(extra)
