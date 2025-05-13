from htmlnode import ParentNode
from textnode import TextNode, text_node_to_html_node, text_types
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockTypes
from splitnode import text_to_textnodes

def markdown_to_HTML(markdown):
    new_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockTypes.PARAGRAPH:
                new_nodes.append(ParentNode("p", texts_to_LeafNodes(block)))
            case BlockTypes.HEADING:
                new_nodes.append(ParentNode(heading_count(block), texts_to_LeafNodes(block.lstrip("# "))))
            case BlockTypes.CODE:
                new_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(block.lstrip("```\n").rstrip("```"), text_types.code))]))
            case BlockTypes.QUOTE:
                new_nodes.append(ParentNode("blockquote", quotes_to_LeafNodes(block)))
            case BlockTypes.UNORDERED_LIST:
                new_nodes.append(ParentNode("ul", ulist_to_LeafNodes(block)))
            case BlockTypes.ORDERED_LIST:
                new_nodes.append(ParentNode("ol", olist_to_LeafNodes(block)))
    return ParentNode("div", new_nodes)


def texts_to_LeafNodes(block):
    lines = block.split("\n")
    new_nodes = []
    for i in range(0, len(lines)):
        text = lines[i]
        if len(lines) > 1 and i != len(lines)-1:
            text = text + " "
        text_nodes = text_to_textnodes(text)
        for node in text_nodes:
            new_nodes.append(text_node_to_html_node(node))
    return new_nodes

def ulist_to_LeafNodes(texts):
    lines = texts.split("\n")
    new_nodes = []
    for line in lines:
        if not line.startswith("-"):
            raise ValueError("Invalid list format")
        new_nodes.append(ParentNode("li", texts_to_LeafNodes(line.lstrip("- "))))   
    return new_nodes

def olist_to_LeafNodes(block):
    lines = block.split("\n")
    new_nodes = []
    count = 1
    for line in lines:
        if not line.startswith(f"{count}."):
            raise ValueError("Invalid list order")
        new_nodes.append(ParentNode("li", texts_to_LeafNodes(line.lstrip(f"{count}. "))))
        count += 1
    return new_nodes

def quotes_to_LeafNodes(block):
    lines = block.split("\n")
    new_nodes = []
    for i in range(0, len(lines)):
        text = lines[i]
        if not text.startswith(">"):
            raise ValueError("Invalid quote block format")
        if len(lines) > 1 and i != len(lines)-1:
            text = text + " "
        text_nodes = text_to_textnodes(text.lstrip("> "))
        for node in text_nodes:
            new_nodes.append(text_node_to_html_node(node))
    return new_nodes

def heading_count(block):
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
