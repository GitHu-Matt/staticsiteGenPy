import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "![one](url1.png) and ![two](url2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("one", "url1.png"), ("two", "url2.png")], matches)

    def test_extract_markdown_links(self):
        text = "Link [boot dev](https://www.boot.dev) and [YouTube](https://youtube.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("boot dev", "https://www.boot.dev"), ("YouTube", "https://youtube.com")],
            matches,
        )

    def test_links_and_images_together(self):
        text = "An ![img](img.png) and a [link](page.html)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("img", "img.png")], images)
        self.assertListEqual([("link", "page.html")], links)

    def test_no_matches(self):
        text = "plain text with no markdown"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()
