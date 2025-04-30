from enum import Enum

class text_types(Enum):
    normal = "normal"
    bold = "bold"
    code = "code"
    link = "link"
    image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_types(text_type)
        self.url = url
    
    def __eg__(self, Text_Node):
        return self.text == Text_Node.text and self.text_type == Text_Node.text_type and self.url == Text_Node.url

    def __repr__(self):
        if isinstance(self.url, str):
            return "TextNode(" + self.text + ", " + self.text_type.value + ", " + self.url + ")"
        return "TextNode(" + self.text + ", " + self.text_type.value + ")"