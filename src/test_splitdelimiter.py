import unittest

from textnode import TextNode, TextType
from splitdelimiter import split_node_delimiter

class TestSplitDelimiter(unittest.TestCase):
    def test_basic_code_delimiter(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        nodes = split_node_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " here")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_no_delimiter(self):
        node = TextNode("Plain text here", TextType.TEXT)
        nodes = split_node_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Plain text here")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_invalid_delimiter(self):
        invalid_node = TextNode("Invalid **markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_node_delimiter([invalid_node], "**", TextType.BOLD)

    def test_multiple_nodes(self):
        node1 = TextNode("Hello **world**", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        nodes = split_node_delimiter([node1, node2], "**", TextType.BOLD)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, "Already bold")
        self.assertEqual(nodes[2].text_type, TextType.BOLD)

    def test_multiple_delimiters_in_node(self):
        node = TextNode("This is `code` and more `code` here", TextType.TEXT)
        nodes = split_node_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " and more ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "code")
        self.assertEqual(nodes[3].text_type, TextType.CODE)
        self.assertEqual(nodes[4].text, " here")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

    def test_empty_delimiter_content(self):
        node = TextNode("This has an **** empty bold", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
    
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This has an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " empty bold")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        nodes = split_node_delimiter([node], "*", TextType.ITALIC)
    
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_wrong_delimiter_style(self):
        node = TextNode("This is **italic** text", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
    
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_leading_delimiter(self):
        node = TextNode("**bold** text", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
    
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, " text")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_middle_delimiter(self):
        node = TextNode("some `code` here", TextType.TEXT)
        nodes = split_node_delimiter([node], "`", TextType.CODE)
    
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "some ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " here")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_no_split_different_type(self):
        node = TextNode("**bold**", TextType.BOLD)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
    
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "**bold**")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_missing_delimiter(self):
        node = TextNode("some *italic text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_node_delimiter([node], "*", TextType.ITALIC)

    def test_split_nodes_delimiter_trailing(self):
        node = TextNode("some text**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_node_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("**text****text**", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("**text******text**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_node_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_leading(self):
        node = TextNode("**text**rest", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "rest")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("**text*text**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_node_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_multiple_occurrences(self):
        node = TextNode("Text with **bold** and **more bold**", TextType.TEXT)
        nodes = split_node_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "Text with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "more bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)