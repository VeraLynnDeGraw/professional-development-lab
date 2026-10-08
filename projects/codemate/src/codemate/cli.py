"""Command-line interface for CODEMATE."""

from __future__ import annotations

import argparse

from codemate.project import inspect_project


def build_parser() -> argparse.ArgumentParser:
    """Build the CODEMATE command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="codemate",
        description="A human-controlled AI developer assistant.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect a software project.",
    )

    inspect_parser.add_argument(
        "path",
        help="Path to the project directory.",
    )

    return parser


def main() -> int:
    """Run the CODEMATE command-line interface."""

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "inspect":
        try:
            context = inspect_project(args.path)
        except (FileNotFoundError, NotADirectoryError) as error:
            parser.error(str(error))

        print("CODEMATE — Project Inspection")
        print()
        print(f"Project: {context.root}")
        print()
        print("Files:")

        if context.files:
            for project_file in context.files:
                print(f"  {project_file.path} ({project_file.size} bytes)")
        else:
            print("  No files discovered.")

        print()
        print(f"Total files: {len(context.files)}")
        print()
        print("Evidence:")
        print("  OBSERVED")
        print(f"    {len(context.files)} files discovered")
        print("  INFERRED")
        print("    None")
        print("  PROPOSED")
        print("    None")
        print("  UNKNOWN")
        print("    Project purpose has not yet been analyzed.")

        return 0

    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
