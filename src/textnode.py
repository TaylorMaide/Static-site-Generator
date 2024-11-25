from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text 
        self.text_type = text_type if text_type else TextType.TEXT
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    @staticmethod   
    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode("", text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                link_node = LeafNode("a", text_node.text)
                if text_node.url:
                    link_node.add_property("href", text_node.url)
                return link_node
            case TextType.IMAGE:
                image_node = LeafNode("img", "")
                src = text_node.url if text_node.url else "default_src"
                alt = text_node.text if text_node.text is not None else ""
                              
                image_node.add_property("src", src)
                image_node.add_property("alt", alt)
                return image_node
            case _:
                raise ValueError("Invalid TextType")
