# This file is mainly designed for managing restaurant orders, including creating new orders,
# adding items, applying and removing discounts or promo codes, processing checkouts, and
# handling active orders. It provides functions for order item management, discount logic,
# order status updates, and transaction processing in a point-of-sale system.

from .helpers import get_total_ordered_quantity, merge_order_items, calculate_order_total, generate_receipt
from .display import view_order_details, show_menu
from datetime import datetime
import json


def apply_discount_to_entire_order(order_id, current_orders, menu_items, discount_type):
    """Apply discount to the entire order"""
    # Calculate order total and existing discounts
    calc = calculate_order_total(order_id, current_orders, menu_items)
    order_total = calc['total']
    existing_discount = sum(d['amount'] for d in calc['discount_details'])
    remaining_value = order_total - existing_discount

    if discount_type == '1':  # Percentage discount
        try:
            percentage = float(
                input("Enter discount percentage for entire order (0-100): "))
            if percentage <= 0 or percentage > 100:
                print("Percentage must be between 0-100.")
                return

            discount_amount = min(
                order_total * percentage / 100, remaining_value)
            if discount_amount <= 0:
                print(
                    f"Cannot apply discount - order already fully discounted (remaining value: ${remaining_value:.2f})")
                return

            current_orders[order_id].setdefault("discounts", []).append({
                "type": "percentage",
                "value": percentage,
                "description": f"{percentage}% off entire order",
                "apply_to": "total",
                "amount": discount_amount
            })
            print(
                f"Applied {percentage}% discount to entire order (-${discount_amount:.2f})")

        except ValueError:
            print("Please enter a valid number.")

    else:  # Fixed amount discount
        try:
            amount = float(input(
                f"Enter fixed discount amount for entire order (max ${remaining_value:.2f}): "))
            if amount <= 0:
                print("Amount must be positive.")
                return
            if amount > remaining_value:
                print(
                    f"Discount cannot exceed remaining order value (${remaining_value:.2f})")
                return

            current_orders[order_id].setdefault("discounts", []).append({
                "type": "fixed",
                "value": amount,
                "description": f"${amount:.2f} off entire order",
                "apply_to": "total",
                "amount": amount
            })
            print(f"Applied ${amount:.2f} discount to entire order")

        except ValueError:
            print("Please enter a valid number.")

    calculate_order_total(order_id, current_orders,
                          menu_items, show_calculation=True)


def apply_discount_to_specific_item(order_id, current_orders, menu_items, discount_type):
    """Apply discount to a specific menu item"""
    print("\nCurrent Order Items:")
    for idx, (item_code, qty) in enumerate(current_orders[order_id]["items"], 1):
        item = menu_items[item_code]
        print(f"{idx}. {item['name']} - Qty: {qty}")

    try:
        item_idx = int(input("Enter item number to discount: ")) - 1
        if 0 <= item_idx < len(current_orders[order_id]["items"]):
            item_code = current_orders[order_id]["items"][item_idx][0]
            item_name = menu_items[item_code]['name']
            item_price = menu_items[item_code]['price']
            item_qty = current_orders[order_id]["items"][item_idx][1]
            item_total = item_price * item_qty

            existing_discount = sum(
                d['amount'] for d in current_orders[order_id].get("discounts", [])
                if d.get('item_code') == item_code
            )
            remaining_value = item_total - existing_discount

            if discount_type == '1':  # Percentage
                percentage = float(
                    input(f"Enter discount percentage for {item_name} (0-100): "))
                if percentage <= 0 or percentage > 100:
                    print("Percentage must be between 0-100.")
                    return

                discount_amount = min(
                    item_total * percentage / 100, remaining_value)
                if discount_amount <= 0:
                    print(
                        f"Cannot apply discount - item already fully    discounted (remaining value: ${remaining_value:.2f})")
                    return

                current_orders[order_id].setdefault("discounts", []).append({
                    "type": "percentage",
                    "value": percentage,
                    "description": f"{percentage}% off on {item_name}",
                    "apply_to": "specific_item",
                    "item_code": item_code,
                    "amount": discount_amount
                })
                print(
                    f"Applied {percentage}% discount to {item_name} (-${discount_amount:.2f})")

            else:  # Fixed amount
                amount = float(input(
                    f"Enter fixed discount amount for {item_name} (max ${remaining_value:.2f}): "))
                if amount <= 0:
                    print("Amount must be positive.")
                    return

                if amount > remaining_value:
                    print(
                        f"Discount cannot exceed remaining item value (${remaining_value:.2f})")
                    return

                current_orders[order_id].setdefault("discounts", []).append({
                    "type": "fixed",
                    "value": amount,
                    "description": f"${amount:.2f} off on {item_name}",
                    "apply_to": "specific_item",
                    "item_code": item_code,
                    "amount": amount
                })
                print(f"Applied ${amount:.2f} discount to {item_name}")

            calculate_order_total(order_id, current_orders,
                                  menu_items, show_calculation=True)
        else:
            print("Invalid item number!")
    except ValueError:
        print("Please enter valid numbers.")


