def display_menu_by_category(menu, category):
    print(f"\n=== {category.upper()} ===")
    for item_id, item in menu.items():
        if item['category'] == category:
            print(f"\n{item_id}. {item['name']} - RM{item['base_price']:.2f}")
            if item.get('contents'):
                print("   Includes:")
                for content_id, qty in item['contents'].items():
                    print(f"   - {qty}x {menu[content_id]['name']}")
            if item.get('ingredients'):
                print("   Customizable: Yes")


def product_browsing(menu):
    while True:
        print("\n=== BROWSE MENU ===")
        print("1. Burgers")
        print("2. Sides")
        print("3. Drinks")
        print("4. Set Meals")
        print("5. Back")

        choice = input("Choose category (1-5): ")

        categories = {
            "1": "Burgers",
            "2": "Sides",
            "3": "Drinks",
            "4": "Meals"
        }

        if choice in categories:
            display_menu_by_category(menu, categories[choice])
        elif choice == "5":
            break
        else:
            print("Invalid choice")

        input("\nPress Enter to continue...")