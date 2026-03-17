"""CLI entrypoint for fm-ddr-to-llm."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import run_pipeline, save_output


def main(argv: list[str] | None = None) -> int:
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