def apply_promo_code(order_id, current_orders, menu_items, promo_codes):
    """Apply a promo code to the order"""
    promo_code = input("\nEnter promo code: ").strip().upper()
    if promo_code in promo_codes:
        promo = promo_codes[promo_code]

        # Check if promo already applied
        if any(d.get('promo_code') == promo_code for d in
               current_orders[order_id].get("discounts", [])):
            print("This promo code has already been applied.")
            return

        elif promo['apply_to'] == 'specific_item':
            item_code = promo.get('item_code')
            if not item_code or not any(item[0] == item_code for item in current_orders[order_id]["items"]):
                print(f"No valid item in order for this promo.")
                return
            item_total = sum(
                qty * menu_items[item_code]['price']
                for code, qty in current_orders[order_id]["items"]
                if code == item_code
            )
            existing_discount = sum(
                d['amount'] for d in current_orders[order_id].get("discounts", [])
                if d.get('item_code') == item_code
            )
            remaining_value = item_total - existing_discount

        elif promo['apply_to'] == 'total':
            calc = calculate_order_total(order_id, current_orders, menu_items)
            applicable_total = calc['total']
            existing_discount = sum(d['amount']
                                    for d in calc['discount_details'])
            remaining_value = applicable_total - existing_discount

        else:
            print("Invalid promo code application type.")
            return

        # Calculate the discount amount
        if promo['type'] == 'percentage':
            discount_amount = min(
                remaining_value * promo['value'] / 100, remaining_value)
        else:
            discount_amount = min(promo['value'], remaining_value)

        if discount_amount <= 0:
            print("No value left to discount for this promo.")
            return

        # Apply promo
        discount_entry = {
            "type": promo['type'],
            "value": promo['value'],
            "amount": discount_amount,
            "description": promo['description'],
            "apply_to": promo['apply_to'],
            "promo_code": promo_code
        }
        if promo['apply_to'] == 'specific_item':
            discount_entry['item_code'] = promo['item_code']

        current_orders[order_id].setdefault(
            "discounts", []).append(discount_entry)
        print(
            f"Applied promo: {promo['description']} (-${discount_amount:.2f})")
        calculate_order_total(order_id, current_orders,
                              menu_items, show_calculation=True)
    else:
        print("Invalid promo code.")


def apply_new_discount(order_id, current_orders, menu_items, promo_codes):
    """Apply a new discount to the order"""
    print("\nSelect Discount Type:")
    print("1. Percentage Discount")
    print("2. Fixed Amount Discount")
    print("3. Promo Code")
    discount_choice = input("Enter choice (1-3): ").strip()

    if discount_choice in ['1', '2']:
        print("\nApply discount to:")
        print("1. Specific food item")
        print("2. Entire order")
        apply_to = input("Enter choice (1-2): ").strip()

        if apply_to == '1':  # Specific item
            apply_discount_to_specific_item(
                order_id, current_orders, menu_items, discount_choice)
        elif apply_to == '2':
            apply_discount_to_entire_order(
                order_id, current_orders, menu_items, discount_choice)
        else:
            print("Invalid choice.")

    elif discount_choice == '3':  # Promo Code
        apply_promo_code(order_id, current_orders, menu_items, promo_codes)
    else:
        print("Invalid choice.")


def remove_existing_discount(order_id, current_orders, menu_items):
    """Remove an existing discount from the order"""
    if not current_orders[order_id].get("discounts"):
        print("No discounts applied to this order.")
        return

    print("\nApplied Discounts:")
    for idx, discount in enumerate(current_orders[order_id]["discounts"], 1):
        desc = discount['description']
        if discount.get('apply_to') == 'specific_item':
            item_name = menu_items[discount['item_code']]['name']
            desc = f"{discount['description']} on {item_name}"
        print(f"{idx}. {desc}")

    try:
        remove_idx = int(
            input("Enter discount number to remove (or 0 to cancel): ")) - 1
        if remove_idx == -1:
            return
        if 0 <= remove_idx < len(current_orders[order_id]["discounts"]):
            removed = current_orders[order_id]["discounts"].pop(remove_idx)
            print(f"Removed discount: {removed['description']}")
            calculate_order_total(order_id, current_orders,
                                  menu_items, show_calculation=True)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def manage_discounts(order_id, current_orders, menu_items, promo_codes):
    """Handle all discount operations for an order"""
    if order_id not in current_orders:
        print("No active order found!")
        return

    while True:
        print("\n=== Discount Management ===")
        print("1. Apply Discount")
        print("2. Remove Discount")
        print("3. Back to Order Actions")

        disc_choice = input("Select an option: ").strip()

        # Apply Discount
        if disc_choice == '1':
            apply_new_discount(order_id, current_orders,
                               menu_items, promo_codes)

        # Remove Discount
        elif disc_choice == '2':
            remove_existing_discount(order_id, current_orders, menu_items)

        # Back to Order Actions
        elif disc_choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")


