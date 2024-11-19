import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


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
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
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

    def test_text_to_html_Normal(self):
        text_node = TextNode("Example text", TextType.TEXT)
        expected_html_node = LeafNode("", "Example text")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Bold(self):
        text_node = TextNode("Example text", TextType.BOLD)
        expected_html_node = LeafNode("b", "Example text")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Italic(self):
        text_node = TextNode("Example text", TextType.ITALIC)
        expected_html_node = LeafNode("i", "Example text")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)
    
    def test_text_to_html_Code(self):
        text_node = TextNode("Example text", TextType.CODE)
        expected_html_node = LeafNode("code", "Example text")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Links_no_props(self):
        text_node = TextNode("Example text", TextType.LINK)
        expected_html_node = LeafNode("a", "Example text", props={})
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Links_with_props(self):
        text_node = TextNode("Example text", TextType.LINK)
        text_node.url = "http://example.com"
        expected_html_node = LeafNode("a", "Example text", props={"href": "http://example.com"})
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Images_no_props_with_defaults(self):
        text_node = TextNode("", TextType.IMAGE)
        text_node.url = ""
        text_node.text = ""
        expected_html_node = LeafNode("img", "")
        expected_html_node.add_property("src", "default_src")
        expected_html_node.add_property("alt", "")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_Images_with_props(self):
        text_node = TextNode("An example image", TextType.IMAGE, "example.com/image.png")
        expected_html_node = LeafNode("img", "")
        expected_html_node.add_property("src", "example.com/image.png")
        expected_html_node.add_property("alt", "An example image")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_error_for_invalid_type(self):
        invalid_node = TextNode("Example text", "Invalid Type")
        with self.assertRaises(ValueError):
            TextNode.text_node_to_html_node(invalid_node)

    def test_text_to_html_EmptyText(self):
        text_node = TextNode("", TextType.TEXT)
        expected_html_node = LeafNode("", "")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_SpecialCharacters(self):
        special_text = "<>This & that"
        text_node = TextNode(special_text, TextType.TEXT)
        expected_html_node = LeafNode("", special_text)
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    def test_text_to_html_PartialImageProps(self):
        text_node = TextNode("", TextType.IMAGE, "example.com/image.png")
        expected_html_node = LeafNode("img", "")
        expected_html_node.add_property("src", "example.com/image.png")
        expected_html_node.add_property("alt", "")
        result_html_node = TextNode.text_node_to_html_node(text_node)
        self.assertEqual(result_html_node, expected_html_node)

    

    


if __name__ == "__main__":
    unittest.main()