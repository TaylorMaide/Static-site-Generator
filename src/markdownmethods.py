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

def block_to_block_type(block):
    if block.startswith('```') and block.endswith('```'):
        return 'code'
    
    if block.startswith('#'):
        count = 0
        for char in block:
            if char == '#':
                count += 1
            else:
                break
        if (count <=6 and
            len(block) > count and
            block[count] == " " and
            len(block) > count + 1):
            return 'heading'
        
    lines = block.split('\n')

    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return 'paragraph'
        return 'quote'
    
    if block.startswith("*") or block.startswith('-'):
        first_marker = block[0]
        for line in lines:
            if not line.startswith(first_marker):
                return 'paragraph'
            if len(line) < 2 or line[1] != ' ':
                return 'paragraph'
        return 'unordered_list'
    
    if block.startswith("1"):
        expected_number = 1
        for line in lines:
            if not line.startswith(str(expected_number)):
                return 'paragraph'
            number_text = str(expected_number)
            expected_pattern = number_text + ". "
            if not line.startswith(expected_pattern):
                return 'paragraph'
            if len(line) <= len(expected_pattern):
                return 'paragraph'
            expected_number += 1
        return 'ordered_list'
    else:
        return 'paragraph'