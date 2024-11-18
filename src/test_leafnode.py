import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(value=None, tag="p").to_html()
    
    def test_leafnode_raw_text(self):
        node = LeafNode(tag=None, value="This is raw text.")
        result = node.to_html()
        self.assertEqual(result, "This is raw text.")

    def test_leafnode_with_tag_no_props(self):
        node = LeafNode(tag="p", value="A paragraph.")
        result = node.to_html()
        self.assertEqual(result, "<p>A paragraph.</p>")

    def test_leafnode_with_tag_with_props(self):
        node = LeafNode(tag="a", value="Click here", props = {"href": "https://www.example.com"})
        result = node.to_html()
        self.assertEqual(result, '<a href="https://www.example.com">Click here</a>')

if __name__ == "__main__":
    unittest.main()