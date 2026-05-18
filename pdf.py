#!/usr/bin/env python3
"""PDF Multi-Tool: merge and split PDF files via CLI."""

import argparse
from pathlib import Path
import pypdf


def validate_pdf(path_str: str) -> pypdf.PdfReader | None:
    path = Path(path_str).resolve()
    if not path.exists():
        print(f"  [ERROR] File not found: {path}")
        return None
    if path.suffix.lower() != ".pdf":
        print(f"  [ERROR] Not a PDF file: {path.name}")
        return None
    try:
        reader = pypdf.PdfReader(str(path))
        print(f"  [OK] {path.name} ({len(reader.pages)} pages)")
        return reader
    except Exception as e:
        print(f"  [ERROR] Could not read {path.name}: {e}")
        return None


def merge_pdfs(readers: list, output_path: Path) -> None:
    writer = pypdf.PdfWriter()
    for reader in readers:
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"\nMerged PDF saved to: {output_path}")
    print(f"Total pages: {sum(len(r.pages) for r in readers)}")


# Split a PDF into one file per page
def split_pdf(reader: pypdf.PdfReader, output_dir: Path) -> None:
    # Create the output folder if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    total = len(reader.pages)

    # zfill() pads a number with leading zeros to a fixed width
    # so page 1 of 100 becomes "001" not "1" — sorts correctly in Finder
    width = len(str(total))

    for i, page in enumerate(reader.pages):
        # enumerate() gives us both the index (i) and the value (page)
        # i + 1 so pages start at 1 not 0
        page_number = str(i + 1).zfill(width)
        output_path = output_dir / f"page_{page_number}.pdf"

        # Each page gets its own writer
        writer = pypdf.PdfWriter()
        writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"  Saved: {output_path.name}")

    print(f"\nSplit complete. {total} pages saved to: {output_dir}")


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

    if args.command == "merge":
        print("Validating input files...")
        readers = []
        for path_str in args.inputs:
            reader = validate_pdf(path_str)
            if reader:
                readers.append(reader)

        if len(readers) < 2:
            print("\nNeed at least 2 valid PDF files to merge.")
            return

        output_path = Path(args.output).resolve()
        merge_pdfs(readers, output_path)

    elif args.command == "split":
        print("Validating input file...")
        reader = validate_pdf(args.input)
        if not reader:
            return

        # Resolve output dir and split
        output_dir = Path(args.output_dir).resolve()
        split_pdf(reader, output_dir)


if __name__ == "__main__":
    main()