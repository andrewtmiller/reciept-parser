from utilities import get_content
from CategoryOrganizer import CategoryOrganizer
import pprint
import sys

FILE = input("Path to reciept file: ") or "/Users/andrewmiller/Desktop/order.html"


sys.dont_write_bytecode = True

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    items = soup.findAll('div', {"data-testid": "itemtile-stack"})
    if not items:
        print("No items found in the receipt.")
    for item in items:
        # Check if the item is in the unavailable section
        if item.find_parent('div', {"data-testid": "category-accordion-"}):
            continue
        
        name_html = item.find('span', {"class": "w_V_DM"})
        price_html = item.find('div', {"data-testid": "line-price"})
        for span in price_html.find_all('span', class_='w_iUH7'):
            span.extract()
        x=0
        for s in price_html.contents:
            text = s.get_text(strip=True)
            if s.string and s.string.strip() == '': 
                x=x+1
                s.extract()
            elif s.string and 'Discount price' in s.string:
                x=x+1
                s.extract()
            elif s.name == 'span' and s.get('class') == ['w_iUH7']:
                x=x+1
                s.extract()
            else:
                x=x+1
                # inspect_element(s)
            
        
        name = name_html.text.strip().replace(',','')
        price = float(price_html.text.replace('$','').strip())
        organizer.organize_item(name,price)
    organizer.print_summary()
