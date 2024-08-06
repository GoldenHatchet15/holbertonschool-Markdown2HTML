#!/usr/bin/python3
"""
Markdown to HTML converter script.

This script takes two arguments: the input Markdown file
and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.
"""

import re
import sys


def markdown_to_html(markdown_text):
    """Convert Markdown text to HTML."""

    # Regular expressions to match Markdown headings and unordered lists
    heading_regex = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)
    list_regex = (
        re.compile(r'(^\s*-\s.*(?:\n\s*-\s.*)*)', re.MULTILINE | re.DOTALL)
    )

    def replace_heading(match):
        """Convert Markdown heading to HTML."""
        level = len(match.group(1))
        text = match.group(2)
        return f'<h{level}>{text}</h{level}>'

    def replace_list(match):
        """Convert Markdown unordered list to HTML."""
        items = match.group(0).strip().split('\n')
        html_list = (
            '<ul>\n' +
            '\n'.join(f'    <li>{item.strip()[2:]}</li>' for item in items) +
            '\n</ul>'
        )
        return html_list

    # Replace unordered lists first
    markdown_text = list_regex.sub(replace_list, markdown_text)

    # Replace headings
    html_text = heading_regex.sub(replace_heading, markdown_text)

    # Ensure there is a newline at the end of the HTML text
    return html_text.strip() + '\n'


def main(input_file, output_file):
    """Read Markdown file, convert to HTML, and write to output file."""
    try:
        # Read the Markdown file
        with open(input_file, 'r') as file:
            markdown_text = file.read()

        # Convert Markdown to HTML
        html_text = markdown_to_html(markdown_text)

        # Write HTML to the output file with a newline at the end
        with open(output_file, 'w') as file:
            file.write(html_text)

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
