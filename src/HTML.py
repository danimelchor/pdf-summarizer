import src.utils as utils

class H:
    """
    A class to represent a header tag.
    """
    def __init__(self, text: str, importance: int):
        self.text = text
        self.importance = importance
    
    def __repr__(self) -> str:
        tag = f"h{self.importance}"
        id = utils.parse_id(self.text)
        return f"<{tag} id='{id}'>{self.text}</{tag}>"

class P:
    """
    A class to represent a paragraph tag.
    """
    def __init__(self, text: str):
        self.text = text

    def __repr__(self) -> str:
        return f"<p>{self.text}</p>"

class ContentLink:
    """
    A class to represent a link in the table of contents.
    """
    def __init__(self, text: str, importance: int):
        self.text = text
        self.importance = importance

    def __repr__(self) -> str:
        id = utils.parse_id(self.text)
        style = f"padding-left: {(self.importance - 1) * 20}px"
        return f"<a href='#{id}' style='{style}'>{self.text}</a>"

