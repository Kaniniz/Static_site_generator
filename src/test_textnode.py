import unittest

from textnode import TextNode, text_types, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_types.bold)
        node2 = TextNode("This is a text node", text_types.bold)
        node3 = TextNode("This is a text node", text_types.text)
        node4 = TextNode("This is a link node", text_types.link, "https://example.com")
        node5 = TextNode("This is not a text node", text_types.text)
        node6 = TextNode("This is a text node", text_types.bold, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node5)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertEqual(node, node6)

    def test_text(self):
        node = TextNode("This is a text node", text_types.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_leafnode_with_link(self):
        node = TextNode("Hello World!", text_types.link, "https://example.com")
        node1 = TextNode("Hello World!", text_types.image, "https://example.com")
        html_node = text_node_to_html_node(node)
        html_node1 = text_node_to_html_node(node1)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello World!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node1.tag, "img")
        self.assertEqual(html_node1.value, None)
        self.assertEqual(html_node1.props, {"src": "https://example.com", "alt": "Hello World!"})

    def test_invalid_text_type(self):
        node = TextNode("Hello World!", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()