from .textnode import TextType, TextNode, Delimiter, delimiters_regex_match, delimiters_to_text_type
from .leafnode import LeafNode
import re



def text_node_to_html_node(text_node: TextNode):
    type = text_node.text_type
    match type:
        case TextType.TEXT:
            temp = text_node.text.replace('\n', ' ')
            return LeafNode(None, temp)
        case TextType.NORMAL:
            return LeafNode('p', text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception(f"Unknown text type, can't return a LeafNode: {text_node.text_type}")

def handle_delimited_text(delimited_text, text_type, delimiter, has_leading_delimiter):
    nodes = []

    switcher = has_leading_delimiter
    for text in delimited_text:
        if text!="":
            if switcher:
                nodes.append(TextNode(text, text_type))
            else:
                nodes.append(TextNode(text, TextType.TEXT))
            switcher = not switcher


    return nodes

def handle_bold(delimited_text, delimiter, text_type, has_leading_delimiter):
    return handle_delimited_text(delimited_text, text_type, delimiter, has_leading_delimiter)
def handle_italic(delimited_text, delimiter, text_type, has_leading_delimiter):
    return handle_delimited_text(delimited_text, text_type, delimiter, has_leading_delimiter)
def handle_code(delimited_text, delimiter, text_type, has_leading_delimiter):
    return handle_delimited_text(delimited_text, text_type, delimiter, has_leading_delimiter)

delimiter_handlers = {
    Delimiter.BOLD: handle_bold,
    Delimiter.ITALIC: handle_italic,
    Delimiter.CODE: handle_code,
}

def split_nodes_delimiter(old_nodes, delimiter: Delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if re.search(delimiters_regex_match[delimiter], node.text) and node.text_type == TextType.TEXT:
            delimited_text = node.text.split(delimiter.value[0])
            handler = delimiter_handlers.get(delimiter)
            if handler:
                new_nodes.extend(handler(delimited_text, delimiter, text_type, node.text.startswith(delimiter.value)))
            else:
                new_nodes.append(TextNode(node.text, text_type))
        else:
            new_nodes.append(TextNode(node.text,node.text_type))


    return new_nodes


def extract_markdown_images(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_images(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for text, url in links:
            parts = remaining_text.split(f"![{text}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))

            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
            links = extract_markdown_links(remaining_text)
            if not links:
                split_nodes_image([TextNode(remaining_text, TextType.TEXT)])
            else:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))


    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for text, url in links:
            parts = remaining_text.split(f"[{text}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))

            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
            links = extract_markdown_links(remaining_text)
            if not links:
                split_nodes_link([TextNode(remaining_text, TextType.TEXT)])
            else:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))


    return new_nodes

def text_to_textnodes(text):
    nodes = []
    if text != '':
        nodes.append(TextNode(text, TextType.TEXT))

        for delimiter, text_type in delimiters_to_text_type.items():
            nodes = split_nodes_delimiter(nodes, delimiter,text_type)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
    return nodes
