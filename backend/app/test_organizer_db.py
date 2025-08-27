from organizer import CategoryOrganizer

if __name__ == "__main__":
    org = CategoryOrganizer()
    org.organize_item("shampoo", 5.99)
    org.organize_item("t-shirt", 12.50)
    org.organize_item("apple", 1.25)
    org.organize_item("unknown item", 3.00)
    summary = org.get_summary()
    for category, data in summary.items():
        print(f"Category: {category}")
        print(f"  Total Price: {data['total_price']}")
        for item in data['items']:
            print(f"    - {item['name']}: ${item['price']}")
