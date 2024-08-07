#!/usr/bin/python3
"""
    markdown2html.py: Converts markdown files to html files.
    Usage: markdown2html.py <inputfile.md> <outputfile.html>
"""

from sys import argv, exit, stderr
from os import path


def open_file(filename: str) -> str:
    """Opens a file and returns the text."""
    if not path.isfile(filename):
        raise FileNotFoundError(f'Missing {filename}')
    with open(filename, 'r') as f:
        text = f.read()
    return text


def markdown2html(inputfile: str, outputfile: str = None) -> None:
    """Converts markdown files to html files."""
    text = open_file(inputfile)


def main() -> None:
    """Main function starting the program"""
    try:
        if (len(argv) != 3):
            raise ValueError('Usage: ./markdown2html.py README.md README.html')
        markdown2html(argv[1], argv[2])
        exit(0)  # File converted successfully
    except ValueError as err:
        print(err, file=stderr)
        exit(1)  # Invalid arguments
    except FileNotFoundError as err:
        print(err, file=stderr)
        exit(1)  # File not found
    except Exception as err:
        print(err, file=stderr)
        exit(1)  # Unknown error occurred


if __name__ == '__main__':
    main()
