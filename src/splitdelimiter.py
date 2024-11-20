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