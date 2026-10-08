"""Project inspection utilities for CODEMATE."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectFile:
    """Describe a file discovered inside a project."""

    path: str
    size: int


@dataclass(frozen=True)
class ProjectContext:
    """Structured information discovered about a project."""

    root: str
    files: tuple[ProjectFile, ...]


def inspect_project(project_path: str | Path) -> ProjectContext:
    """
    Inspect a project directory and return structured file information.

    The inspector only reads filesystem metadata. It does not modify files.
    """

    root = Path(project_path).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Project does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {root}")

    discovered_files: list[ProjectFile] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        try:
            relative_path = path.relative_to(root)
            size = path.stat().st_size
        except OSError:
            continue

        discovered_files.append(
            ProjectFile(
                path=str(relative_path),
                size=size,
            )
        )

    return ProjectContext(
        root=str(root),
        files=tuple(discovered_files),
    )
