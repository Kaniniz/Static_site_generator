from enum import Enum
from htmlnode import LeafNode

class text_types(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text_type == other.text_type and self.text == other.text and self.url == other.url
                

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_types.text:
            return LeafNode(None, text_node.text)
        case text_types.bold:
            return LeafNode("b", text_node.text)
        case text_types.italic:
            return LeafNode("i", text_node.text)
        case text_types.code:
            return LeafNode("code", text_node.text)
        case text_types.link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case text_types.image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type")

    
    