


class HTMLNode():
    def __init__(self, tag, value, props=None, children=None):
        self.tag = tag
        self.value = value
        self.props = props or {}
        self.children = children or []

    def to_html(self):
        raise ValueError("Method not implemented")

    def props_to_html(self):
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self) -> str:
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
