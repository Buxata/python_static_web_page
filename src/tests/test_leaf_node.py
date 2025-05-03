import unittest

from src.nodes.leafnode import LeafNode


class testLeafNode(unittest.TestCase):

    def test_to_html_with_no_children(self):
        # Test converting to HTML with no children
        # Text node (no tag)
        text_node = LeafNode(None, "Just text", None)
        self.assertEqual(text_node.to_html(), "Just text")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_anchor(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    # def test_to_html_with_no_children(self):
    #     # Test converting to HTML with no children
    #     # Text node (no tag)
    #     text_node = HTMLNode(None, "Just text", None, {})
    #     self.assertEqual(text_node.to_html(), "Just text")

    #     # Tag with value
    #     p_node = HTMLNode("p", "Paragraph text", None, {})
    #     self.assertEqual(p_node.to_html(), "<p>Paragraph text</p>")

    #     # Tag with properties
    #     div_node = HTMLNode("div", "", None, {"class": "alert"})
    #     self.assertEqual(div_node.to_html(), '<div class="alert"></div>')

    # def test_to_html_with_children(self):
    #     # Test converting to HTML with children
    #     child1 = HTMLNode("span", "Child 1", None, {})
    #     child2 = HTMLNode("span", "Child 2", None, {})
    #     parent = HTMLNode("div", "", [child1, child2], {"id": "parent"})

    #     expected = '<div id="parent"><span>Child 1</span><span>Child 2</span></div>'
    #     self.assertEqual(parent.to_html(), expected)

    # def test_nested_structure(self):
    #     # Test a more complex nested structure
    #     grandchild = HTMLNode("b", "Bold text", None, {})
    #     child = HTMLNode("p", "", [grandchild], {"class": "paragraph"})
    #     parent = HTMLNode("div", "", [child], {"id": "content"})

    #     expected = '<div id="content"><p class="paragraph"><b>Bold text</b></p></div>'
    #     self.assertEqual(parent.to_html(), expected)

if __name__ == "__main__":
    unittest.main()
