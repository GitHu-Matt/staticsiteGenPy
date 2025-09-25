from pathlib import Path

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extract the first-level H1 title from a markdown string.
    Raises ValueError if no H1 is present.
    Example: extract_title("# Hello") -> "Hello"
    """
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 title found in markdown")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generate a HTML page:
    - Read markdown from from_path
    - Convert markdown to HTML using markdown_to_html_node(...).to_html()
    - Read template_path and replace {{ Title }} and {{ Content }}
    - Write final HTML to dest_path (creating directories if needed)
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src_md = Path(from_path).read_text(encoding="utf-8")
    template = Path(template_path).read_text(encoding="utf-8")

    # convert markdown to html string
    html_content = markdown_to_html_node(src_md).to_html()

    # extract title
    title = extract_title(src_md)

    # replace placeholders
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(full_html, encoding="utf-8")
