from bs4 import BeautifulSoup


class RecieptParser:
    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text, "html.parser")

    def parse_items(self):
        raise NotImplementedError("Subclasses must implement parse_items")

    def to_json(self):
        import json

        return json.dumps(self.parse_items())
