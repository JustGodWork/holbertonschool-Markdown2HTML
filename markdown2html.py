#!/usr/bin/python3


"""
    markdown2html.py: Converts markdown files to html files.
    Usage: markdown2html.py <inputfile.md> <outputfile.html>
"""

from sys import argv, exit, stderr, stdout
from typing import List, Tuple
from os import path


debug_state = False  # Set to True to enable debug information


def debug(*args, **kwargs) -> None:
    """Prints debug information."""

    if debug_state:
        stdout.write('\033[91mDEBUG: \033[96m')
        print(*args, **kwargs)
        stdout.write('\033[0m')


def open_file(filename: str) -> str:
    """Opens a file and returns the text."""

    if not path.isfile(filename):
        raise FileNotFoundError(f'Missing {filename}')
    with open(filename, 'r') as f:
        text = f.readlines()
        debug(f'Opened {filename} with {len(text)} lines')
    return text


def save_file(filename: str, text: str) -> None:
    """Saves the text to a file."""

    if (not filename.endswith('.html')):
        filename += '.html'

    with open(filename, 'w') as f:
        f.write(text)


def is_markdown(line: str) -> bool:
    """Checks if a line is a markdown line."""

    return (
        line.startswith('#')
        or line.startswith('- ')
        or line.startswith('* ')
    )


def get_heading_level(line: str) -> int:
    """Returns the heading level of a markdown heading."""

    level = 0
    for char in line:
        if char == '#':
            level += 1
        else:
            break

    return level


def heading(line: str) -> str:
    """Converts markdown headings to html headings."""

    # level + 1 because markdown headings as space after the # symbol
    level = get_heading_level(line)
    # Strip removes leading and trailing whitespaces
    heading_content = line[level + 1:]
    debug(f'Converting \'{heading_content}\' to heading level {level}')
    return f'<h{level}>{heading_content}</h{level}>'


def list_item(lines: List[str], index: int,
              prefix: str, list_type: str) -> Tuple[int, List[str]]:
    """Converts markdown unordered lists to html unordered lists."""

    html = [f'<{list_type}>']

    for i in range(index, len(lines)):
        line = lines[i].strip()

        if (line.startswith(prefix)):
            li_content = line[2:]
            debug(f'Converting \'{li_content}\' to \'{list_type}\' list item')
            html.append(f'<li>{li_content}</li>')
            index += 1
        else:
            break
    html.append(f'</{list_type}>')
    return index, html


def paragraph(lines: List[str], index: int) -> Tuple[
    int,
    str
]:
    """Converts markdown paragraphs to html paragraphs."""

    original_index = index
    html = []

    for i in range(index, len(lines)):
        line = lines[i].strip()

        if (line == '' or is_markdown(line)):
            break
        else:
            debug(f'Converting \'{line}\' to paragraph')
            html.append(line)
            index += 1
            debug(f'Index is now {index}, original index is {original_index}')

    html_body = '\n<br/>\n'.join(html)
    html_text = f"<p>\n{html_body}\n</p>"

    if (index != original_index):
        debug(
            f'Converted paragraph at index {original_index},\
 incrementing index to {index}'
        )
        return index, html_text

    return original_index + 1, None


def convert(lines: List[str]) -> str:
    """Converts markdown to html."""

    html: List[str] = []
    index = 0

    debug(f'Converting {len(lines)} lines of markdown to html')

    # We use a while loop instead of a for loop because we need to skip lines
    while (index < len(lines)):
        line = lines[index].strip()  # Get the current line as a variable

        if (line.startswith('#')):
            debug(f'{line} is a heading')
            html.append(heading(line))
            index += 1  # Go to the next line
            continue

        is_ul_item = line.startswith('- ')
        is_ol_item = line.startswith('* ')

        if (is_ul_item or is_ol_item):
            debug(f'{line} is a list (ul/ol) item')
            # We need to update the index with the new value
            index, html_list = list_item(
                lines, index, '- ' if (is_ul_item) else '* ',
                'ul' if (is_ul_item) else 'ol'
            )
            html.extend(html_list)
            continue

        # In case the line does not match above conditions
        index, html_paragraph = paragraph(lines, index)
        html_paragraph and html.append(html_paragraph)

    return '\n'.join(html)


def markdown2html(inputfile: str, outputfile: str) -> None:
    """Converts markdown files to html files."""

    lines = open_file(inputfile)
    html_content = convert(lines)  # Convert markdown to html
    save_file(outputfile, html_content)  # Save the html content to a html file


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
