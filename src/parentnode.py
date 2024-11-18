from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if props is None:
            props = {}
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be empty or None")
        if self.children is None or self.children == []:
            raise ValueError("Parent Node must have children")
        
        attributes = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        if attributes:
            return f"<{self.tag} {attributes}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"