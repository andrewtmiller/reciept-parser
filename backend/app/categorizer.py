from app.organizer import CategoryOrganizer

def categorize_receipt(html: str):
    items = []
    # Very basic detection logic — improve as needed
    if any(domain in html.lower() for domain in ["walmart.com", "walmartimages.com"]):
        from app.parsers.walmart import WalmartReceiptParser
        walmart = WalmartReceiptParser(html)
        items = walmart.parse_items()
    elif "amazon.com" in html.lower():
        items = "Amazon"
        # items = amazon.parse(html)
    elif "costco.com" in html.lower():
        items = "Costco"
        # items = costco.parse(html)
    elif "bjs.com" in html.lower():
        items = "BJs"
        # items = bjs.parse(html)
    elif any(domain in html.lower() for domain in ["target.com", "targetimg1.com"]):
        from app.parsers.target import TargetReceiptParser
        print("Target!")
        parser = TargetReceiptParser(html)
        items = parser.to_json()
    else:
        raise ValueError("Store could not be identified.")

    # Here’s where you’d also categorize each item
    # For now, assume each parser returns already-categorized items
    if not items:
        raise ValueError("No items found in the receipt.")
    if isinstance(items, str):
        return items
    organizer = CategoryOrganizer()
    for item in items:
        if isinstance(item, dict) and 'name' in item and 'price' in item:
            organizer.organize_item(item['name'], item['price'])
        else:
            raise ValueError("Invalid item format. Each item should be a dictionary with 'name' and 'price' keys.")

    return organizer.get_summary()
