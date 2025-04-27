from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD= "**Bold**"
    ITALIC = "_Italic_"
    CODE = "`Code`"
    LINK = "[anchor](url)"
    IMAGE = "![alt](url)"