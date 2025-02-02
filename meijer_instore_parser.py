from bs4 import BeautifulSoup
from utilities import get_content
from CategoryOrganizer import CategoryOrganizer

FILE = "/Users/andrewmiller/Desktop/meijer.html"

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    order = soup.find("div", {"class": "pdfViewer"})
    items = order.findAll('span', {"role": "presentation"})
    # for item in items:
    #     name_html = item.find('h3',{"class": "cart-item__title"})
    #     price_html = item.find('div',{"class": "cart-item__total-price"})
    #     name = name_html.text.strip()
    #     price = float(price_html.text.replace('$','').strip())
    #     organizer.organize_item(name, price)

    # organizer.print_summary()
    print(items)
