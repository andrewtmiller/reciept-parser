from app.parsers.reciept_parser import RecieptParser


class CostcoReceiptParser(RecieptParser):
    def __init__(self, html_text):
        super().__init__(html_text)

    def parse_items(self):
        items = []
        table = self.soup.find("table", {"class": "MuiTable-root"})
        if not table:
            raise ValueError("No items table found in the Costco receipt.")
        for row in table.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) == 4:
                name = tds[2].get_text(strip=True)
                price_text = tds[3].get_text(strip=True)
                # Only process rows with a valid price and a plausible product name
                if (
                    name
                    and price_text
                    and not name.startswith("/")
                    and not name.upper() in ["SUBTOTAL", "TAX", "TOTAL"]
                ):
                    # Remove trailing letters and handle negative/discounts
                    price_clean = (
                        price_text.replace("N", "")
                        .replace("Y", "")
                        .replace("$", "")
                        .replace(",", "")
                        .replace("-", "")
                        .strip()
                    )
                    try:
                        price = float(price_clean)
                        # If the price_text ends with '-', it's a discount, so make it negative
                        if price_text.strip().endswith("-"):
                            price = -price
                        items.append({"name": name, "price": price})
                    except ValueError:
                        continue
        return items
