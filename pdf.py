#!/usr/bin/env python3
"""PDF Multi-Tool: merge and split PDF files via CLI."""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="PDF Multi-Tool: merge and split PDF files."
    )

    # Subparsers let you define separate modes, each with their own arguments.
    # dest="command" means the chosen subcommand is stored in args.command
    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to run"
    )

    # "merge" subcommand
    # nargs="+" means one or more values. You can pass as many PDFs as you want
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs into one")
    merge_parser.add_argument(
        "inputs",
        nargs="+",
        help="PDF files to merge"
    )
    merge_parser.add_argument(
        "--output",
        default="merged.pdf",
        help="Output filename (default: merged.pdf)"
    )

    # "split" subcommand
    split_parser = subparsers.add_parser("split", help="Split a PDF into individual pages")
    split_parser.add_argument(
        "input",
        help="PDF file to split"
    )
    split_parser.add_argument(
        "--output-dir",
        default="split_output",
        help="Folder to save pages in (default: split_output)"
    )

    args = parser.parse_args()

    # Print help if no subcommand was given
    if not args.command:
        parser.print_help()
        return

    # Temporary: confirm subcommand was received
    print(f"Command: {args.command}")
    print(f"Args: {args}")


if __name__ == "__main__":
    main()