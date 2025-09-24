import unittest
from textnode import TextNode, TextType
from split_images_links import split_nodes_image, split_nodes_link

class TestSplitImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_no_images_or_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_preserve_non_text_nodes(self):
        node_text = TextNode("plain", TextType.TEXT)
        node_bold = TextNode("x", TextType.BOLD)
        out_images = split_nodes_image([node_text, node_bold])
        out_links = split_nodes_link([node_text, node_bold])
        # second node should be preserved as-is
        self.assertEqual(out_images[1], node_bold)
        self.assertEqual(out_links[1], node_bold)

    def test_leading_trailing_images(self):
        node = TextNode("![lead](a.png) middle ![tail](b.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("lead", TextType.IMAGE, "a.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("tail", TextType.IMAGE, "b.png"),
            ],
            new_nodes,
        )

    def test_mixed_images_and_links(self):
        node = TextNode("Start ![img](i.png) and [link](p.html) end", TextType.TEXT)
        # split images first, then split links on result
        step1 = split_nodes_image([node])
        # after image split, step1 should have TEXT, IMAGE, TEXT nodes
        step2 = split_nodes_link(step1)
        # Verify step2 contains a Link node correctly
        # Find the Link node in step2
        found_links = [n for n in step2 if n.text_type == TextType.LINK]
        self.assertEqual(len(found_links), 1)
        self.assertEqual(found_links[0], TextNode("link", TextType.LINK, "p.html"))

if __name__ == "__main__":
    unittest.main()
