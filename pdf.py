#!/usr/bin/env python3
"""PDF Multi-Tool: merge and split PDF files via CLI."""

import argparse
from pathlib import Path
import pypdf


# Validate a single PDF file and return a PdfReader if valid, None if not
def validate_pdf(path_str: str) -> pypdf.PdfReader | None:
    path = Path(path_str).resolve()

    # File must exist
    if not path.exists():
        print(f"  [ERROR] File not found: {path}")
        return None

    # Must be a .pdf extension
    if path.suffix.lower() != ".pdf":
        print(f"  [ERROR] Not a PDF file: {path.name}")
        return None

    # Try opening it. Catches corrupted or invalid PDFs
    try:
        reader = pypdf.PdfReader(str(path))
        print(f"  [OK] {path.name} ({len(reader.pages)} pages)")
        return reader
    except Exception as e:
        print(f"  [ERROR] Could not read {path.name}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="PDF Multi-Tool: merge and split PDF files."
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs into one")
    merge_parser.add_argument("inputs", nargs="+", help="PDF files to merge")
    merge_parser.add_argument("--output", default="merged.pdf", help="Output filename")

    split_parser = subparsers.add_parser("split", help="Split a PDF into individual pages")
    split_parser.add_argument("input", help="PDF file to split")
    split_parser.add_argument("--output-dir", default="split_output", help="Folder to save pages in")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Validate inputs depending on which subcommand was chosen
    if args.command == "merge":
        print("Validating input files...")
        readers = []
        for path_str in args.inputs:
            reader = validate_pdf(path_str)
            if reader:
                readers.append(reader)

        print(f"\n{len(readers)} of {len(args.inputs)} files valid.")

    elif args.command == "split":
        print("Validating input file...")
        reader = validate_pdf(args.input)
        if not reader:
            return
        print(f"\nReady to split {len(reader.pages)} pages.")


if __name__ == "__main__":
    main()