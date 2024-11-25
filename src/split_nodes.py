import re
from textnode import TextNode, TextType

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimters_to_check = ["*", "`", "[", "!["]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter in node.text:
                parts = node.text.split(delimiter)

                if len(parts) % 2 == 0:
                    raise ValueError("Invalid markdown pattern")
            
                current_delimiters = delimters_to_check.copy()
                if delimiter in current_delimiters:
                    current_delimiters.remove(delimiter)
                if delimiter == "**":
                    current_delimiters.remove("*")

                for i in range(1, len(parts), 2):
                    for other_delimiter in delimters_to_check:
                        if other_delimiter in parts[i]:   
                            raise ValueError("Invalid markdown: mixed delimiters")
                
                for i in range(len(parts)):
                    current_part = parts[i]
                    if i % 2 == 0:
                        if current_part != "":
                            new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    pattern = r"!\[([^\[\]]+)\]\(([^\(\)]+)\)"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue
        segments = re.split(pattern, node.text)

        for i, segment in enumerate(segments):

            if i % 3 == 0 and segment:
                new_nodes.append(TextNode(segment, TextType.TEXT))

            elif i % 3 == 1:
                alt_text = segment
                if i + 1 < len(segments):
                    url = segments[i + 1]
                else:
                    url = ""

                if url:
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                else:
                    new_nodes.append(TextNode(alt_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    pattern = r"(?<!!)\[((?:[^\[\]]|\\\[|\\\])*)\]\(((?:[^\(\)]|\((?:[^\(\)]|\([^\(\)]*\))*\))*)\)"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue
        segments = re.split(pattern, node.text)
        for i, segment in enumerate(segments):
            if i % 3 == 0 and segment:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            elif i % 3 == 1:
                link_text = segment
                url = segments[i + 1] if i + 1 < len(segments) else None
                if link_text and url:
                    new_nodes.append(TextNode(link_text, TextType.LINK, url))
                else:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
    return new_nodes

def split_nodes_delimiters(old_nodes):
    nodes = old_nodes
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)
    return nodes

def text_to_textnodes(text):
    if not text:
        return []
    current_nodes = [TextNode(text, TextType.TEXT)]
    current_nodes = split_nodes_delimiters(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_image(current_nodes)
    return current_nodes