import unittest
from copy_static import extract_title

class test_copy_static(unittest.TestCase):
    def test_extract_title(self):
        md = "# Title"
        md2 = "## Wrong title"
        self.assertEqual("Title", extract_title(md))
        with self.assertRaises(Exception):
            extract_title(md2)