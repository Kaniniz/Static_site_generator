from enum import Enum

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = []
    md = markdown.split("\n\n")
    for text in md:
        text = text.rstrip().lstrip()
        if text == "":
            continue
        
        blocks.append(text)
    return blocks
    
def block_to_block_type(block):
    if block == "" or block.startswith("\n"):
        raise Exception("Empty block")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockTypes.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockTypes.CODE

    is_quote = True

    block_lines = block.split("\n")
    if block.startswith(">"):
        for block in block_lines:
            if block == "":
                continue
            if block.startswith(">"):
                continue
            else:
                is_quote = False
                break
        if is_quote == True:
            return BlockTypes.QUOTE

    is_unordered = True
    if block.startswith("- "):
        for block in block_lines:
            if block == "":
                continue
            if block.startswith("- "):
                continue
            else:
                is_unordered = False
                break
        if is_unordered == True:
            return BlockTypes.UNORDERED_LIST

    is_ordered = True
    count = 1
    if block.startswith(f"{count}. "):
        for block in block_lines:
            if block == "":
                continue
            if block.startswith(f"{count}. "):
                count += 1
                continue
            else:
                is_ordered = False
                break
        if is_ordered == True:
            return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH