"""Class for quote data model"""


class QuoteModel:
    def __init__(self, body: str, author: str):
        """Create a new `QuoteModel`.

        :param body: content of a quote
        :param author: author of a quote
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return a string representation of this object."""
        return f'"{self.body}" - {self.author}'
