from typing import Optional, List, Dict, Any


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, Any]] = None,
    ):
        """
        tag: HTML tag name (e.g. "p", "a"). If None -> raw text node.
        value: textual content (used when there are no children).
        children: list of HTMLNode children (used when value is None).
        props: dictionary of attributes, e.g. {"href": "https://..."}
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Render this node to HTML. Child classes will override this.
        For now, indicate this should be overridden."""
        raise NotImplementedError("to_html() must be implemented by subclasses")

    def props_to_html(self) -> str:
        """
        Convert self.props dict into a string of HTML attributes.
        Returns a string that *starts with a single space* if there are attributes,
        otherwise returns an empty string.
        Example:
            props = {"href": "https://x", "target": "_blank"}
            -> ' href="https://x" target="_blank"'
        """
        if not self.props:
            return ""
        parts = []
        for k, v in self.props.items():
            # Convert booleans: True => key only, False => skip
            if isinstance(v, bool):
                if v:
                    parts.append(f'{k}')
                else:
                    continue
            else:
                parts.append(f'{k}="{v}"')
        return " " + " ".join(parts) if parts else ""

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
