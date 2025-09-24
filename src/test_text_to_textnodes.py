import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToTextNodes(unittest.TestCase):
    def test_complex_mixed_inline(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_empty_string_returns_empty_list(self):
        self.assertEqual(text_to_textnodes(""), [])
        self.assertEqual(text_to_textnodes("   \n\t "), [])

    def test_code_prevents_other_splits_inside(self):
        text = "a `**not bold**` b"
        nodes = text_to_textnodes(text)
        # code should be preserved as code text, not split into bold
        expected = [TextNode("a ", TextType.TEXT), TextNode("**not bold**", TextType.CODE), TextNode(" b", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_ordering_images_links_and_delimiters(self):
        # shows images and links are handled and surrounding text preserved
        text = "Start ![img](i.png) middle [link](p.html) end **B** _I_ `C`"
        nodes = text_to_textnodes(text)
        # verify presence and types in expected order (partial check)
        types = [n.text_type for n in nodes]
        expected_types = [TextType.TEXT, TextType.IMAGE, TextType.TEXT, TextType.LINK, TextType.TEXT, TextType.BOLD, TextType.TEXT, TextType.ITALIC, TextType.TEXT, TextType.CODE]
        self.assertEqual(types, expected_types)

if __name__ == "__main__":
    unittest.main()
