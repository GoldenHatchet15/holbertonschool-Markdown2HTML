#!/usr/bin/python3
"""
Markdown to HTML converter script.

This script takes two arguments: the input Markdown file and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.
"""

import sys
import os
import re

def markdown_to_html(markdown_text):
    # Converting headers
    markdown_text = re.sub(r"(^|\n)###### (.*?)(\n|$)", r"\1<h6>\2</h6>\3", markdown_text)
    markdown_text = re.sub(r"(^|\n)##### (.*?)(\n|$)", r"\1<h5>\2</h5>\3", markdown_text)
    markdown_text = re.sub(r"(^|\n)#### (.*?)(\n|$)", r"\1<h4>\2</h4>\3", markdown_text)
    markdown_text = re.sub(r"(^|\n)### (.*?)(\n|$)", r"\1<h3>\2</h3>\3", markdown_text)
    markdown_text = re.sub(r"(^|\n)## (.*?)(\n|$)", r"\1<h2>\2</h2>\3", markdown_text)
    markdown_text = re.sub(r"(^|\n)# (.*?)(\n|$)", r"\1<h1>\2</h1>\3", markdown_text)

    # Converting bold text
    markdown_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", markdown_text)
    markdown_text = re.sub(r"__(.*?)__", r"<b>\1</b>", markdown_text)

    # Converting paragraphs
    paragraphs = markdown_text.split("\n\n")
    html_paragraphs = []
    for p in paragraphs:
        if not (p.startswith('<h') and p.endswith('>')):
            p = f"<p>{p}</p>"
        html_paragraphs.append(p)
    
    html_text = "\n\n".join(html_paragraphs)

    return html_text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r') as file:
            markdown_text = file.read()
            print(f"Markdown content:\n{markdown_text}")  # Debugging print
            html_text = markdown_to_html(markdown_text)
            print(f"HTML content:\n{html_text}")  # Debugging print
        
        with open(output_file, 'w') as file:
            file.write(html_text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
