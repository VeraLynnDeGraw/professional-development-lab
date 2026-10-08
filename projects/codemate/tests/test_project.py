"""Tests for CODEMATE project inspection."""

from pathlib import Path

import pytest

from codemate.project import inspect_project


def test_inspect_project_finds_files(tmp_path: Path) -> None:
    """The inspector should discover files inside a project."""

    readme = tmp_path / "README.md"
    source = tmp_path / "main.py"

    readme.write_text("# Test Project\n", encoding="utf-8")
    source.write_text("print('hello')\n", encoding="utf-8")

    context = inspect_project(tmp_path)

    paths = {project_file.path for project_file in context.files}

    assert "README.md" in paths
    assert "main.py" in paths


def test_inspect_project_returns_absolute_root(tmp_path: Path) -> None:
    """The project context should contain the resolved project root."""

    context = inspect_project(tmp_path)

    assert context.root == str(tmp_path.resolve())


def test_inspect_project_rejects_missing_path(tmp_path: Path) -> None:
    """A missing project should produce a clear filesystem error."""

    missing = tmp_path / "does-not-exist"

    with pytest.raises(FileNotFoundError):
        inspect_project(missing)


def test_inspect_project_rejects_file(tmp_path: Path) -> None:
    """A file should not be accepted as a project directory."""

    file_path = tmp_path / "README.md"
    file_path.write_text("# Test\n", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        inspect_project(file_path)
