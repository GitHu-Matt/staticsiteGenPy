import unittest
from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


class TestSplitDelimiter(unittest.TestCase):
    def test_split_backtick(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_occurrences(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_preserve_non_text_nodes(self):
        node1 = TextNode("plain", TextType.TEXT)
        node2 = TextNode("bolded", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        # second node should be preserved untouched
        self.assertEqual(new_nodes[1], node2)
        self.assertEqual(len(new_nodes), 2)

    def test_leading_and_trailing_delimiters(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # leading/trailing empty text segments are skipped, leaving only the bold node
        self.assertEqual(new_nodes, [TextNode("bold", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()
