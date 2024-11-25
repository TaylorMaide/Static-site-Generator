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

def markdown_to_blocks(markdown):
    valid_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        check_block = block.strip()
        if check_block:
            valid_blocks.append(check_block)
    return valid_blocks
