#!/usr/bin/env python3
"""PDF Multi-Tool: merge and split PDF files via CLI."""

import argparse
import logging
from pathlib import Path
import pypdf


# Configure logging to write to pdf_errors.log in the project folder
# This runs once when the script starts, before any functions are called
logging.basicConfig(
    filename="pdf_errors.log",       # where to write logs
    level=logging.DEBUG,             # minimum severity level to record
    format="%(asctime)s [%(levelname)s] %(message)s",  # timestamp + level + message
    datefmt="%Y-%m-%d %H:%M:%S"     # human readable timestamp format
)


def validate_pdf(path_str: str) -> pypdf.PdfReader | None:
    path = Path(path_str).resolve()

    if not path.exists():
        msg = f"File not found: {path}"
        print(f"  [ERROR] {msg}")
        logging.error(msg)           # Log the error to file
        return None

    if path.suffix.lower() != ".pdf":
        msg = f"Not a PDF file: {path.name}"
        print(f"  [ERROR] {msg}")
        logging.error(msg)
        return None

    try:
        reader = pypdf.PdfReader(str(path))
        logging.info(f"Opened successfully: {path.name} ({len(reader.pages)} pages)")
        print(f"  [OK] {path.name} ({len(reader.pages)} pages)")
        return reader
    except Exception as e:
        msg = f"Could not read {path.name}: {e}"
        print(f"  [ERROR] {msg}")
        logging.error(msg)           # Log the exception details
        return None


def merge_pdfs(readers: list, output_path: Path) -> None:
    writer = pypdf.PdfWriter()
    for reader in readers:
        for page in reader.pages:
            writer.add_page(page)
    try:
        with open(output_path, "wb") as f:
            writer.write(f)
        logging.info(f"Merge complete: {output_path}")
        print(f"\nMerged PDF saved to: {output_path}")
        print(f"Total pages: {sum(len(r.pages) for r in readers)}")
    except Exception as e:
        msg = f"Failed to write merged PDF: {e}"
        print(f"  [ERROR] {msg}")
        logging.error(msg)


def split_pdf(reader: pypdf.PdfReader, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    total = len(reader.pages)
    width = len(str(total))

    for i, page in enumerate(reader.pages):
        page_number = str(i + 1).zfill(width)
        output_path = output_dir / f"page_{page_number}.pdf"
        writer = pypdf.PdfWriter()
        writer.add_page(page)
        try:
            with open(output_path, "wb") as f:
                writer.write(f)
            print(f"  Saved: {output_path.name}")
        except Exception as e:
            msg = f"Failed to write {output_path.name}: {e}"
            print(f"  [ERROR] {msg}")
            logging.error(msg)

    logging.info(f"Split complete: {total} pages saved to {output_dir}")
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

        output_dir = Path(args.output_dir).resolve()
        split_pdf(reader, output_dir)


if __name__ == "__main__":
    main()