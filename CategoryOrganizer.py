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
                "moisturizer",
                "toothbrush",
                "razor",
                "ponytail",
                "sunscreen",
                "brightening serum"
            ],
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
                "joggers",
                "puma sock",
                "pumaliner8pr",
                "sandals",
                "utility short",
                "pants",
                "shorts",
                "skort",
                "romper",
                "blouse",
                "dress"
            ],
            "Home Supplies": [
                "aluminum foil",
                "bath tissue",
                "batteries",
                "bowls",
                "broom",
                "cascplatplus",
                "cleaner",
                "cleaners",
                "cleaning",
                "coffee filter",
                "command 8pk heavy phs adhesives",
                "command strips",
                "dawn powerws",
                "detergent",
                "dish soap",
                "disinfectant",
                "disinfecting wipe",
                "dixie to go",
                "dryer sheets",
                "extension cord",
                "freeze block",
                "hand soap",
                "hangers",
                "ks dish pacs",
                "laundry",
                "light bulb",
                "lysol" "mop",
                "outlet",
                "paper towel",
                "parchment paper",
                "plate",
                "snack bag",
                "sponges",
                "straws",
                "swiffer wet",
                "thermacell refills",
                "tissue",
                "toiletwand",
                "towel",
                "trash bag",
                "trash can",
                "utility pans",
                "vacuum",
                "ziploc",
                "zipper bags",
                "clorox",
                "duracell",
                "ks bath",
                "food storage"
            ],
            "Medical": [
                "cough drops",
                "throat drops",
                "vicks",
                "ibuprofen",
                "medicine",
                "supplement",
                "softgels",
                "pregnancy test",
            ],
            "Baby Supplies": ["diapers", "baby wipes", "diaper", "baby wipe"],
            "Gifts": [
                "wrapping paper",
                "gift wrap",
                "inflatables yard",
                "christmas tree",
                "nutcraker",
            ],
            "Furnishings": ["curtain"],
            "Groceries": groceries.GROCERIES,
            "Other": [],
        }
        self.organized_items = {category: [] for category in self.categories}

    def organize_item(self, item_name, item_price):
        for category, keywords in self.categories.items():
            if any(keyword in item_name.lower() for keyword in keywords):
                self.organized_items[category].append(
                    {"name": item_name, "price": item_price}
                )
                return  # Exit after assigning to the first matching category
        # If no category matches, add to "Other"
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
