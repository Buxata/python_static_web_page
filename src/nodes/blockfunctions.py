from enum import Enum
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode
from nodes.textnodefunctions import text_node_to_html_node, text_to_textnodes
import re
import warnings


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



def check_heading_lvl(text):
    # Count the number of # symbols at the beginning of the text
    count = 0
    for char in text:
        if char == '#':
            count+=1
        else:
            return str(count)
    return ''

def block_to_block_type(block):
    if block == '':
        return None
    if re.match(blocks_regex_match[BlockType.HEADING], block):
        # print("heading")
        return BlockType.HEADING
    if re.match(blocks_regex_match[BlockType.CODE], block):
        # print("code")
        return BlockType.CODE
    if re.match(blocks_regex_match[BlockType.QUOTE], block):
        # print("quote")
        return BlockType.QUOTE
    if re.match(blocks_regex_match[BlockType.UNORDERED_LIST], block, re.MULTILINE):
        # print("unordered_list")
        return BlockType.UNORDERED_LIST
    if is_valid_ordered_list(block):
        # print("ordered_list")
        return BlockType.ORDERED_LIST
    # print("paragraph")
    return BlockType.PARAGRAPH

def handle_code(text):
    temp = text.strip('```').lstrip('\n')
    return [LeafNode('code', temp)]

def handle_heading(text):
    clean_text = re.sub(r'^#+\s*', '', text)
    children = text_to_textnodes(clean_text)
    return list(map(text_node_to_html_node, children))

def handle_quote(text):
    lines = list(map(lambda x: x.strip(),text.strip("> ").split('\n>')))
    children = text_to_textnodes('<br>'.join(lines))
    return list(map(text_node_to_html_node, children))

def handle_unordered_list(text):
    nodes = []

    bullets = text.split('\n')
    for bullet in bullets:
        # Remove the bullet marker (- ) from the text
        clean_bullet = re.sub(r'^\s*[-*+]\s+', '', bullet)
        children = text_to_textnodes(clean_bullet)
        if bullet.strip():
            nodes.append(ParentNode('li', list(map(text_node_to_html_node, children))))
    return nodes

def handle_ordered_list(text):
    nodes = []

    items = text.split('\n')
    for item in items:
        # Remove the number prefix (1., 2., etc.) from the text
        clean_item = re.sub(r'^\s*\d+\.\s+', '', item)
        children = text_to_textnodes(clean_item)
        if item.strip():
            nodes.append(ParentNode('li', list(map(text_node_to_html_node, children))))
    return nodes


block_handlers = {
    BlockType.CODE: handle_code,
    BlockType.HEADING: handle_heading,
    BlockType.QUOTE: handle_quote,
    BlockType.UNORDERED_LIST: handle_unordered_list,
    BlockType.ORDERED_LIST: handle_ordered_list,
    None:None
}

def text_to_children(text):
    if text == None:
        raise ValueError("Text cannot be None")
    handler = block_handlers.get(block_to_block_type(text))
    if handler:
        return handler(text)
    else:
        nodes = text_to_textnodes(text)
        htmlnodes = list(map(text_node_to_html_node, nodes))
        return htmlnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                nodes.append(ParentNode('h'+check_heading_lvl(block), text_to_children(block)))
            case BlockType.CODE:
                nodes.append(ParentNode('pre',text_to_children(block)))
            case BlockType.QUOTE:
                nodes.append(ParentNode('blockquote',text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                nodes.append(ParentNode('ul', text_to_children(block)))
            case BlockType.ORDERED_LIST:
                nodes.append(ParentNode('ol', text_to_children(block)))
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode('p', text_to_children(block)))
            case _:
                warnings.warn('No block type was identified. This could be just an empty block.')
    main_node = ParentNode('div', nodes)
    return main_node
