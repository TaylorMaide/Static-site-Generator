import re
from textnode import TextNode, TextType

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = ["**", "*", "`"]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter in node.text:
                parts = node.text.split(delimiter)
                for i in range(1, len(parts), 2):
                    for other_delimiter in delimiter:
                        if other_delimiter in parts[i]:
                            raise ValueError("Cannot have mixed or nested delimiters")
                
                if len(parts) % 2 == 0:
                    raise ValueError("Invalid markdown pattern")
                
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

