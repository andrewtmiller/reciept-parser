from categories import groceries

class CategoryOrganizer:
    def __init__(self):
        self.categories = {
            "Personal": [
                "shampoo",
                "tampons",
                "conditioner",
                "toothpaste",
                "deoderant",
                "eyeliner",
                "blush",
                "lotion",
                "cosmetics",
                "mascara",
                "makeup",
                "face serum",
                "facial",
                "scalp treatment",
            ],
            "Groceries": groceries.GROCERIES,
            "Clothing": [
                "sweater",
                "socks",
                "t-shirt",
                "underwear",
                "shoe",
                "shirt",
                "body suit",
                "tights",
                "gloves",
                "boots",
                "pullover",
                "clogs",
                "leggings",
                "ballet flats",
                "hoodie",
                "jkt",
            ],
            "Home Supplies": [
                "aluminum foil",
                "bath tissue",
                "batteries",
                "bowls",
                "cascplatplus",
                "coffee filter",
                "command 8pk heavy phs adhesives",
                "command strips",
                "dawn powerws",
                "dish soap",
                "disinfectant",
                "dixie to go",
                "dryer sheets",
                "extension cord",
                "freeze block",
                "ks dish pacs",
                "laundry",
                "lysol"
                "outlet",
                "paper towel",
                "parchment paper",
                "plate",
                "snack bag",
                "straws",
                "swiffer wet",
                "thermacell refills",
                "toiletwand",
                "utility pans",
                "ziploc",
                "zipper bags",
            ],
            "Pharmacy": ["cough drops", "throat drops"],
            "Baby Supplies": ["diapers", "baby wipes", "diaper", "baby wipe"],
            "Gifts": [
                "wrapping paper",
                "gift wrap",
                "inflatables yard",
                "christmas tree",
                "nutcraker",
            ],
            "Furnishings": ["curtain"],
            "Other": [],
        }
        self.organized_items = {category: [] for category in self.categories}

    def organize_item(self, item_name, item_price):
        other = True
        for category, keywords in self.categories.items():
            if any(keyword in item_name.lower() for keyword in keywords):
                self.organized_items[category].append(
                    {"name": item_name, "price": item_price}
                )
                other = False
        if other:
            self.organized_items["Other"].append(
                {"name": item_name, "price": item_price}
            )

    def print_summary(self):
        for category, items in self.organized_items.items():
            total = sum(item["price"] for item in items)
            if total > 0:
                print(f"\n{category}: ${total}")
                # total =
                for item in items:
                    print(item)
