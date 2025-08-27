import json
from bs4 import BeautifulSoup


class TargetReceiptParser:
    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text, "html.parser")

    def parse_items(self):
        # Find all divs with data-test="package-cart-item-row"
        package_rows = self.soup.find_all("div", {"data-test": "package-card-item-row"})
        if not package_rows:
            raise ValueError("No items found in the receipt.")
        parsed_items = []
        for row in package_rows:
            # Find all direct child divs (item containers)
            item_divs = row.find_all("div", recursive=False)
            for item in item_divs:
                name_html = item.find("h3")
                price_html = item.find("span", {"data-test": "order-price"})
                qty_html = item.find("p", {"class": "h-text-sm"})

                if name_html and price_html and qty_html:
                    name = name_html.text.strip()
                    price = float(
                        price_html.text.strip()
                        .replace("$", "")
                        .replace(" each", "")
                        .replace(" unit price", "")
                    )
                    # Try to extract quantity from the text, fallback to 1 if not found
                    qty_text = qty_html.text.strip()
                    try:
                        qty = int(qty_text.split(" ")[1])
                    except (IndexError, ValueError):
                        qty = 1
                    total_price = price * qty

                    parsed_items.append(
                        {"name": name, "price": total_price, "quantity": qty}
                    )
        return parsed_items

    def to_json(self):
        return json.dumps(self.parse_items())
