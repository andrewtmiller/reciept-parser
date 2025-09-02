from app.parsers.reciept_parser import RecieptParser


class BJsReceiptParser(RecieptParser):
    def __init__(self, html_text):
        super().__init__(html_text)

    def parse_items(self):
        items = self.soup.findAll("app-order-details-item-level")
        if not items:
            raise ValueError("No items found in the BJs receipt.")
        parsed_items = []
        for item in items:
            name_html = item.find("p", {"class": "description"})
            price_html = item.find("div", {"class": "col-2"})
            name = name_html.text.strip().replace(",", "")
            price = float(price_html.text.replace("$", "").strip())
            parsed_items.append({"name": name, "price": price})
        return parsed_items
