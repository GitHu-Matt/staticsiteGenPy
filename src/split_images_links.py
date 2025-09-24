from typing import List
from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split any TextType.TEXT nodes that contain markdown image syntax:
      ![alt text](url)

    Returns a new list of TextNode with Image TextNodes (TextType.IMAGE)
    and TEXT nodes for the surrounding text. Non-TEXT nodes are preserved.
    Empty TEXT segments are not added.
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text
        # Find all images first (alt, url) in left-to-right order
        images = extract_markdown_images(s)
        if not images:
            new_nodes.append(node)
            continue

        remaining = s
        for alt, url in images:
            token = f"![{alt}]({url})"
            # split once at the first occurrence of this specific image markdown
            before, sep, after = remaining.partition(token)
            # partition returns before, sep, after; sep empty if token not found
            # but since images came from findall on s, token should be present in order
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after  # continue on the remainder

        # any trailing text after the last image
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split any TextType.TEXT nodes that contain markdown link syntax:
      [anchor text](url)

    Returns a new list of TextNode with Link TextNodes (TextType.LINK)
    and TEXT nodes for the surrounding text. Non-TEXT nodes are preserved.
    Images (which are ![alt](url)) are not treated as links because we use the extract_markdown_links helper.
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text
        links = extract_markdown_links(s)
        if not links:
            new_nodes.append(node)
            continue

        remaining = s
        for anchor, url in links:
            token = f"[{anchor}]({url})"
            before, sep, after = remaining.partition(token)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes
