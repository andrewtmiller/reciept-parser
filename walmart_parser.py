from utilities import get_content
from CategoryOrganizer import CategoryOrganizer
import pprint
import sys

FILE = "/Users/andrewmiller/Desktop/walmart.html"


sys.dont_write_bytecode = True

# def organize(name, price):
#     for category, keywords in CATEGORIES.items():
#         if any(keyword in name.lower() for keyword in keywords):
#             organized_items[category].append({"name": name, "price": price})
#             return True
#     return False

# def inspect_element(element):
#     print(f"Element Type: {type(element).__name__}")
#     print(f"Name: {element.name}") 
#     print(f"Attributes: {element.attrs}")
#     print(f"Text Content: {element.text}")
#     print(f"String Content: {element.string}")
#     print(f"Parent: {element.parent}")
#     print(f"Children:")
#     pprint.pprint(list(element.children)) 

if __name__ == '__main__':
    organizer = CategoryOrganizer()
    soup = get_content(FILE)
    items = soup.findAll('div', {"data-testid": "itemtile-stack"})
    for item in items:
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
