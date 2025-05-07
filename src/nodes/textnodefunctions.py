from .textnode import TextType, TextNode
from .leafnode import LeafNode
import re



def text_node_to_html_node(text_node: TextNode):
    type = text_node.text_type
    match type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        delimited_text = node.text.split(delimiter)
        match delimiter:
            case '**':
                new_nodes.append(TextNode(delimited_text[0], TextType.TEXT))
                new_nodes.append(TextNode(delimited_text[1], TextType.BOLD))
                new_nodes.append(TextNode(delimited_text[2], TextType.TEXT))
            case '_':
                new_nodes.append(TextNode(delimited_text[0], TextType.TEXT))
                new_nodes.append(TextNode(delimited_text[1], TextType.ITALIC))
                new_nodes.append(TextNode(delimited_text[2], TextType.TEXT))
            case '`':
                new_nodes.append(TextNode(delimited_text[0], TextType.TEXT))
                new_nodes.append(TextNode(delimited_text[1], TextType.CODE))
                new_nodes.append(TextNode(delimited_text[2], TextType.TEXT))
            case _:
                new_nodes.append(TextNode(node.text, text_type))

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
    pattern = r'!\[(.*?)\]\((.*?)\)'

    for old_node in old_nodes:
        node: TextNode = old_node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = re.findall(pattern, node.text)

        if not links:
            new_nodes.append(node)
            continue

        remaining_text = old_node.text

        for text,url in links:
            parts = remaining_text.split(f"![{text}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
            new_nodes.append(TextNode(text,TextType.IMAGE,url))

            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
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
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))


    return new_nodes

def text_to_textnodes(text):
    nodes = []


    return nodes
