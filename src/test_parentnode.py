import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_with_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_nested_parent_nodes(self):
        node = ParentNode("div", [
            ParentNode("section", [
                LeafNode("p", "Here is some example text"),
                ParentNode("div", [
                    LeafNode("span", "Nested text")
                ])
            ])
        ])

        expected_html = "<div><section><p>Here is some example text</p><div><span>Nested text</span></div></section></div>"

        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_none_tag(self):
        node = ParentNode(None, [LeafNode("p", "some text")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_node_empty_tag(self):
        node = ParentNode("", [LeafNode("p", "some text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_none_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_node_empty_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div", 
            [LeafNode("p", "text")],
            {"class": "container", "id": "main"}
        )
        expected = '<div class="container" id="main"><p>text</p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_multiple_children_same_level(self):
        node = ParentNode("div", [
            LeafNode("p", "text1"),
            LeafNode("p", "text2"),
            LeafNode("p", "text3")
        ])
        expected = "<div><p>text1</p><p>text2</p><p>text3</p></div>"
        self.assertEqual(node.to_html(), expected)
    def test_multiple_children_same_level(self):
        node = ParentNode("div", [
            LeafNode("p", "text1"),
            LeafNode("p", "text2"),
            LeafNode("p", "text3")
        ])
        expected = "<div><p>text1</p><p>text2</p><p>text3</p></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_mixed_children_types(self):
        node = ParentNode("div", [
            LeafNode("span", "text1"),
            ParentNode("p", [
                LeafNode("b", "bold text")
            ]),
            LeafNode("span", "text2")
        ])
        expected = "<div><span>text1</span><p><b>bold text</b></p><span>text2</span></div>"
        self.assertEqual(node.to_html(), expected)

    def test_deep_nesting_with_props(self):
        node = ParentNode("div", [
            ParentNode("section", [
                LeafNode("p", "text", {"class": "text-bold"}),
                ParentNode("div", [
                    LeafNode("span", "nested", {"id": "special"})
                ], {"class": "wrapper"})
            ], {"data-type": "main"})
        ], {"id": "root"})
        expected = '<div id="root"><section data-type="main"><p class="text-bold">text</p><div class="wrapper"><span id="special">nested</span></div></section></div>'
        self.assertEqual(node.to_html(), expected)

    def test_special_characters(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello & Goodbye"),
            LeafNode("p", "<script>alert('hi')</script>")
        ])
        expected = "<div><p>Hello & Goodbye</p><p><script>alert('hi')</script></p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_props_special_characters(self):
        node = ParentNode("div", [
            LeafNode("p", "text")
        ], {"data-test": "Hello & Goodbye", "class": "my-class<>"})
        expected = '<div data-test="Hello & Goodbye" class="my-class<>"><p>text</p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_empty_string_content(self):
        node = ParentNode("div", [
            LeafNode("p", ""),
            LeafNode("span", "")
        ])
        expected = "<div><p></p><span></span></div>"
        self.assertEqual(node.to_html(), expected)

    def test_props_no_values(self):
        node = ParentNode("div", [
            LeafNode("p", "text")
        ], {"checked": "", "disabled": ""})
        expected = '<div checked="" disabled=""><p>text</p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_mixed_parent_and_text(self):
        node = ParentNode("div", [
            LeafNode(None, "Just text"),
            ParentNode("p", [
                LeafNode(None, "More text"),
                LeafNode("span", "Span text")
            ]),
            LeafNode(None, "Final text")
        ])
        expected = "<div>Just text<p>More text<span>Span text</span></p>Final text</div>"
        self.assertEqual(node.to_html(), expected)



if __name__ == "__main__":
    unittest.main()