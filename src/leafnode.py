from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if props is None:
            props = {}
        super().__init__(tag, props)
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return str(self.value)
    
        attributes = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        if attributes:
            return f"<{self.tag} {attributes}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"