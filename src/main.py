
from nodes.textnodefunctions import split_nodes_image, split_nodes_link, extract_markdown_links,text_to_textnodes,split_nodes_delimiter

from nodes.textnode import TextType, TextNode, Delimiter

from nodes.blockfunctions import markdown_to_html_node
# print("hello world")

# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

# all_types = [
#     TextType.TEXT,
#     TextType.BOLD,
#     TextType.ITALIC,
#     TextType.NORMAL,
#     TextType.CODE,
#     TextType.LINK,
#     TextType.IMAGE
# ]

# some_nodes = [
#     TextNode("Link text", TextType.LINK, "https://example.com"),
#     TextNode("Link text", TextType.LINK, "https://example.com")
# ]

# some_other_nodes = [
#     TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT),
#     TextNode("Check out [my website](https://www.mysite.org) for more info", TextType.TEXT),
#     TextNode("Here's a tutorial on [Python basics](https://docs.python.org/3/tutorial/index.html)", TextType.TEXT),
#     TextNode("Visit [GitHub](https://github.com) for code repositories", TextType.TEXT),
# ]



# for type in all_types:
#     print(type)

# # match some_nodes[0].text_type:
# #     case TextType.LINK:
# #         print("Link")
# #     case TextType.IMAGE:
# #         print("Image")
# #     case _:
# #         print("Unknown")

# print(split_nodes_link(some_other_nodes))

# print(extract_markdown_links(text))

# text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
# print("FROM MAIN")
# print(text_to_textnodes(text))
# node = TextNode("Here is `code1` and also `code2`", TextType.TEXT)
# print (node)
# new_nodes = split_nodes_delimiter([node], Delimiter.CODE, TextType.CODE)
# print(new_nodes)


# node = TextNode("This is text with a **bold** word", TextType.TEXT)
# print (node)
# new_nodes = split_nodes_delimiter([node], Delimiter.BOLD, TextType.BOLD)
# print(new_nodes)

# original = TextNode("This text has no code blocks", TextType.TEXT)
# print(original)
# new_nodes = split_nodes_delimiter([original], Delimiter.CODE, TextType.CODE)
# print(new_nodes)

# text = "Start **bold1** then _italic1_ and finally `code1`"
# print("FROM MAIN")
# print(text)
# # Process bold delimiters first
# nodes_after_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], Delimiter.BOLD, TextType.BOLD)
# intermediate_nodes = []
# for node in nodes_after_bold:

#     if node.text_type == TextType.TEXT:
#         nodes_italic = split_nodes_delimiter([node], Delimiter.ITALIC, TextType.ITALIC)
#         intermediate_nodes.extend(nodes_italic)
#     else:
#         intermediate_nodes.append(node)
# final_nodes = []
# for node in intermediate_nodes:
#     if node.text_type == TextType.TEXT:
#         nodes_code = split_nodes_delimiter([node], Delimiter.CODE, TextType.CODE)
#         final_nodes.extend(nodes_code)
#     else:
#         final_nodes.append(node)

# print("FROM MAIN")
# print (final_nodes)

def test_paragraphs():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    return (html, md, html=="<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

def test_codeblock():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    return (html, md, html=="<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")

code = test_codeblock()
print(code[0])
print("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
print(code[0])
print(code[1])
print(code[2])
print(test_codeblock())

print()
print("Next test for paragraphs")
print()

paragraphs = test_paragraphs()
print("Converted HTML")
print()
print(paragraphs[0])
print("What it needs to be")
print()
print("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
print()
print(paragraphs[2])
