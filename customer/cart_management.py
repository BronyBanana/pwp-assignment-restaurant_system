import os
from datetime import datetime


def load_cart(user):
    cart = []
    try:
        with open("data/carts.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|||")
                if parts[0] == user:
                    for item_str in parts[1:]:
                        try:
                            item = eval(item_str)
                            if not isinstance(item, dict):
                                continue
                            if 'remarks' not in item:
                                item['remarks'] = ''
                            cart.append(item)
                        except:
                            continue
                    break
    except (FileNotFoundError, SyntaxError):
        pass
    return cart


def save_cart(user, cart):
    os.makedirs("data", exist_ok=True)

    carts = {}
    try:
        with open("data/carts.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|||")
                if parts:
                    carts[parts[0]] = parts[1:]
    except FileNotFoundError:
        pass

    carts[user] = [str(item) for item in cart]

    with open("data/carts.txt", "w") as f:
        for username, items in carts.items():
            if username:
                f.write(f"{username}|||{'|||'.join(items)}\n")


def customize_item(menu_item, full_menu=None):
    item = {
        'id': menu_item.get('id'),
        'name': menu_item['name'],
        'price': menu_item['base_price'],
        'quantity': 1,
        'remarks': '',
        'type': 'combo' if 'contents' in menu_item else 'single',
        'drink_selections': {}  # New field to track custom drink selections
    }

    try:
        item['quantity'] = max(1, min(10, int(input("Quantity (1-10): "))))
    except ValueError:
        print("Invalid quantity. Using 1.")

    # Handle combo meals
    if item['type'] == 'combo' and full_menu:
        print(f"\nCustomizing {menu_item['name']} Combo")

        # Calculate total drinks needed and original drinks
        original_drinks = {}
        total_drinks = 0
        for content_id, qty in menu_item['contents'].items():
            if full_menu.get(content_id, {}).get('category') == 'Drinks':
                original_drinks[content_id] = {
                    'item': full_menu[content_id],
                    'quantity': qty
                }
                total_drinks += qty

        # Show combo contents
        print("Includes:")
        for content_id, qty in menu_item['contents'].items():
            content_item = full_menu.get(content_id, {})
            print(f"- {content_item.get('name', 'Unknown')} x{qty}")

        # Drink customization system
        if original_drinks:
            print(f"\nYou can customize {total_drinks} drink(s):")
            remaining_drinks = total_drinks
            drink_selections = {}
            all_drink_options = [d for d in full_menu.values() if d.get('category') == 'Drinks']

            while remaining_drinks > 0:
                print(f"\n{remaining_drinks} drink(s) remaining to select")
                print("Available drink options:")
                for i, drink in enumerate(all_drink_options, 1):
                    print(f"{i}. {drink['name']} (RM{drink['base_price']:.2f})")

                try:
                    drink_choice = int(input("Select drink (1-{}): ".format(len(all_drink_options)))) - 1
                    if 0 <= drink_choice < len(all_drink_options):
                        selected_drink = all_drink_options[drink_choice]
                        max_possible = min(remaining_drinks, 10)  # Max 10 of one type
                        qty = int(input(f"How many {selected_drink['name']} (1-{max_possible})? "))
                        qty = max(1, min(max_possible, qty))

                        # Add to selections
                        drink_id = [k for k, v in full_menu.items() if v == selected_drink][0]
                        if drink_id in drink_selections:
                            drink_selections[drink_id] += qty
                        else:
                            drink_selections[drink_id] = qty

                        remaining_drinks -= qty
                        print(f"Added {qty} {selected_drink['name']}")
                    else:
                        print("Invalid selection")
                except (ValueError, IndexError):
                    print("Invalid input")

            # Calculate price difference
            original_drink_cost = sum(d['item']['base_price'] * d['quantity']
                                      for d in original_drinks.values())
            new_drink_cost = sum(full_menu[did]['base_price'] * qty
                                 for did, qty in drink_selections.items())
            price_diff = new_drink_cost - original_drink_cost

            # Update item details
            item['price'] += price_diff
            item['drink_selections'] = drink_selections
            drink_desc = ", ".join([f"{full_menu[did]['name']} x{qty}"
                                    for did, qty in drink_selections.items()])
            item['name'] += f" (Drinks: {drink_desc})"

    # Handle regular item customization
    elif menu_item.get("ingredients"):
        print(f"\nCustomizing {menu_item['name']}")
        for ing, details in menu_item["ingredients"].items():
            if not details["default"] and input(f"Add {ing} (+RM{details['price']:.2f})? (y/n): ").lower() == 'y':
                item['price'] += details['price']
                item['name'] += f" +{ing}"

    item['remarks'] = input("Any special instructions for this item? (press enter to skip): ").strip()
    return item


