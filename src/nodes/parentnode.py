from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, props=None)

    def __repr__(self):
        return f"<_nodes.Parrent Node({self.tag}, {len(self.children)} children)>"

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")
        if not self.children:
            raise ValueError("Children are required")
        return f"<{self.tag}>{''.join(list(map(lambda child: child.to_html(), self.children)))}</{self.tag}>"
