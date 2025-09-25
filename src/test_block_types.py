import unittest
from block_types import block_to_block_type, BlockType

class TestBlockTypes(unittest.TestCase):
    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6"), BlockType.HEADING)
        # seven hashes is not a heading per our rule (1-6)
        self.assertEqual(block_to_block_type("####### NotHeading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        md = "```\\nprint('hi')\\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
        # language hint on opening fence
        md2 = "```python\\nprint('x')\\n```"
        self.assertEqual(block_to_block_type(md2), BlockType.CODE)
        # missing closing fence -> not code
        md3 = "```\\nprint('x')"
        self.assertEqual(block_to_block_type(md3), BlockType.PARAGRAPH)

    def test_quote_block(self):
        bd = "> first line\\n> second line"
        self.assertEqual(block_to_block_type(bd), BlockType.QUOTE)
        # blank line inside is invalid per strict rule
        self.assertEqual(block_to_block_type("> ok\\n"), BlockType.QUOTE)
        # a line missing > => not a quote
        self.assertEqual(block_to_block_type("> good\\nnot a quote"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        lst = "- item one\\n- item two\\n- item three"
        self.assertEqual(block_to_block_type(lst), BlockType.UNORDERED_LIST)
        # lines not starting with "- " should fail
        self.assertEqual(block_to_block_type("- ok\\n* not ok"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ol = "1. first\\n2. second\\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)
        # wrong numbering (starts at 2) -> not ordered list
        ol2 = "2. first\\n3. second"
        self.assertEqual(block_to_block_type(ol2), BlockType.PARAGRAPH)
        # non-incrementing numbers
        ol3 = "1. a\\n3. b"
        self.assertEqual(block_to_block_type(ol3), BlockType.PARAGRAPH)
        # single-line numbered starting with 1 is allowed
        self.assertEqual(block_to_block_type("1. single"), BlockType.ORDERED_LIST)

    def test_paragraph_default(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(None), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
