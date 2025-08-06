from bs4 import BeautifulSoup
from utilities import get_content
from CategoryOrganizer import CategoryOrganizer

FILE = "/Users/andrewmiller/Desktop/order.html"

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    # items = soup.findAll('div', {"data-test": "invoice-details-card"})
    items = soup.findAll("div", {"class": "kqpKGC"})
    for item in items:
        name_html = item.find("h3", {"class": "styles_ndsHeading__HcGpD"})
        price_html = item.find('span', {"data-test": "order-price"})
        qty_html = item.find('p',{"class":"h-text-sm"})
        name = name_html.text.strip()
        price = float(price_html.text.strip().replace('$','').replace(' each','').replace(' unit price',''))
        qty = int(qty_html.text.strip().split(' ')[1])
        price = price * qty
        organizer.organize_item(name, price)
    organizer.print_summary()