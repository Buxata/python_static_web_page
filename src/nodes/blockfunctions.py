from enum import Enum
from nodes.textnode import TextNode, TextType
from src.nodes.htmlnode import HTMLNode
from src.nodes.textnodefunctions import text_node_to_html_node
import re
from wave import Error


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

blocks_regex_match = {
    BlockType.HEADING: r'^#+',
    BlockType.CODE: r"\`\`\`[\s\S]*?\`\`\`",
    BlockType.QUOTE: r'^>',
    BlockType.UNORDERED_LIST: r"^(?:\s*[-*+]\s+.+\n?)+$",
    BlockType.ORDERED_LIST: r"^(?:\s*\d+\.\s+.+\n?)+$",
}

blocks_to_html_tag = {
    BlockType.HEADING: "h",
    BlockType.CODE: "pre",
    BlockType.QUOTE: "blockquote",
    BlockType.UNORDERED_LIST: "ul",
    BlockType.ORDERED_LIST: "ol",
}

def is_valid_ordered_list(text):
    # Match all ordered list lines
    pattern = r"^\s*(\d+)\.\s+.+$"
    matches = re.findall(pattern, text, re.MULTILINE)

    if not matches:
        return False

    numbers = list(map(int, matches))
    return numbers == list(range(1, len(numbers) + 1))

def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip('\n'), markdown.split('\n\n')))

def check_heading_lvl (text):
    temp = 0
    while text[temp] != '#':
        temp+=1
    return str(temp+1)

def block_to_block_type(block):
    if re.match(blocks_regex_match[BlockType.HEADING], block):
        return BlockType.HEADING
    if re.match(blocks_regex_match[BlockType.CODE], block):
        return BlockType.CODE
    if re.match(blocks_regex_match[BlockType.QUOTE], block):
        return BlockType.QUOTE
    if re.match(blocks_regex_match[BlockType.UNORDERED_LIST], block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    if is_valid_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def handle_heading(text):
    text_node_to_html_node

def handle_quote(text):
    text_node_to_html_node

def handle_unordered_list(text):
    text_node_to_html_node

def handle_ordered_list(text):
    text_node_to_html_node

block_handlers = {
    BlockType.HEADING: handle_heading,
    BlockType.QUOTE: handle_quote,
    BlockType.UNORDERED_LIST: handle_unordered_list,
    BlockType.ORDERED_LIST: handle_ordered_list,
}

def text_to_children(text):
    if text == None:
        raise ValueError("Text cannot be None")
    handler = block_handlers.get(block_to_block_type(text))
    if handler:
        return handler(text)
    else:
        return [TextNode(text, TextType.TEXT)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # create html parrent node

    nodes = []

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                nodes.append(HTMLNode('h'+check_heading_lvl(block), '', text_to_children(block)))
            case BlockType.CODE:
                nodes.append(HTMLNode('pre', block))
            case BlockType.QUOTE:
                nodes.append(HTMLNode('blockquote', block))
            case BlockType.UNORDERED_LIST:
                nodes.append(HTMLNode('ul', block))
            case BlockType.ORDERED_LIST:
                nodes.append(HTMLNode('ol', block))
            case BlockType.PARAGRAPH:
                nodes.append(HTMLNode('p', block))
