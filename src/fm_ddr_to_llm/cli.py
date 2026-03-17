"""CLI entrypoint for fm-ddr-to-llm."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import run_pipeline, save_output


def _is_interactive() -> bool:
    """Check if stdin is a terminal (not piped/redirected)."""
    return sys.stdin.isatty()


def _ensure_ddrparser() -> bool:
    """Check for DDRParser; offer to install if missing and interactive.

    Returns True if DDRParser is available (was found or just installed).
    """
    from .ddrparser import check_ddrparser, download_and_install

    found, message = check_ddrparser()
    if found:
        return True

    if not _is_interactive():
        print(f"Error: {message}", file=sys.stderr)
        return False

    # Interactive: offer to install right now
    success, install_msg = download_and_install(interactive=True)
    print(install_msg)

    if not success:
        return False

    # Verify it actually works now
    found, _ = check_ddrparser()
    return found


def _cmd_check_prereqs(argv: list[str]) -> int:
    """Check for required prerequisites."""
    parser = argparse.ArgumentParser(
        prog="fm-ddr-to-llm check-prereqs",
        description="Check for required prerequisites (DDRParser).",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Download and install missing prerequisites",
    )
    args = parser.parse_args(argv)

    from .ddrparser import check_ddrparser, download_and_install

    found, message = check_ddrparser(verbose=True)
    print(message)

    if found:
        return 0

    if args.install or _is_interactive():
        success, install_msg = download_and_install(interactive=not args.install)
        print(install_msg)
        return 0 if success else 1

    return 1


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Route subcommands before argparse sees them
    if argv and argv[0] == "check-prereqs":
        return _cmd_check_prereqs(argv[1:])

    parser = argparse.ArgumentParser(
        prog="fm-ddr-to-llm",
        description="Convert FileMaker DDR XML to structured, cross-referenced output for LLM consumption.",
    )
    parser.add_argument(
        "ddr_xml",
        type=Path,
        help="Path to the FileMaker DDR XML file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSON file path (default: <input-stem>-llm.json)",
    )

    args = parser.parse_args(argv)

    if not args.ddr_xml.exists():
        print(f"Error: DDR XML file not found: {args.ddr_xml}", file=sys.stderr)
        return 1

    if not _ensure_ddrparser():
        return 1

    output_path = args.output or args.ddr_xml.with_name(
        args.ddr_xml.stem + "-llm.json"
    )

    print(f"Processing: {args.ddr_xml}")
    result = run_pipeline(args.ddr_xml)

    summary = result.to_dict()["summary"]
    print(f"Extracted {summary['total_objects']} objects, {summary['total_cross_references']} cross-references")
    for type_name, count in sorted(summary["objects_by_type"].items()):
        print(f"  {type_name}: {count}")

    save_output(result, output_path)
    print(f"Output saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
