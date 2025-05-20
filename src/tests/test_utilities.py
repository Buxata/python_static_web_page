import unittest

from src.nodes.utilities import extract_title

class TestUtilitiesFunctions(unittest.TestCase):
    def test_extract_title_success(self):
        markdown = "# My Title\nSome additional text"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_extract_title_no_header(self):
        markdown = "Some text without a markdown header"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

    def test_extract_title_invalid_header(self):
        markdown = "## NotATitle"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

if __name__ == "__main__":
    unittest.main()