def display_cart(cart):
    """Enhanced cart display showing combo contents"""
    if not cart:
        print("\nYour cart is empty")
        return

    print("\n=== YOUR CART ===")
    for idx, item in enumerate(cart, 1):
        remarks = item.get('remarks', '')
        remarks_str = f" [Remarks: {remarks}]" if remarks else ""

        if item.get('type') == 'combo':
            print(f"{idx}. COMBO: {item['name']} x{item['quantity']} - RM{item['price']:.2f}{remarks_str}")
        else:
            print(f"{idx}. {item['name']} x{item['quantity']} - RM{item['price']:.2f}{remarks_str}")

    total = sum(item['price'] * item['quantity'] for item in cart)
    print(f"\nTOTAL: RM{total:.2f}")


def checkout(current_user, cart):
    """Handle checkout with order remarks"""
    if not cart:
        print("Cannot checkout - cart is empty!")
        return False

    display_cart(cart)
    order_remarks = input("\nEnter order remarks (for the whole order): ").strip()

    order_data = {
        'user': current_user,
        'items': cart,
        'total': sum(item.get('price', 0) * item.get('quantity', 1) for item in cart),
        'datetime': str(datetime.now()),
        'remarks': order_remarks
    }

    os.makedirs("data", exist_ok=True)
    with open("data/orders.txt", "a") as f:
        f.write(f"{current_user}|||{cart}|||{order_data['total']}|||{order_data['datetime']}|||{order_remarks}\n")

    save_cart(current_user, [])
    print("\nOrder placed successfully!")
    if order_remarks:
        print(f"Order Remarks: {order_remarks}")
    return True


def cart_management(current_user, menu):
    """Updated to pass full menu to customize_item"""
    if not current_user:
        print("Please login first")
        return current_user

    cart = load_cart(current_user)

    while True:
        display_cart(cart)

        print("\nOPTIONS:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Edit Item Remarks")
        print("4. Checkout")
        print("5. Back")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            print("\nMENU ITEMS:")
            # Group by category
            categories = {}
            for item_id, item in menu.items():
                categories.setdefault(item['category'], []).append((item_id, item))

            for category, items in categories.items():
                print(f"\n{category.upper()}")
                for item_id, item in items:
                    print(f"{item_id}. {item['name']} - RM{item['base_price']:.2f}")

            item_id = input("\nEnter item ID: ").strip()
            if item_id in menu:
                item_data = {'id': item_id, **menu[item_id]}
                cart.append(customize_item(item_data, menu))  # Pass full menu
                save_cart(current_user, cart)
                print("Item added to cart!")
            else:
                print("Invalid item ID!")

        elif choice == "2":
            if not cart:
                print("Cart is empty!")
                continue

            try:
                idx = int(input("Enter item number to remove: ")) - 1
                if 0 <= idx < len(cart):
                    removed = cart.pop(idx)
                    save_cart(current_user, cart)
                    print(f"Removed {removed.get('name', 'item')}")
                else:
                    print("Invalid item number!")
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "3":
            if not cart:
                print("Cart is empty!")
                continue

            try:
                idx = int(input("Enter item number to edit remarks: ")) - 1
                if 0 <= idx < len(cart):
                    new_remarks = input("Enter new remarks: ").strip()
                    cart[idx]['remarks'] = new_remarks
                    save_cart(current_user, cart)
                    print("Remarks updated!")
                else:
                    print("Invalid item number!")
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "4":
            if checkout(current_user, cart):
                return current_user

        elif choice == "5":
            return current_user

        else:
            print("Invalid choice")