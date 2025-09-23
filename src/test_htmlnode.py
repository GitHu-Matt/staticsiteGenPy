import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        got = node.props_to_html()
        # order of dict iteration is stable in Python 3.7+, but tests should allow either order.
        self.assertTrue(got.startswith(" "))
        # Must contain both attributes
        self.assertIn('href="https://www.google.com"', got)
        self.assertIn('target="_blank"', got)

    def test_props_to_html_none_or_empty(self):
        node_none = HTMLNode(props=None)
        self.assertEqual(node_none.props_to_html(), "")

        node_empty = HTMLNode(props={})
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr_shows_all_fields(self):
        child = HTMLNode(tag="span", value="x")
        node = HTMLNode(tag="p", children=[child], props={"class": "lead"})
        r = repr(node)
        self.assertIn("HTMLNode(", r)
        self.assertTrue(("tag='p'" in r) or ('tag="p"' in r))
        self.assertIn("children=", r)
        self.assertTrue(("props={'class': 'lead'}" in r) or ('props={"class": "lead"}' in r))


if __name__ == "__main__":
    unittest.main()
