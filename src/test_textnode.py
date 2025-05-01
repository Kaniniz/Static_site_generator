import unittest

from textnode import TextNode, text_types


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_types.bold)
        node2 = TextNode("This is a text node", text_types.bold)
        node3 = TextNode("This is a text node", text_types.normal)
        node4 = TextNode("This is a link node", text_types.link, "https://example.com")
        node5 = TextNode("This is not a text node", text_types.normal)
        node6 = TextNode("This is a text node", text_types.bold, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node5)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertEqual(node, node6)


if __name__ == "__main__":
    unittest.main()