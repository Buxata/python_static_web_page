import os
import re
from nodes.blockfunctions import markdown_to_html_node

TITLE_REGEX = re.compile(r"^#\s?(.*)$", re.MULTILINE)

def extract_title(markdown):
    match = TITLE_REGEX.search(markdown)
    if match and not match.group(1).startswith('#'):
        return match.group(1).strip()
    else:
        raise Exception("No title's found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    markdown = open(from_path, "r", encoding="utf-8")
    template = open(template_path, "r", encoding="utf-8")
    html_node = markdown_to_html_node(markdown.read())

    return markdown,template, html_node
