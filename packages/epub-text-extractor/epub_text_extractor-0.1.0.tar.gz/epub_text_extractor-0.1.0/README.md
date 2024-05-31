# EPUB to text

## Overview

`epub_to_text` is a Python package designed to extract content from EPUB files and export it in various formats such as text, JSON, and Markdown. This package can be used to feed content into AI models for summarization, knowledge base building, and other applications.

## Features

- Extracts content from EPUB files by chapters.
- Exports content as plain text, JSON, or Markdown.
- Handles creation of export directories.
- Provides a command-line interface (CLI) for easy usage.

## Installation

### Prerequisites

- Python 3.6 or higher

### Required Packages

The following packages are required:

- `ebooklib==0.17.1`
- `beautifulsoup4==4.9.3`
- `markdown==3.3.4`

### Installing the Package

You can install the package directly from PyPI:

```sh
pip install epub_to_text
```

## Usage

### Command-Line Interface (CLI)

The package provides a CLI for easy extraction and export of EPUB content. The command `epub-extract` can be used from the terminal.

### Basic Usage

Navigate to the directory containing your EPUB file and run:

```sh
epub-extract path_to_your_epub_file.epub --text --json --markdown