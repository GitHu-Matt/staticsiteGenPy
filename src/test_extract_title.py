import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_trim(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("No title here\n## Subheading\n")


if __name__ == "__main__":
    unittest.main()
