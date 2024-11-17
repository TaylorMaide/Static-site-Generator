import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)


    def test_url_none(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertIsNone(node.url)
    
    def test_nodes_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_nodes_text_different(self):
        node1 = TextNode("This is text A", TextType.BOLD)
        node2 = TextNode("This is text B", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_nodes_url_different(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://different.com")
        self.assertNotEqual(node1, node2)

    


if __name__ == "__main__":
    unittest.main()