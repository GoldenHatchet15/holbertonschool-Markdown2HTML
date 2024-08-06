#!/usr/bin/python3
"""
Markdown to HTML converter script.

This script takes two arguments: the input Markdown file
and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.
"""

import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Read the Markdown file
        with open(input_file, 'r') as file:
            markdown_text = file.read()

        # Initialize variables
        html_text = ''
        change_status = False
        ordered_status = False
        paragraph = False

        # Regular expressions for matching Markdown syntax
        heading_regex = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)
        list_regex = re.compile(
            r'(^\s*-\s.*(?:\n\s*-\s.*)*)', re.MULTILINE | re.DOTALL)

        # Process each line of the Markdown text
        lines = markdown_text.splitlines(True)
        for line in lines:
            line = line.rstrip()  # Remove trailing whitespace

            # Check for headings
            heading_match = heading_regex.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2)
                html_text += f'<h{level}>{text}</h{level}>\n'
                continue

            # Check for unordered lists
            list_match = list_regex.match(line)
            if list_match:
                items = line.strip().split('\n')
                if not change_status:
                    html_text += '<ul>\n'
                    change_status = True
                for item in items:
                    html_text += f'<li>{item.strip()[2:]}</li>\n'
                continue

            # End of unordered list
            if change_status and not list_regex.match(line):
                html_text += '</ul>\n'
                change_status = False

            # Check for ordered lists (if needed in future)
            # ...

            # Check for paragraphs
            if not heading_match and not change_status:
                if not paragraph and line:
                    html_text += '<p>\n'
                    paragraph = True
                elif line:
                    html_text += '<br/>\n'
                elif paragraph:
                    html_text += '</p>\n'
                    paragraph = False

            # Add regular text
            if line:
                html_text += line + '\n'

        # Close any open tags
        if change_status:
            html_text += '</ul>\n'
        if paragraph:
            html_text += '</p>\n'

        # Ensure there is a newline at the end of the HTML text
        html_text = html_text.strip() + '\n'

        # Write HTML to the output file
        with open(output_file, 'w') as file:
            file.write(html_text)

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}")
        sys.exit(1)
