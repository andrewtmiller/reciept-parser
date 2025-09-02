from app.parsers.reciept_parser import RecieptParser


class LowesReceiptParser(RecieptParser):
    def __init__(self, html_text):
        super().__init__(html_text)

    def parse_items(self):
        items = []
        for row in self.soup.select(
            ".print-no-break .GridStyles__GridRow-sc-1ejksnu-1.kCxbMF.row.padding-none"
        ):
            name_tag = row.select_one("p.display-block.bold")
            price_tag = row.find("p", string=lambda s: s and "/ea." in s)
            total_tag = row.find(
                "p",
                string=lambda s: s and s.strip().startswith("$") and "/ea." not in s,
            )
            qty_tag = row.find("p", string=lambda s: s and "QTY" in s)
            if name_tag and total_tag:
                name = name_tag.get_text(strip=True)
                price = total_tag.get_text(strip=True).replace("$", "").replace(",", "")
                try:
                    price = float(price)
                except ValueError:
                    continue
                items.append({"name": name, "price": price})
        return items
