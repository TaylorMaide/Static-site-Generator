import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode("h1", "hello World")
        self.assertIsNone(node.props)
    def test_single_prop(self):
        props = {"testing": "stuff"}
        node = HTMLNode(props=props)
        expected = " testing=\"stuff\""
        self.assertEqual(node.props_to_html(), expected)
    def test_multiple_props(self):
        props = {
            "href": "https://google.com",
            "target": "_blank"
        }
        node = HTMLNode(props=props)
        expected = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

if __name__ == "__main__":
    unittest.main()