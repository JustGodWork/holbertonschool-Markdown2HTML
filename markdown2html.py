#!/usr/bin/python3
"""
    markdown2html.py: Converts markdown files to html files.
    Usage: markdown2html.py <inputfile.md> <outputfile.html>
"""

from sys import argv, exit


def open_file(filename: str) -> str:
    """Opens a file and returns the text."""
    try:
        with open(filename, 'r') as f:
            text = f.read()
        return text
    except FileNotFoundError as err:
        print(f'Missing {filename}')
        raise err


def markdown2html(inputfile: str, outputfile: str = None) -> None:
    """Converts markdown files to html files."""
    text = open_file(inputfile)


def main() -> None:
    """Main function starting the program"""
    if (len(argv) != 3):
        print('Usage: ./markdown2html.py README.md README.html')
        exit(1)
    try:
        markdown2html(argv[1], argv[2])
    except FileNotFoundError:
        exit(1)
    exit(0)
    # markdown2html(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
