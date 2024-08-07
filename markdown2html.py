#!/usr/bin/python3
"""
    markdown2html.py: Converts markdown files to html files.
    Usage: markdown2html.py <inputfile.md> <outputfile.html>
"""

from sys import argv, exit, stderr
from typing import List
from os import path


def open_file(filename: str) -> str:
    """Opens a file and returns the text."""
    if not path.isfile(filename):
        raise FileNotFoundError(f'Missing {filename}')
    with open(filename, 'r') as f:
        text = f.readlines()
    return text


def save_file(filename: str, text: str) -> None:
    """Saves the text to a file."""
    if (not filename.endswith('.html')):
        filename += '.html'
    with open(filename, 'w') as f:
        f.write(text)


def get_heading_level(line: str) -> int:
    """Returns the heading level of a markdown heading."""
    level = 0
    for char in line:
        if char == '#':
            level += 1
        else:
            break
    return level


def heading(text: str, level: int) -> str:
    """Converts markdown headings to html headings."""
    # Strip removes leading and trailing whitespaces
    return f'<h{level}>{text.strip()}</h{level}>'


def convert(lines: List[str]) -> str:
    """Converts markdown to html."""

    html = []

    for line in lines:
        if (line.startswith('#')):
            level = get_heading_level(line)
            # level + 1 because markdown headings as space after the # symbol
            html.append(heading(line[level + 1:], level))

    return '\n'.join(html)


def markdown2html(inputfile: str, outputfile: str) -> None:
    """Converts markdown files to html files."""
    lines = open_file(inputfile)
    html_content = convert(lines)  # Convert markdown to html
    save_file(outputfile, html_content)


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
