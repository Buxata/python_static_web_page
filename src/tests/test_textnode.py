import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_different_text(self):
        node1 = TextNode("Text one", TextType.BOLD)
        node2 = TextNode("Text two", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example1.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example2.com")
        self.assertNotEqual(node1, node2)

    def test_url_none_equal(self):
        node1 = TextNode("Text", TextType.BOLD, None)
        node2 = TextNode("Text", TextType.BOLD)  # Default is None
        self.assertEqual(node1, node2)

    def test_with_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
