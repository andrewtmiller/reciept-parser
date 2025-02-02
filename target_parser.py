from bs4 import BeautifulSoup
from utilities import CATEGORIES, get_content

FILE = "/Users/andrewmiller/Desktop/target.html"

def organize(name, price):
    for category, keywords in CATEGORIES.items():
        if any(keyword in name.lower() for keyword in keywords):
            organized_items[category].append({"name": name, "price": price})
            return True
    return False

if __name__ == '__main__':
    soup = get_content(FILE)
    items = soup.findAll('div', {"data-test": "invoice-details-card"})
    organized_items = {category: [] for category in CATEGORIES}
    for item in items:
        name_html = item.find('p', {"class": "h-padding-b-tight"})
        price_html = item.findAll('div', {"class": "sc-be7acf58-2"})[-1]
        name = name_html.text.strip()
        price = float(price_html.text.strip().replace('Item total','').replace('$',''))
        result = organize(name, price)
        if not result:
            organized_items["Other"].append({"name": name, "price": price})
    for category, items in organized_items.items():
        total = sum(item["price"] for item in items)
        if total > 0:
            print(f"\n{category}: ${total}")
            # total = 
            for item in items:
                print(item)