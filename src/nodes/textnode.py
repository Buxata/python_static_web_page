from enum import Enum

class Delimiter(Enum):
    BOLD = '**',
    ITALIC = '_',
    CODE = '`',

delimiters = {
    Delimiter.BOLD: "**",
    Delimiter.ITALIC: "_",
    Delimiter.CODE: "`",
}


delimiters_regex_match = {
    Delimiter.BOLD: r'(\*\*|__)(.*?)\1',
    Delimiter.ITALIC: r'(?<!\*)\*(?!\*)(.*?)\*(?!\*)|(?<!_)_(?!_)(.*?)_(?!_)',
    Delimiter.CODE: r'`([^`\n]+?)`',
}

class TextType(Enum):
    TEXT = "text"
    NORMAL = "normal"
    BOLD= "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    HEADER1 =  "header1"
    HEADER2 = "header2"
    HEADER3 = "header3"
    HEADER4 = "header4"
    HEADER5 = "header5"
    HEADER6 = "header6"

class TextNode():
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

delimiters_to_text_type = {
    Delimiter.BOLD: TextType.BOLD,
    Delimiter.ITALIC: TextType.ITALIC,
    Delimiter.CODE: TextType.CODE,
}
