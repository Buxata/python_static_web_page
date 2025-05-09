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
    pattern = r'\[(.*?)\]\((.*?)\)'

    for node in old_nodes:
        temp = re.findall(pattern, node.text)
        print(''.join(temp))

    return new_nodes

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        print(f'Node loop: \n{node}\n' )
        temp = re.findall(pattern, node.text)
        for member in temp:
            print(member[0])
            print(member[1])
        print()

        opposite = re.findall("^"+pattern, node.text)
        for member in opposite:
            print(member)
        print()

        # print(''.join(temp))
        new_nodes.append(temp)

    return new_nodes
