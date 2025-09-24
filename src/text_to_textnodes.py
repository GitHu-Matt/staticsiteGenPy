from typing import List
from textnode import TextNode, TextType
from split_images_links import split_nodes_image, split_nodes_link
from split_delimiter import split_nodes_delimiter

def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Convert a raw markdown-flavored inline string into a list of TextNode objects.

    Splitting order (recommended):
      1. images      -> ![alt](url)
      2. links       -> [text](url)
      3. code        -> `code`
      4. bold        -> **bold**
      5. italic      -> _italic_

    Returns an empty list for empty/whitespace-only input.
    """
    if text is None:
        return []

    # If text is empty or only whitespace, return empty list
    if text.strip() == "":
        return []

    # Start with a single TEXT node
    nodes: List[TextNode] = [TextNode(text, TextType.TEXT)]

    # Apply splitters in recommended order
    nodes = split_nodes_image(nodes)                        # images first
    nodes = split_nodes_link(nodes)                         # then links
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)   # code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # bold
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) # italic

    return nodes
