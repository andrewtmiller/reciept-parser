import json
from bs4 import BeautifulSoup

class TargetReceiptParser:
    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text, 'html.parser')

    def parse_items(self):
        print(self.soup.prettify())
        items = self.soup.findAll("div", {"class": "kqpKGC"})
        if not items:
            raise ValueError("No items found in the receipt.")
        parsed_items = []
        for item in items:
            name_html = item.find("h3", {"class": "styles_ndsHeading__HcGpD"})
            price_html = item.find('span', {"data-test": "order-price"})
            qty_html = item.find('p', {"class": "h-text-sm"})

            if name_html and price_html and qty_html:
                name = name_html.text.strip()
                price = float(price_html.text.strip().replace('$', '').replace(' each', '').replace(' unit price', ''))
                qty = int(qty_html.text.strip().split(' ')[1])
                total_price = price * qty

                parsed_items.append({
                    'name': name,
                    'price': total_price,
                    'quantity': qty
                })
        return parsed_items

    def to_json(self):
        return json.dumps(self.parse_items())