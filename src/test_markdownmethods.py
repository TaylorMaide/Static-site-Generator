import unittest

from markdownmethods import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type

class TestMarkdownMethods(unittest.TestCase):
    def test_extract_markdown_links(self):
        node1 = extract_markdown_links("[text](url)")
        node2 = [("text", "url")]
        self.assertEqual(node1, node2)
    def test_extract_markdown_links_is_empty(self):
        node1 = extract_markdown_links("")
        node2 = []
        self.assertEqual(node1, node2)
    def test_multiple_markdown_links(self):
        text = "Here is a [link1](url1) and another [link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
    def test_links_in_mixed_content(self):
        text = "Here is a [link](url1) and an ![image](url2) followed by another [link2](url3)"
        expected_links = [("link", "url1"), ("link2", "url3")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_links)
    def test_links_with_text_no_links(self):
        text = "Here is a bunch of test stuff"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
    def test_malformed_links(self):
        malformed_cases = [
            "This is a [link(url)",
            "This is a [link](url",
            "This is a [](url)",
            "This is a [link]()",
            "This is a link"
        ]
        for text in malformed_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, [])
    def test_special_characters_links(self):
        test_cases = [
            ("[link with params](https://example.com/page?id=123&type=doc)",
             [("link with params", "https://example.com/page?id=123&type=doc")]),
            ("[my cool link](https://example.com/page.html)",
             [("my cool link", "https://example.com/page.html")]),
        ]
        for text, expected in test_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        node1 = extract_markdown_images("![alt](url)")
        node2 = [("alt", "url")]
        self.assertEqual(node1, node2)
    def test_extract_markdown_images_is_empty(self):
        node1 = extract_markdown_images("")
        node2 = []
        self.assertEqual(node1, node2)
    def test_multiple_markdown_images(self):
        text = "Here is a ![image1](url1) and another ![image2](url2)"
        expected = [("image1", "url1"), ("image2", "url2")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
    def test_images_in_mixed_content(self):
        text = "Here is a [link](url1) and an ![image](url2) followed by another [link2](url3)"
        expected_links = [("image", "url2")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected_links)
    def test_links_with_text_no_images(self):
        text = "Here is a bunch of test stuff"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)
    def test_malformed_images(self):
        malformed_case = [
            "This is a [link(url)",
            "This is a [link](url",
            "This is a [](url)",
            "This is a [link]()",
            "This is a link"
        ]
        for text in malformed_case:
            result = extract_markdown_images(text)
            self.assertEqual(result, [])
    def test_special_characters_images(self):
        test_cases = [
            ("![alt](https://example.com/image?id=123&type=png)",
             [("alt", "https://example.com/image?id=123&type=png")]),
            ("![my cool image](https://example.com/pic.jpg)",
             [("my cool image", "https://example.com/pic.jpg")]),
            ("![alt](https://example.com/image#fragment)",
             [("alt", "https://example.com/image#fragment")]),
            ("![spaced text here](https://example.com/image@2x.png?size=large)",
             [("spaced text here", "https://example.com/image@2x.png?size=large")])
        ]
        for text, expected in test_cases:
            result = extract_markdown_images(text)
            self.assertEqual(result, expected)

    def test_spaces_in_texts(self):
        image_cases = [
            ("![my    spaced    image](url.jpg)",
             [("my    spaced    image", "url.jpg")]),
            ("![ spaced image ](url.jpg)",
             [(" spaced image ", "url.jpg")]),
            ("![spaced\timage](url.jpg)",
             [("spaced\timage", "url.jpg")])
        ]
    
        link_cases = [
            ("[my    spaced    link](url.com)",
             [("my    spaced    link", "url.com")]),
            ("[ spaced link ](url.com)",
             [(" spaced link ", "url.com")])
        ]
        for text, expected in image_cases:
            result = extract_markdown_images(text)
            self.assertEqual(result, expected)
        for text, expected in link_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, expected)
    def test_nested_parentheses(self):
        test_cases = [
            ("[link](https://example.com/path(1))",
             [("link", "https://example.com/path(1)")]),
            ("[complex](https://api.com/data(nested(deeply)))",
             [("complex", "https://api.com/data(nested(deeply))")])
        ]
        for text, expected in test_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, expected)

    def test_escaped_characters(self):
        test_cases = [
            ("[Link with \\[brackets\\]](url)",
             [("Link with \\[brackets\\]", "url")]),
            ("[Text with \\(parens\\)](url)",
             [("Text with \\(parens\\)", "url")])
        ]
        for text, expected in test_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, expected)

    def test_urls_with_spaces_and_encoding(self):
        test_cases = [
            ("[link](https://example.com/path%20with%20spaces)",
             [("link", "https://example.com/path%20with%20spaces")]),
            ("[link](https://example.com/path+with+plus)",
             [("link", "https://example.com/path+with+plus")]),
            ("[link](https://example.com/?q=hello%20world&lang=en)",
             [("link", "https://example.com/?q=hello%20world&lang=en")])
        ]
        for text, expected in test_cases:
            result = extract_markdown_links(text)
            self.assertEqual(result, expected)

    # Testing for markdown to blocks

    def test_markdown_to_blocks_empty_string(self):
        test_markdown = ""
        expected_result = []
        result = markdown_to_blocks(test_markdown)
        self.assertEqual(expected_result, result)

    def test_markdown_to_blocks(self):
            test_markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
            expected_result = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
            result = markdown_to_blocks(test_markdown)
            self.assertEqual(result, expected_result)
    
    def test_markdown_to_blocks_only_whitespace(self):
        test_markdown = " \n \n "
        expected_result = []
        result = markdown_to_blocks(test_markdown)
        self.assertEqual(result, expected_result)

    def test_markdown_to_block_multiple_consectutive_empty_lines(self):
        test_markdown = "block1\n\n\nblock2"
        expected_result = [
            "block1",
            "block2"
        ]
        result = markdown_to_blocks(test_markdown)
        self.assertEqual(result, expected_result)
    
    def test_markdown_to_block_whitespace_only_blocks(self):
        test_markdown = "block1\n\n \n\nblock2"
        expected_result = [
            "block1",
            "block2"
        ]
        result = markdown_to_blocks(test_markdown)
        self.assertEqual(result, expected_result)

    # Testing block to block type

    def test_block_to_block_type_heading(self):
        test_block1 = "# Heading 1"
        expected_result1 = "heading"
        result1 = block_to_block_type(test_block1)
        self.assertEqual(result1, expected_result1)
        test_block2 = "### Heading 3"
        expected_result2 = "heading"
        result2 = block_to_block_type(test_block2)
        self.assertEqual(result2, expected_result2)
        test_block3 = "###### Heading 6"
        expected_result3 = "heading"
        result3 = block_to_block_type(test_block3)
        self.assertEqual(result3, expected_result3)

    def test_block_to_block_type_heading_invalid(self):
        test_block1 = "#NoSpace"
        expected_result1 = "heading"
        result1 = block_to_block_type(test_block1)
        self.assertNotEqual(result1, expected_result1)
        test_block2 = "####### Heading 3"
        expected_result2 = "heading"
        result2 = block_to_block_type(test_block2)
        self.assertNotEqual(result2, expected_result2)
        test_block3 = "# "
        expected_result3 = "heading"
        result3 = block_to_block_type(test_block3)
        self.assertNotEqual(result3, expected_result3)

    def test_block_to_block_type_quote(self):
        test_block1 = "> Single quote"
        expected_result1 = "quote"
        result1 = block_to_block_type(test_block1)
        self.assertEqual(result1, expected_result1)
        test_block2 = "> Line1\n> Line 2"
        expected_result2 = "quote"
        result2 = block_to_block_type(test_block2)
        self.assertEqual(result2, expected_result2)
        test_block3 = "> Line1\n> Line 2\n> Line 3"
        expected_result3 = "quote"
        result3 = block_to_block_type(test_block3)
        self.assertEqual(result3, expected_result3)

    def test_block_to_block_type_quote_invalid(self):
        test_block1 = "> Line1\nLine 2"
        expected_result1 = "quote"
        result1 = block_to_block_type(test_block1)
        self.assertNotEqual(result1, expected_result1)
        test_block2 = "Not a quote"
        expected_result2 = "quote"
        result2 = block_to_block_type(test_block2)
        self.assertNotEqual(result2, expected_result2)

    def test_block_to_block_type_code(self):
        test_block1 = "```code```"
        expected_result1 = "code"
        result1 = block_to_block_type(test_block1)
        self.assertEqual(result1, expected_result1)

    def test_block_to_block_type_unordered_lists(self):
        test_block1 = "* Item 1\n* Item 2"
        expected_result1 = "unordered_list"
        result1 = block_to_block_type(test_block1)
        self.assertEqual(result1, expected_result1)
        test_block2 = "- Item 1\n- Item 2"
        expected_result2 = "unordered_list"
        result2 = block_to_block_type(test_block2)
        self.assertEqual(result2, expected_result2)

    def test_block_to_block_type_unordered_list_invalid(self):
        test_block1 = "* Item 1\n- Item 2"
        expected_result1 = "unordered_list"
        result1 = block_to_block_type(test_block1)
        self.assertNotEqual(result1, expected_result1)
        test_block2 = "*Item 1"
        expected_result2 = "unordered_list"
        result2 = block_to_block_type(test_block2)
        self.assertNotEqual(result2, expected_result2)
        test_block3 = "* Item 1\nItem 2"
        expected_result3 = "unordered_list"
        result3 = block_to_block_type(test_block3)
        self.assertNotEqual(result3, expected_result3)
        test_block4 = "*"
        expected_result4 = "unordered_list"
        result4 = block_to_block_type(test_block4)
        self.assertNotEqual(result4, expected_result4)

    def test_block_to_block_type_ordered_list(self):
        test_block1 = "1. First\n2. Second"
        expected_result1 = "ordered_list"
        result1 = block_to_block_type(test_block1)
        self.assertEqual(result1, expected_result1)
        test_block2 = "1. First\n3. Second"
        expected_result2 = "paragraph"
        result2 = block_to_block_type(test_block2)
        self.assertEqual(result2, expected_result2)
        test_block3 = "2. First"
        expected_result3 = "paragraph"
        result3 = block_to_block_type(test_block3)
        self.assertEqual(result3, expected_result3)
        test_block4 = "1.First"
        expected_result4 = "paragraph"
        result4 = block_to_block_type(test_block4)
        self.assertEqual(result4, expected_result4)
        test_block5 = "1. \n2. "
        expected_result5 = "paragraph"
        result5 = block_to_block_type(test_block5)
        self.assertEqual(result5, expected_result5)
        test_block6 = "1. First\n2. Second\n3. Third"
        expected_result6 = "ordered_list"
        result6 = block_to_block_type(test_block6)
        self.assertEqual(result6, expected_result6)
        test_block7 = "1 First"
        expected_result7 = "paragraph"
        result7 = block_to_block_type(test_block7)
        self.assertEqual(result7, expected_result7)
    
    


if __name__ == "__main__":
    unittest.main()