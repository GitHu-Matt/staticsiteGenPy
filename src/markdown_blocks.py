from typing import List

def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Split a full markdown document string into block-level strings.
    Blocks are separated by blank lines (double newline).
    Leading/trailing whitespace is stripped.
    Empty blocks are removed.
    """
    if markdown is None:
        return []

    # Split on double newlines
    raw_blocks = markdown.split("\n\n")

    # Strip whitespace and remove empties
    blocks = [block.strip() for block in raw_blocks if block.strip() != ""]

    return blocks
