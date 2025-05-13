from enum import Enum
from src.nodes.htmlnode import HTMLNode
import re


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
    return text

def text_to_children(text):
    return text

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # create html parrent node

    for block in blocks:
       node = HTMLNode(blocks_to_html_tag[block_to_block_type(block)], block, None, None)
