from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE  = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
                continue
            else:
                break

        if count > 0 and count <= 6 and len(block) > count and block[count] == " ":
            return BlockType.HEADING
        
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    block_split = block.split("\n")

    if block_split[0].startswith(">"):
        count = 0
        for line in block_split:
            if line.startswith(">"):
                count += 1
                continue
            else:
                break
        
        if len(block_split) == count:
            return BlockType.QUOTE
        
    if block_split[0].startswith("- "):
        count = 0
        for line in block_split:
            if line.startswith("- "):
                count += 1
                continue
            else:
                break
        
        if len(block_split) == count:
            return BlockType.ULIST
        
    if block_split[0].startswith("1. "):
        count = 0
        for i in range(len(block_split)):
            if block_split[i].startswith(f"{i+1}. "):
                count += 1
                continue
            else:
                break
        
        if len(block_split) == count:
            return BlockType.OLIST
        
    return BlockType.PARAGRAPH