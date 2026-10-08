"""Tests for the CODEMATE command-line interface."""

from pathlib import Path

from codemate.cli import main


def test_inspect_command_succeeds(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    """The inspect command should inspect a valid project."""

    readme = tmp_path / "README.md"
    readme.write_text("# Test Project\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["codemate", "inspect", str(tmp_path)],
    )

    exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "CODEMATE — Project Inspection" in captured.out
    assert "README.md" in captured.out
    assert "Total files: 1" in captured.out


def test_inspect_command_rejects_missing_project(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """The inspect command should reject a missing project."""

    missing = tmp_path / "does-not-exist"

    monkeypatch.setattr(
        "sys.argv",
        ["codemate", "inspect", str(missing)],
    )

    try:
        main()
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("Expected argparse to exit with status 2")


def test_inspect_command_rejects_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """The inspect command should reject a file as a project."""

    file_path = tmp_path / "README.md"
    file_path.write_text("# Test\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["codemate", "inspect", str(file_path)],
    )

    try:
        main()
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("Expected argparse to exit with status 2")
