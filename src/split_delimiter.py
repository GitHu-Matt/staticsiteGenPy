from typing import List
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Given a list of TextNode objects, split any TEXT nodes on `delimiter`
    and convert the delimited segments into TextNodes of `text_type`.

    Examples:
      split_nodes_delimiter([TextNode("a `b` c", TextType.TEXT)], "`", TextType.CODE)
      -> [TextNode("a ", TEXT), TextNode("b", CODE), TextNode(" c", TEXT)]

    Rules:
      - Only nodes with text_type == TextType.TEXT are inspected/split.
      - Non-TEXT nodes are passed through unchanged.
      - If a matching closing delimiter is not found, raise ValueError.
      - Empty text segments (outside delimiters) are skipped to avoid empty TextNode objects.
    """
    if delimiter == "":
        raise ValueError("Delimiter must be a non-empty string")

    new_nodes: List[TextNode] = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text
        parts = s.split(delimiter)

        # No delimiter present -> keep original node
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # number of delimiter occurrences == len(parts) - 1
        # We need delimiters to come in pairs (opening + closing). If the number of occurrences is odd,
        # there's an unmatched delimiter.
        if (len(parts) - 1) % 2 != 0:
            raise ValueError(f"Unclosed delimiter {delimiter!r} in text: {s!r}")

        # Build nodes: even-index parts are outside delimiters (TEXT), odd-index parts are inside (text_type)
        for idx, part in enumerate(parts):
            if idx % 2 == 0:
                # outside delimiter
                if part != "":
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiter -> convert to requested text_type
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
