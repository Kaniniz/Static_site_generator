import unittest
from markdown_blocks import BlockTypes, markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_block_leading_spaces(self):
        md = " This is a block with a leading space.\n\nThis is a block with a trailing space. "
        self.assertListEqual(
            [            
            "This is a block with a leading space.",
            "This is a block with a trailing space."
            ],
            markdown_to_blocks(md)
        )

    def test_block_to_block_type(self):
        block = "This is a paragraph"
        block1 = "# This is a heading"
        block2 = "#### This is a bigger heading"
        block3 = "```This is code```"
        block4 = "> This is a quote"
        block5 = """> This is multiple quotes
> On seperate
>Lines
"""
        block6 = """- This is an unordered list
- with multiple things
- in it
"""
        block7 = """1. This is an ordered list
2. It has numbers
3. In the begining
"""
        
        self.assertEqual(BlockTypes.PARAGRAPH, block_to_block_type(block))
        self.assertEqual(BlockTypes.HEADING, block_to_block_type(block1))
        self.assertEqual(BlockTypes.HEADING, block_to_block_type(block2))
        self.assertEqual(BlockTypes.CODE, block_to_block_type(block3))
        self.assertEqual(BlockTypes.QUOTE, block_to_block_type(block4))
        self.assertEqual(BlockTypes.QUOTE, block_to_block_type(block5))
        self.assertEqual(BlockTypes.UNORDERED_LIST, block_to_block_type(block6))
        self.assertEqual(BlockTypes.ORDERED_LIST, block_to_block_type(block7))

if __name__ == "__main__":
    unittest.main()