def apply_items_to_order(order_id, current_orders, menu_items):
    """Add items to an existing order with quantity validation"""
    if order_id not in current_orders:
        print("No active order found!")
        return False

    show_menu(menu_items, current_orders)
    items_to_add = []

    while True:
        item_choice = input("Select item or 'done' to finish: ").strip()
        if item_choice.lower() == "done":
            break
        elif item_choice in menu_items:
            try:
                quantity = int(input("Quantity: "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    continue

                available = menu_items[item_choice]['available_quantity'] - \
                    get_total_ordered_quantity(item_choice, current_orders)
                if quantity > available:
                    print(
                        f"Only {available} available. Cannot order {quantity}.")
                    continue

                items_to_add.append((item_choice, quantity))
                print(
                    f"Added {quantity} {menu_items[item_choice]['name']} to order {order_id}.")
                show_menu(menu_items, current_orders)
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Invalid item choice!")

    if items_to_add:
        all_items = current_orders[order_id]["items"] + items_to_add
        current_orders[order_id]["items"] = merge_order_items(all_items)
        print("Items merged successfully.")
        return True
    return False


def create_new_order(current_orders, menu_items, dine_in_counter, take_away_counter):
    print("\nSelect Order Type:")
    print("1. Dine-In")
    print("2. Take Away")
    order_type = input("Enter choice (1 or 2): ").strip()

    if order_type == "1":
        order_id = f"D{dine_in_counter:02d}"
        dine_in_counter += 1
    elif order_type == "2":
        order_id = f"T{take_away_counter:02d}"
        take_away_counter += 1
    else:
        print("Invalid choice. Please try again.")
        return dine_in_counter, take_away_counter

    if order_id in current_orders:
        print(f"Order ID {order_id} already exists!")
        return dine_in_counter, take_away_counter

    show_menu(menu_items)
    items = []
    while True:
        item_choice = input("Select item or 'done' to finish: ").strip()
        if item_choice.lower() == "done":
            break
        elif item_choice in menu_items:
            try:
                quantity = int(input("Enter Quantity: "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    continue

                available = menu_items[item_choice]['available_quantity'] - \
                    get_total_ordered_quantity(item_choice, current_orders)
                if quantity > available:
                    print(
                        f"Only {available} available. Cannot order {quantity}.")
                    continue

                items.append((item_choice, quantity))
                show_menu(menu_items, current_orders)
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Invalid item choice!")

    if items:
        merged_items = merge_order_items(items)
        current_orders[order_id] = {
            "items": merged_items,
            "status": "Pending",
            "type": "Dine-In" if order_type == "1" else "Take Away",
            "discounts": []
        }
        print(f"Order {order_id} created successfully.")
    else:
        print("No items added. Order cancelled.")

    return dine_in_counter, take_away_counter


def process_checkout(order_id, order, current_orders, menu_items, transactions):
    print("\n=== Process Transaction ===")
    calc = calculate_order_total(order_id, current_orders, menu_items)

    print(f"\nProcessing Order {order_id} ({order['type']})")
    print("\nOrder Items:")
    for item_code, qty in order["items"]:
        item = menu_items[item_code]
        print(f"- {item['name']}: {qty} x ${item['price']}")

    if calc['discount_details']:
        print("\nDiscounts Applied:")
        for discount in calc['discount_details']:
            print(f"- {discount['description']}: -${discount['amount']:.2f}")

    print(f"\nSubtotal: ${calc['subtotal']:.2f}")
    print(f"Total Amount Due: ${calc['total']:.2f}")

    while True:
        payment_method = input(
            "\nEnter payment method (cash, card or touch n go) or 'cancel': ").strip().lower()
        if payment_method in ['touchngo', 'tng', 'touch-n-go', 'touchandgo', 'touch n go']:
            payment_method = 'touch n go'
            break
        if payment_method in ['cash', 'card']:
            break
        elif payment_method == 'cancel':
            print("Transaction cancelled.")
            return
        else:
            print("Invalid payment method. Please enter 'cash', 'card' or 'touch n go'.")

    transactions.append({
        "order_id": order_id,
        "type": order["type"],
        "items": order["items"],
        "subtotal": calc['subtotal'],
        "discounts": calc['discount_details'],
        "total": calc['total'],
        "payment_method": payment_method,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    generate_receipt(order_id, order, calc, payment_method, menu_items)
    del current_orders[order_id]


def handle_order_actions(order_id, order, current_orders, menu_items, transactions, promo_codes):
    while True:
        print("\nSelect An Option:")
        print("1. Apply Items")
        print("2. Manage Discount")
        print("3. Cancel Order")
        print("4. Checkout")
        print("5. Back ")

        action = input("\nEnter Choice: ")

        if action == "1":
            # Add items to order
            apply_items_to_order(order_id, current_orders, menu_items)

        elif action == "2":
            manage_discounts(order_id, current_orders, menu_items, promo_codes)

        elif action == "3":
            confirm = input(
                f"Confirm cancel order {order_id}? (y/n): ").lower()
            if confirm == 'y':
                del current_orders[order_id]
                print(f"Order {order_id} cancelled.")
                return
        elif action == "4":
            process_checkout(order_id, order, current_orders,
                             menu_items, transactions)
            return

        elif action == "5":
            return
        else:
            print("Invalid choice!")


def view_active_orders(_, menu_items, transactions, promo_codes):
    print("\n--- Active Orders from File ---")
    try:
        with open("data/orders.txt", "r") as file:
            for line in file:
                order = json.loads(line.strip())
                print(f"Order ID: {order['order_id']}")
                print(f"Type: {order['type']}")
                print("Items:")
                for item in order["items"]:
                    item_id = item["id"]
                    qty = item["quantity"]
                    item_name = menu_items[item_id]["name"] if item_id in menu_items else "Unknown"
                    print(f"  - {item_name} x {qty}")
                print("-" * 30)
    except FileNotFoundError:
        print("❌ No orders found.")
    except json.JSONDecodeError as e:
        print(f"❌ Error reading order: {e}")


def order_management(current_orders, transactions, menu_items, promo_codes, dine_in_counter, take_away_counter):
    while True:
        print("\n=== Order Menu ===")
        print("1. New Order")
        print("2. View Active Order")
        print("3. Back")

        ord_choice = input("Select an option: ").strip()

        if ord_choice == '1':
            dine_in_counter, take_away_counter = create_new_order(
                current_orders, menu_items, dine_in_counter, take_away_counter
            )
        elif ord_choice == '2':
            view_active_orders(current_orders, menu_items,
                               transactions, promo_codes)

        elif ord_choice == '3':
            break
        else:
            print("Invalid Choice. Please try again")

    return dine_in_counter, take_away_counter
