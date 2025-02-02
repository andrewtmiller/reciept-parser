from bs4 import BeautifulSoup
from utilities import get_content
from CategoryOrganizer import CategoryOrganizer

FILE = "/Users/andrewmiller/Desktop/costco.html"

def prep_price(price_html):
    remove = ['$', 'Y', 'N','-']
    price = price_html.text
    for r in remove:
        price = price.replace(r,'')
    return float(price.strip())

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    order = soup.find('tbody',{"class": "MuiTableBody-root"})
    items = order.findAll('tr', {"class": "MuiTableRow-root"})
    for i in range(len(items)):
        item = items[i]
        next_item = items[i+1]
        if item.contents[1].text == 'SUBTOTAL':
            break
        if '-' in item.contents[3].text:
            continue
        name_html = item.contents[2]
        price_html = item.contents[3]
        name = name_html.text.strip()
        price = prep_price(price_html)
        if len(next_item.contents) > 3:
            if '-' in next_item.contents[3].text:
                discount = prep_price(next_item.contents[3])
                price = price - discount
        organizer.organize_item(name, price)
    
    organizer.print_summary()