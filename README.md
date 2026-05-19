# PDF Multi-Tool

Merge and split PDF files via the command line. Errors from corrupted or invalid files are logged to `pdf_errors.log`.

## Setup

```bash
pip3 install pypdf
```

## Usage

### Merge

Combine multiple PDF files into one:

```bash
python3 pdf.py merge file1.pdf file2.pdf
python3 pdf.py merge file1.pdf file2.pdf file3.pdf --output result.pdf
```

| Argument | Description |
|---|---|
| `file1.pdf file2.pdf ...` | Two or more PDF files to merge |
| `--output` | Output filename (default: `merged.pdf`) |

### Split

Split a PDF into one file per page:

```bash
python3 pdf.py split file.pdf
python3 pdf.py split file.pdf --output-dir ~/Desktop/pages
```

| Argument | Description |
|---|---|
| `file.pdf` | PDF file to split |
| `--output-dir` | Folder to save pages in (default: `split_output`) |

## Example

```
python3 pdf.py merge ~/Desktop/invoice.pdf ~/Desktop/contract.pdf --output ~/Desktop/combined.pdf

  [OK] invoice.pdf (3 pages)
  [OK] contract.pdf (5 pages)

Merged PDF saved to: /Users/andrea/Desktop/combined.pdf
Total pages: 8
```

## Error logging

Any corrupted or unreadable files are logged to `pdf_errors.log` in the project folder with a timestamp:

```
2026-05-18 10:00:00 [ERROR] File not found: fakefile.pdf
2026-05-18 10:01:00 [ERROR] Could not read corrupted.pdf: EOF marker not found
```

## Notes

- `pdf_errors.log` is excluded from this repo
- `split_output/` and `merged.pdf` are excluded from this repo
- Watermark, encrypt, and page range extraction coming soon
