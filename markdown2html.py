#!/usr/bin/python3
"""
Markdown to HTML converter script.

This script takes two arguments: the input Markdown file and the output HTML file.
It converts the Markdown content to HTML and writes it to the output file.
"""

import sys
import os

def markdown_to_html(markdown_text):
    import re
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
    paragraphs = [f"<p>{p}</p>" for p in paragraphs if not p.startswith('<h') and not p.startswith('<p>')]
    markdown_text = "\n\n".join(paragraphs)

    return markdown_text