from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from .models import Category, Term
except ImportError:
    from models import Category, Term


class CategoryOrganizer:
    def __init__(self, db_url="sqlite:///categories.db"):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # Load categories and terms from the database
        self.categories = {}
        categories = self.session.query(Category).all()
        for category in categories:
            self.categories[category.name] = [term.name for term in category.terms]
        self.organized_items = {category: [] for category in self.categories}

    def organize_item(self, item_name, item_price):
        item_name_lower = item_name.lower()
        # Sort categories by number of terms (ascending)
        sorted_categories = sorted(self.categories.items(), key=lambda x: len(x[1]))
        for category, keywords in sorted_categories:
            if any(keyword in item_name_lower for keyword in keywords):
                self.organized_items[category].append(
                    {"name": item_name, "price": item_price}
                )
                return
        # If no category matches, add to "Other" (create if not present)
        if "Other" not in self.organized_items:
            self.organized_items["Other"] = []
        self.organized_items["Other"].append({"name": item_name, "price": item_price})

    def get_summary(self):
        summary = {}
        for category, items in self.organized_items.items():
            total_price = sum(item["price"] for item in items)
            summary[category] = {"items": items, "total_price": total_price}
        return summary
