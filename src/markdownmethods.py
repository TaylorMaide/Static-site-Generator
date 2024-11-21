import re

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]+)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    valid_matches = []
    for match in matches:
        if len(match[0]) > 0 and len(match[1]) > 0:
            valid_matches.append(match)
    return valid_matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[((?:[^\[\]]|\\\[|\\\])*)\]\(((?:[^\(\)]|\((?:[^\(\)]|\([^\(\)]*\))*\))*)\)"
    matches = re.findall(pattern, text)
    valid_matches = []
    for match in matches:
        if len(match[0]) > 0 and len(match[1]) > 0:
            valid_matches.append(match)
    return valid_matches