from bs4 import BeautifulSoup
from utilities import get_content
from CategoryOrganizer import CategoryOrganizer

FILE = input("File path: ") or "/Users/andrewmiller/Desktop/order.html"

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    items = soup.findAll('app-order-details-item-level')
    for item in items:
        name_html = item.find('p',{"class": "description"})
        price_html = item.find('div',{"class": "col-2"})
        name = name_html.text.strip()
        price = float(price_html.text.replace('$','').strip())
        organizer.organize_item(name, price)
    
    organizer.print_summary()