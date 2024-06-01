"""
Utility code for managing projects.
"""

# pyright: basic
import os
import sys
from pathlib import Path

__all__ = ["here", "project_root", "setup_project_dir"]

_initialized: bool = False
_root_dir: Path


def setup_project_dir():
    global _root_dir, _initialized
    if _initialized:
        return

    cur = Path.cwd()
    while cur.parent and not (cur / ".git").exists():
        cur = cur.parent

    if (cur / ".git").exists():
        _root_dir = cur
    else:
        raise RuntimeError("cannot find project root directory")
    sys.path.insert(0, os.fspath(_root_dir))
    _initialized = True


def project_root() -> Path:
    "Get the project root directory."
    setup_project_dir()
    return _root_dir


def here(path: str) -> Path:
    """
    Resolve a project-relative path to the current working direcetory.
    """
    setup_project_dir()
    apath = _root_dir / path
    return apath
