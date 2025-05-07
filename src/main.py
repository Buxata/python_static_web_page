
from nodes.textnodefunctions import split_nodes_image, split_nodes_link, extract_markdown_links

from nodes.textnode import TextType, TextNode
print("hello world")

text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

all_types = [
    TextType.TEXT,
    TextType.BOLD,
    TextType.ITALIC,
    TextType.NORMAL,
    TextType.CODE,
    TextType.LINK,
    TextType.IMAGE
]

some_nodes = [
    TextNode("Link text", TextType.LINK, "https://example.com"),
    TextNode("Link text", TextType.LINK, "https://example.com")
]

some_other_nodes = [
    TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT),
    TextNode("Check out [my website](https://www.mysite.org) for more info", TextType.TEXT),
    TextNode("Here's a tutorial on [Python basics](https://docs.python.org/3/tutorial/index.html)", TextType.TEXT),
    TextNode("Visit [GitHub](https://github.com) for code repositories", TextType.TEXT),
]
some_other_image_nodes = [
    TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT),
    TextNode("Check out ![my website](https://www.mysite.org) for more info", TextType.TEXT),
    TextNode("Here's a tutorial on ![Python basics](https://docs.python.org/3/tutorial/index.html)", TextType.TEXT),
    TextNode("Visit ![GitHub](https://github.com) for code repositories", TextType.TEXT),
]

for type in all_types:
    print(type)

# match some_nodes[0].text_type:
#     case TextType.LINK:
#         print("Link")
#     case TextType.IMAGE:
#         print("Image")
#     case _:
#         print("Unknown")

print(split_nodes_image(some_other_image_nodes))
