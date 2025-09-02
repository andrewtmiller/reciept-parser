from app.organizer import CategoryOrganizer


def categorize_receipt(html: str):
    items = []
    # Very basic detection logic — improve as needed
    if any(domain in html.lower() for domain in ["walmart.com", "walmartimages.com"]):
        from app.parsers.walmart import WalmartReceiptParser

        walmart = WalmartReceiptParser(html)
        store = "Walmart"
        items = walmart.parse_items()
        logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Walmart_spark_%282025%29.svg/1280px-Walmart_spark_%282025%29.svg.png"
    elif "amazon.com" in html.lower():
        items = "Amazon"
        store = "Amazon"
        # items = amazon.parse(html)
    elif "costco.com" in html.lower():
        from app.parsers.costco import CostcoReceiptParser

        costco = CostcoReceiptParser(html)
        logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Costco_Wholesale_logo_2010-10-26.svg/1280px-Costco_Wholesale_logo_2010-10-26.svg.png"
        store = "Costco"
        items = costco.parse_items()
    elif "bjs-universal-app" in html.lower():
        from app.parsers.bjs import BJsReceiptParser

        bjs = BJsReceiptParser(html)
        logo = "https://www.bjs.com/assets/images/icons/BJsNewLogo.svg"
        items = "BJs"
        store = "BJs"
        items = bjs.parse_items()
    elif any(domain in html.lower() for domain in ["target.com", "targetimg1.com"]):
        from app.parsers.target import TargetReceiptParser

        store = "Target"
        logo = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Target_logo.svg"
        parser = TargetReceiptParser(html)
        items = parser.parse_items()

    elif any(domain in html.lower() for domain in ["lowes.com"]):
        store = "Lowe's"
        logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Lowe%27s_logo.svg/1280px-Lowe%27s_logo.svg.png"
        from app.parsers.lowes import LowesReceiptParser

        parser = LowesReceiptParser(html)
        items = parser.parse_items()
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
        if isinstance(item, dict) and "name" in item and "price" in item:
            organizer.organize_item(item["name"], item["price"])
        else:
            raise ValueError(
                "Invalid item format. Each item should be a dictionary with 'name' and 'price' keys."
            )

    # Return the summary of categorized items
    return {
        "store": store,
        "logo": logo if "logo" in locals() else None,
        "categories": organizer.get_summary(),
    }
