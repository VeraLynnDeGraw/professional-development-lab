"""Project inspection utilities for CODEMATE."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_IGNORED_DIRECTORIES = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
    }
)

DEFAULT_IGNORED_SUFFIXES = frozenset(
    {
        ".egg-info",
    }
)


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


def _should_ignore(path: Path) -> bool:
    """Return whether a path belongs to an ignored project artifact."""

    if any(part in DEFAULT_IGNORED_DIRECTORIES for part in path.parts):
        return True

    if any(
        part.endswith(suffix)
        for part in path.parts
        for suffix in DEFAULT_IGNORED_SUFFIXES
    ):
        return True

    return False


def inspect_project(project_path: str | Path) -> ProjectContext:
    """
    Inspect a project directory and return structured file information.

    The inspector only reads filesystem metadata. It does not modify files.
    Known generated, environment, cache, and repository metadata directories
    are excluded from the inspection.
    """

    root = Path(project_path).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Project does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {root}")

    discovered_files: list[ProjectFile] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or _should_ignore(path):
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
