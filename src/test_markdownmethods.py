import unittest

from markdownmethods import extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()