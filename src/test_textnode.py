import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_equal_with_url(self):
        node1 = TextNode("Click me", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Click me", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
