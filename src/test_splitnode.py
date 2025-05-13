import unittest
from splitnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, text_types


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_types.text)
        new_nodes = split_nodes_delimiter([node], "**", text_types.bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_types.text),
                TextNode("bolded", text_types.bold),
                TextNode(" word", text_types.text),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode(
            "**bolded**", text_types.text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_types.bold)
        self.assertListEqual(
            [
                TextNode("bolded", text_types.bold)
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_types.text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_types.bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_types.text),
                TextNode("bolded", text_types.bold),
                TextNode(" word and ", text_types.text),
                TextNode("another", text_types.bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_types.text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_types.bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_types.text),
                TextNode("bolded word", text_types.bold),
                TextNode(" and ", text_types.text),
                TextNode("another", text_types.bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", text_types.text)
        new_nodes = split_nodes_delimiter([node], "_", text_types.italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_types.text),
                TextNode("italic", text_types.italic),
                TextNode(" word", text_types.text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", text_types.text)
        new_nodes = split_nodes_delimiter([node], "**", text_types.bold)
        new_nodes = split_nodes_delimiter(new_nodes, "_", text_types.italic)
        self.assertListEqual(
            [
                TextNode("bold", text_types.bold),
                TextNode(" and ", text_types.text),
                TextNode("italic", text_types.italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_types.text)
        new_nodes = split_nodes_delimiter([node], "`", text_types.code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_types.text),
                TextNode("code block", text_types.code),
                TextNode(" word", text_types.text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_split_node_image(self):
        self.maxDiff = None
        node = TextNode("This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and a ![second_image](https://imgur.com/3elNhQu)", text_types.text)
        node1 = TextNode("Another two images ![image one](https://imgur.com/gallery/estinien-wyrmblood-FEl4Vzs)![image two](https://imgur.com/gallery/many-night-zku7Acz)", text_types.text)
        node2 = TextNode("A node without a image", text_types.text)
        node3 = TextNode("A BOLD node", text_types.bold)
        self.assertListEqual(
            [
            TextNode("This is text with a ", text_types.text),
            TextNode("image", text_types.image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_types.text),
            TextNode("second_image", text_types.image, "https://imgur.com/3elNhQu"),
            TextNode("Another two images ", text_types.text),
            TextNode("image one", text_types.image, "https://imgur.com/gallery/estinien-wyrmblood-FEl4Vzs"),
            TextNode("image two", text_types.image, "https://imgur.com/gallery/many-night-zku7Acz"),
            TextNode("A node without a image", text_types.text)
            ],
        split_nodes_image([node, node1, node2]))
        self.assertEqual(
            [
                TextNode("A node without a image", text_types.text),
                TextNode("This is text with a ", text_types.text),
                TextNode("image", text_types.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_types.text),
                TextNode("second_image", text_types.image, "https://imgur.com/3elNhQu"),
                TextNode("A BOLD node", text_types.bold),
                TextNode("A node without a image", text_types.text)
            ], 
            split_nodes_image([node2, node, node3, node2]))

    def test_split_node_image_single(self):
        node = TextNode("![image](https://imgur.com/3elNhQu)", text_types.text)
        self.assertEqual(
            [
                TextNode("image", text_types.image, "https://imgur.com/3elNhQu")
            ],
            split_nodes_image([node])
        )

    def test_split_node_link(self):
        self.maxDiff = None
        node = TextNode("This is a text with links to [Boot.dev](https://boot.dev) and [Youtube](https://youtube.com)!", text_types.text)
        node1 = TextNode("This is a text without links", text_types.text)
        node2 = TextNode("This is a text with a link to [Nexus mods](https://nexusmods.com)", text_types.text)
        self.assertListEqual(
            [
                TextNode("This is a text with links to ", text_types.text),
                TextNode("Boot.dev", text_types.link, "https://boot.dev"),
                TextNode(" and ", text_types.text),
                TextNode("Youtube", text_types.link, "https://youtube.com"),
                TextNode("!", text_types.text),
                TextNode("This is a text without links", text_types.text),
                TextNode("This is a text with a link to ", text_types.text),
                TextNode("Nexus mods", text_types.link, "https://nexusmods.com")
            ],
        split_nodes_link([node, node1, node2]))

    def test_split_node_link_single(self):
        node = TextNode("[link](https://boot.dev)", text_types.text)
        self.assertEqual(
            [
                TextNode("link", text_types.link, "https://boot.dev")
            ],
            split_nodes_link([node])
        )

    def test_text_to_textnode(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
            TextNode("This is ", text_types.text),
            TextNode("text", text_types.bold),
            TextNode(" with an ", text_types.text),
            TextNode("italic", text_types.italic),
            TextNode(" word and a ", text_types.text),
            TextNode("code block", text_types.code),
            TextNode(" and an ", text_types.text),
            TextNode("obi wan image", text_types.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_types.text),
            TextNode("link", text_types.link, "https://boot.dev"),
            ],
            text_to_textnodes(text))

    def test_text_to_textnode_paragraph(self):
        text = """This is a paragraph
with **multiple** lines
with a single line break
between them"""
        self.assertListEqual(
            [
            TextNode("This is a paragraph\nwith ", text_types.text),
            TextNode("multiple", text_types.bold),
            TextNode(" lines\nwith a single line break\nbetween them", text_types.text)
            ],
            text_to_textnodes(text)
        )


if __name__ == "__main__":
    unittest.main()
