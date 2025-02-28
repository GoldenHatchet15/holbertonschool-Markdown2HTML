#!/usr/bin/python3
"""
Markdown to HTML converter script.

This script takes two arguments: the input Markdown file
and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.
"""

import sys
import os
import hashlib

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)

    with open(sys.argv[1]) as r:
        with open(sys.argv[2], 'w') as w:
            in_list = False
            in_ordered_list = False
            in_paragraph = False
            paragraph_lines = []

            for line in r:
                line = line.rstrip('\n')  # Remove trailing newline characters

                # Handle [[text]] to MD5 hash
                while '[[' in line:
                    start = line.index('[[')
                    end = line.index(']]', start + 2)
                    md5_content = line[start + 2:end]
                    md5_hash = hashlib.md5(md5_content.encode()).hexdigest()
                    line = line[:start] + md5_hash + line[end + 2:]

                # Handle ((text)) to remove 'c'
                while '((' in line:
                    start = line.index('((')
                    end = line.index('))', start + 2)
                    removed_c_content = (
                        line[start + 2:end].replace('c', '').replace('C', '')
                        )
                    line = line[:start] + removed_c_content + line[end + 2:]

                # Handle bold and emphasis
                while '**' in line or '__' in line:
                    if '**' in line:
                        start = line.index('**')
                        end = line.index('**', start + 2)
                        line = (line[:start] +
                                '<b>' + line[start + 2:end] +
                                '</b>' + line[end + 2:])
                    elif '__' in line:
                        start = line.index('__')
                        end = line.index('__', start + 2)
                        line = (line[:start] + '<em>' +
                                line[start + 2:end] +
                                '</em>' + line[end + 2:])

                length = len(line)
                headings = line.lstrip('#')
                heading_count = length - len(headings)
                unordered = line.lstrip('-')
                unordered_count = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_count = length - len(ordered)

                # Handle headings
                if 1 <= heading_count <= 6:
                    if in_paragraph:
                        # Write paragraph content with line breaks
                        paragraph_content = '\n'.join(paragraph_lines).strip()
                        w.write('<p>\n' + paragraph_content + '\n</p>\n')
                        in_paragraph = False
                        paragraph_lines = []
                    if in_list:
                        w.write('</ul>\n')
                        in_list = False
                    if in_ordered_list:
                        w.write('</ol>\n')
                        in_ordered_list = False
                    line = '<h{}>{}</h{}>'.format(
                        heading_count,
                        headings.strip(), heading_count)
                    w.write(line + '\n')
                    continue

                # Handle unordered lists
                if unordered_count:
                    if not in_list:
                        w.write('<ul>\n')
                        in_list = True
                    line = '<li>{}</li>'.format(unordered.strip())
                    w.write(line + '\n')
                    continue

                # Handle ordered lists
                if ordered_count:
                    if not in_ordered_list:
                        w.write('<ol>\n')
                        in_ordered_list = True
                    line = '<li>{}</li>'.format(ordered.strip())
                    w.write(line + '\n')
                    continue

                # Handle blank lines
                if length <= 1:  # Blank line
                    if in_paragraph:
                        # Write paragraph content with line breaks
                        paragraph_content = '\n'.join(paragraph_lines).strip()
                        w.write('<p>\n' + paragraph_content + '\n</p>\n')
                        in_paragraph = False
                        paragraph_lines = []
                    if in_list:
                        w.write('</ul>\n')
                        in_list = False
                    if in_ordered_list:
                        w.write('</ol>\n')
                        in_ordered_list = False
                    continue

                # Handle paragraphs
                if not (heading_count or in_list or in_ordered_list):
                    if not in_paragraph:
                        in_paragraph = True
                        paragraph_lines = []
                    # Append line with <br /> tags,
                    # but avoid adding <br /> at the end of paragraphs
                    if paragraph_lines:
                        line = '<br/>\n' + line
                    paragraph_lines.append(line)

            # Close any open tags
            if in_paragraph:
                paragraph_content = '\n'.join(paragraph_lines).strip()
                w.write('<p>\n' + paragraph_content + '\n</p>\n')
            if in_list:
                w.write('</ul>\n')
            if in_ordered_list:
                w.write('</ol>\n')

    exit(0)
