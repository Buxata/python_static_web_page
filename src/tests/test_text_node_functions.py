import unittest

from src.nodes.textnode import TextNode, TextType, Delimiter
from src.nodes.textnodefunctions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images,extract_markdown_links,text_to_textnodes


class TestTextNodeFunctions(unittest.TestCase):

    def test_text_functions(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.tag, None)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.tag, "b")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.tag, "i")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.tag, "code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_delimited_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.CODE, TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delimited_italics(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.ITALIC, TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_delimited_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.BOLD, TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_full_text_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_delimited_no_occurrence(self):
        """
        When no delimiter is present on the text node, the original node should be returned.
        """
        original = TextNode("This text has no code blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([original], Delimiter.CODE, TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no code blocks")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_delimited_multiple_code(self):
        """
        Test a text node that contains multiple occurrences of the code delimiter.
        Example: "Here is `code1` and also `code2`"
        """
        node = TextNode("Here is `code1` and also `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.CODE, TextType.CODE)
        # Expecting: "Here is " (TEXT), "code1" (CODE),
        # " and also " (TEXT), "code2" (CODE), and an empty TEXT node at the end.
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Here is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and also ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)


    def test_extract_markdown_images_multiple(self):
        """
        Test extracting multiple markdown images from a text string.
        """
        text = (
            "Here is an image ![first](https://example.com/first.png) and another one "
            "![second](https://example.com/second.png)"
        )
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("first", "https://example.com/first.png"),
                ("second", "https://example.com/second.png"),
            ],
        )

    def test_extract_markdown_links_multiple(self):
        """
        Test extracting multiple markdown links from a text string.
        """
        text = (
            "Visit the [first link](https://example.com/first) and also the "
            "[second link](https://example.com/second)"
        )
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("first link", "https://example.com/first"),
                ("second link", "https://example.com/second"),
            ],
        )

    def test_extract_markdown_images_none(self):
        """
        When no markdown images are present, an empty list should be returned.
        """
        text = "This text has no images so it should return an empty list."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_none(self):
        """
        When no markdown links are present, an empty list should be returned.
        """
        text = "This text has no links so it should return an empty list."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_text_to_textnodes_empty(self):
        """
        Converting an empty string using text_to_textnodes should return a single TextNode with empty text.
        """
        nodes = text_to_textnodes("")
        self.assertEqual(len(nodes), 0)

    def test_delimited_multiple_bold(self):
        """
        Test a text node that contains multiple occurrences of the bold delimiter.
        Example: "This is **bold1** and then **bold2** text"
        """
        node = TextNode("This is **bold1** and then **bold2** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.BOLD, TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold1")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and then ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "bold2")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_delimited_multiple_italic(self):
        """
        Test a text node that contains multiple occurrences of the italic delimiter.
        Example: "This is _italic1_ and then _italic2_ text"
        """
        node = TextNode("This is _italic1_ and then _italic2_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], Delimiter.ITALIC, TextType.ITALIC)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic1")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " and then ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "italic2")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_multiple_delimiters_mixed(self):
        """
        Test a text node that contains multiple types of delimiters in one string.
        Example: "Start **bold1** then _italic1_ and finally `code1`"
        The test processes each type of delimiter sequentially.
        """
        text = "Start **bold1** then _italic1_ and finally `code1`"
        # Process bold delimiters first
        nodes_after_bold = split_nodes_delimiter([TextNode(text, TextType.TEXT)], Delimiter.BOLD, TextType.BOLD)
        intermediate_nodes = []
        for node in nodes_after_bold:
            if node.text_type == TextType.TEXT:
                nodes_italic = split_nodes_delimiter([node], Delimiter.ITALIC, TextType.ITALIC)
                intermediate_nodes.extend(nodes_italic)
            else:
                intermediate_nodes.append(node)
        final_nodes = []
        for node in intermediate_nodes:
            if node.text_type == TextType.TEXT:
                nodes_code = split_nodes_delimiter([node], Delimiter.CODE, TextType.CODE)
                final_nodes.extend(nodes_code)
            else:
                final_nodes.append(node)
        self.assertEqual(len(final_nodes), 6)
        self.assertEqual(final_nodes[0].text, "Start ")
        self.assertEqual(final_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[1].text, "bold1")
        self.assertEqual(final_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[2].text, " then ")
        self.assertEqual(final_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[3].text, "italic1")
        self.assertEqual(final_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(final_nodes[4].text, " and finally ")
        self.assertEqual(final_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[5].text, "code1")
        self.assertEqual(final_nodes[5].text_type, TextType.CODE)

    # def test_text_to_textnodes_complex(self):
    #     """
    #     Test the conversion of a string with multiple markdown types in one go.
    #     """
    #     text = (
    #         "Start **bold** then _italic_ after that `code` then an image ![img](https://example.com/img.png) "
    #         "and finally a [link](https://example.com/link)"
    #     )
    #     expected_nodes = [
    #         TextNode("Start ", TextType.TEXT),
    #         TextNode("bold", TextType.BOLD),
    #         TextNode(" then ", TextType.TEXT),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" after that ", TextType.TEXT),
    #         TextNode("code", TextType.CODE),
    #         TextNode(" then an image ", TextType.TEXT),
    #         TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
    #         TextNode(" and finally a ", TextType.TEXT),
    #         TextNode("link", TextType.LINK, "https://example.com/link"),
    #     ]
    #     nodes = text_to_textnodes(text)
    #     self.assertEqual(len(nodes), len(expected_nodes))
    #     for node, expected in zip(nodes, expected_nodes):
    #         self.assertEqual(node.text, expected.text)
    #         self.assertEqual(node.text_type, expected.text_type)
    #         # Check for extra props if they are present (like href or image URL).
    #         if expected.props:
    #             self.assertEqual(node.props, expected.props)


if __name__ == "__main__":
    unittest.main()
