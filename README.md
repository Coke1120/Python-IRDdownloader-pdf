# Document Link Downloader

A Python script that extracts and downloads linked files from Microsoft Word documents (.docx).

## Features

- Extracts all hyperlinks from Word documents
- Downloads linked files to a specified directory
- Shows download progress with progress bars
- Lists files in the working directory
- Handles various types of hyperlinks in Word documents

## Requirements

    pip install python-docx requests tqdm

## Usage

1. Run the script:

   python pdf_downloader.py

2. Enter the path to your DOCX file when prompted

3. Specify an output directory (or press Enter to use the default 'downloaded_pdfs' directory)

The script will:

- Show all files in the current directory
- List all links found in the document
- Download the linked files
- Show progress for each download

## Notes

- The script will create the output directory if it doesn't exist
- Duplicate links are automatically removed
- Failed downloads are logged with error messages
