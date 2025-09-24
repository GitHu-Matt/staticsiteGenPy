import re
from typing import List, Tuple

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extract markdown images of the form:
    ![alt text](url)

    Returns list of (alt_text, url) tuples.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extract markdown links of the form:
    [anchor text](url)

    Returns list of (anchor_text, url) tuples.
    The regex ensures it doesn't capture images (which also start with !).
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
