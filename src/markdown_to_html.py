from typing import List
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from markdown_blocks import markdown_to_blocks
from block_types import block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
import re


def text_to_children(text: str) -> List[HTMLNode]:
    """
    Convert an inline markdown string into a list of HTMLNode children.
    Normalize internal newlines into single spaces so multi-line paragraphs
    are treated as single flow text for inline parsing.
    """
    # collapse internal newlines to single space and normalize whitespace around them
    normalized = re.sub(r'\s*\n\s*', ' ', text).strip()
    nodes: List[HTMLNode] = []
    if normalized == "":
        return nodes
    text_nodes = text_to_textnodes(normalized)
    for tn in text_nodes:
        nodes.append(text_node_to_html_node(tn))
    return nodes


def _heading_node(block: str) -> HTMLNode:
    # count leading '#' characters on first line
    line = block.splitlines()[0]
    i = 0
    while i < len(line) and line[i] == '#':
        i += 1
    level = max(1, min(6, i))
    content = line[i:].lstrip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)


def _code_node(block: str) -> HTMLNode:
    # preserve raw inner lines exactly (including their newlines)
    lines = block.splitlines()
    if len(lines) >= 3:
        inner_lines = lines[1:-1]
    else:
        inner_lines = []
    code_text = "\n".join(inner_lines)
    # include trailing newline inside code tag per test expectation
    code_text_with_trailing_newline = code_text + ("\n" if inner_lines or code_text == "" else "")
    code_leaf = LeafNode("code", code_text_with_trailing_newline)
    return ParentNode("pre", [code_leaf])


def _quote_node(block: str) -> HTMLNode:
    lines = block.splitlines()
    # remove leading '>' and optional space, then join lines with newline preserved
    stripped_lines = [line[1:].lstrip() if line.startswith(">") else line for line in lines]
    combined = "\n".join(stripped_lines)
    # For quotes we keep line breaks inside the quote content, but still parse inline per-line.
    # We'll pass combined with newline characters — but our text_to_children collapses newlines,
    # so to preserve quote internal newlines we bypass normalization: handle inline per line.
    children: List[HTMLNode] = []
    for ln in stripped_lines:
        # parse each logical line separately and append a text node containing a newline between lines
        line_children = text_to_children(ln)
        children.extend(line_children)
        # append a raw newline as a text leaf between quote lines (if not last)
        if ln is not stripped_lines[-1]:
            children.append(LeafNode(None, "\n"))
    return ParentNode("blockquote", children)


def _unordered_list_node(block: str) -> HTMLNode:
    lines = block.splitlines()
    items: List[HTMLNode] = []
    for line in lines:
        item_text = line[2:] if line.startswith("- ") else line
        item_children = text_to_children(item_text)
        li_node = ParentNode("li", item_children)
        items.append(li_node)
    return ParentNode("ul", items)


def _ordered_list_node(block: str) -> HTMLNode:
    lines = block.splitlines()
    items: List[HTMLNode] = []
    for line in lines:
        idx = line.find(". ")
        if idx != -1:
            item_text = line[idx + 2 :]
        else:
            item_text = line
        item_children = text_to_children(item_text)
        li_node = ParentNode("li", item_children)
        items.append(li_node)
    return ParentNode("ol", items)


def _paragraph_node(block: str) -> HTMLNode:
    # paragraphs may include internal newlines; collapse them to spaces via text_to_children
    children = text_to_children(block)
    return ParentNode("p", children)


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert a full markdown document into a single parent HTMLNode (a div)
    containing child HTMLNodes for each block.
    """
    root_children: List[HTMLNode] = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            node = _heading_node(block)

        elif btype == BlockType.CODE:
            node = _code_node(block)

        elif btype == BlockType.QUOTE:
            node = _quote_node(block)

        elif btype == BlockType.UNORDERED_LIST:
            node = _unordered_list_node(block)

        elif btype == BlockType.ORDERED_LIST:
            node = _ordered_list_node(block)

        else:  # paragraph or default
            node = _paragraph_node(block)

        root_children.append(node)

    return ParentNode("div", root_children)
