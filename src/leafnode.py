from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None):
        """
        A leaf node cannot have children.
        tag: required (can be None for raw text)
        value: required (must not be None)
        props: optional dictionary of attributes
        """
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        # Raw text node (no tag)
        if self.tag is None:
            return self.value

        # Normal HTML element
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
