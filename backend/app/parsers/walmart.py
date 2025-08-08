import json
from bs4 import BeautifulSoup

class WalmartReceiptParser:
    def __init__(self, html: str):
        self.html = html

    def parse_items(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        items = soup.findAll('div', {"data-testid": "itemtile-stack"})
        if not items:
            raise ValueError("No items found in the Walmart receipt.")
        parsed_items = []
        for item in items:
            # Check if item is in the unavailable section
            # if item.find_parent('div', {"data-testid": "category-accordion-"}):
            #     continue

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
            parsed_items.append({
                'name': name,
                'price': price
            })
        return parsed_items
    
    def to_json(self):
        return json.dumps(self.parse_items(), indent=4)