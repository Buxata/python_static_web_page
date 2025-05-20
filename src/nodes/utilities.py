import os
import re
from nodes.blockfunctions import markdown_to_html_node

TITLE_REGEX = re.compile(r"^#\s?(.*)$", re.MULTILINE)

def extract_title(markdown):
    match = TITLE_REGEX.search(markdown)
    if match and not match.group(1).startswith('#'):
        return match.group(1).strip()
    else:
        raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    markdown_file = open(from_path, "r", encoding="utf-8").read()
    template_file = open(template_path, "r", encoding="utf-8").read()
    html_node = markdown_to_html_node(markdown_file)
    title = extract_title(markdown_file)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html_node.to_html())
    destination_dir = '/'.join(dest_path.split('/')[:-1])
    print(destination_dir)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    destination_file = open(dest_path,"w",encoding="utf-8")
    destination_file.write(template_file)

    return template_file

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    directory = os.scandir(dir_path_content)
    for entry in directory:
        if entry.is_file():
            print(f"this is a file {entry.name}")
            input_file_name = dir_path_content+ "/" + entry.name
            output_file_name = dest_dir_path + "/" + entry.name.split('.')[0] + ".html"
            generate_page(input_file_name, template_path, output_file_name)
        else:
            print(f"this is a directory {entry.name} ")
            input_files_directory = dir_path_content+ "/" + entry.name
            output_files_directory = dest_dir_path + "/" + entry.name
            generate_pages_recursive(input_files_directory, template_path, output_files_directory)
    return "Something"
