import re
from textnode import TextNode, text_types


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_types.text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_types.text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_types.text:
            new_nodes.append(old_node)
            continue
        image_sections = extract_markdown_images(old_node.text)
        if image_sections == []:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        next_section = old_node.text
        for section in image_sections:
            sections = next_section.split(f"![{section[0]}]({section[1]})", 1)
            next_section = sections[1]
            if sections[0] == "":
                pass
            else: 
                new_nodes.append(TextNode(sections[0], text_types.text))
            new_nodes.append(TextNode(section[0], text_types.image, section[1]))
        if next_section != "":
            new_nodes.append(TextNode(next_section, text_types.text))
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_types.text:
            new_nodes.append(old_node)
            continue
        link_sections = extract_markdown_links(old_node.text)
        if link_sections == []:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        next_section = old_node.text
        for section in link_sections:
            sections = next_section.split(f"[{section[0]}]({section[1]})", 1)
            next_section = sections[1]
            if sections[0] == "":
                pass
            else: 
                new_nodes.append(TextNode(sections[0], text_types.text))
            new_nodes.append(TextNode(section[0], text_types.link, section[1]))
        if next_section != "":
            new_nodes.append(TextNode(next_section, text_types.text))
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_link(
                split_nodes_image(
                    split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter(
                                [TextNode(text, text_types.text)], "**", text_types.bold
                            ), "_", text_types.italic
                        ), "`", text_types.code
                    )
                )
            )

