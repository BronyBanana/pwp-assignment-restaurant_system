# helpers.py provides utility functions 
# Helper functions for loading data, processing orders, calculating totals, and generating receipts

import json
import os
from datetime import datetime


def load_menu_items():
    try:
        with open(os.path.join("data", "menu_items.txt"), "r") as f:
            items_list = json.load(f)
            return {item["item_id"]: item for item in items_list}
    except FileNotFoundError:
        print("Error: data/menu_items.txt not found. Using empty menu.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error in data/menu_items.txt: {e}. Using empty menu.")
        return {}

def load_promo_codes():
    try:
        with open(os.path.join("data", "promo_codes.txt"), "r") as f:
            codes_list = json.load(f)
            return {item["code"]: item for item in codes_list}
    except FileNotFoundError:
        print("Error: data/promo_codes.txt not found. Using empty promo codes.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error in data/promo_codes.txt: {e}. Using empty promo codes.")
        return {}


def merge_order_items(items):
    merged_items = {}
    for item_code, qty in items:
        if item_code in merged_items:
            merged_items[item_code] += qty
        else:
            merged_items[item_code] = qty
    return [(code, qty) for code, qty in merged_items.items()]

def get_total_ordered_quantity(item_code, current_orders):
    total = 0
    for order in current_orders.values():
        for code, qty in order["items"]:
            if code == item_code:
                total += qty
    return total

def calculate_order_total(order_id, current_orders, menu_items, show_calculation=False):
    order = current_orders[order_id]
    subtotal = 0
    item_totals = {}

    for item_code, qty in order["items"]:
        price = menu_items[item_code]['price']
        item_total = price * qty
        item_totals[item_code] = item_total
        subtotal += item_total

    total = subtotal
    discount_details = []

    for discount in order.get("discounts", []):
        if discount["apply_to"] == "specific_item":
            item_code = discount["item_code"]
            if item_code in item_totals:
                item_total = item_totals[item_code]
                remaining_value = item_total - sum(
                    d['amount'] for d in discount_details
                    if d.get('item_code') == item_code
                )

                if discount["type"] == "percentage":
                    discount_amount = min(item_total * discount["value"] / 100, remaining_value)
                else:
                    discount_amount = min(discount["value"], remaining_value)

                if discount_amount > 0:
                    total -= discount_amount
                    discount_details.append({
                        'description': discount['description'],
                        'amount': discount_amount,
                        'item_code': item_code
                    })

        elif discount["apply_to"] in ["food", "beverage"]:
            applicable_total = sum(
                item_totals[code] for code in item_totals
                if menu_items[code]['category'] == discount["apply_to"]
            )

            if discount["type"] == "percentage":
                discount_amount = applicable_total * discount["value"] / 100
            else:
                discount_amount = discount["value"]

            discount_amount = min(discount_amount, total)
            if discount_amount > 0:
                total -= discount_amount
                discount_details.append({
                    'description': discount['description'],
                    'amount': discount_amount
                })

        else:
            if discount["type"] == "percentage":
                discount_amount = subtotal * discount["value"] / 100
            else:
                discount_amount = discount["value"]

            discount_amount = min(discount_amount, total)
            if discount_amount > 0:
                total -= discount_amount
                discount_details.append({
                    'description': discount['description'],
                    'amount': discount_amount
                })

    if show_calculation:
        print(f"\nOrder ID: {order_id} ({order['type']})")
        print("\nItems:")
        for item_code, qty in order["items"]:
            item = menu_items[item_code]
            print(f"- {item['name']}: {qty} x ${item['price']}")

        if discount_details:
            print("\nDiscounts Applied:")
            for discount in discount_details:
                print(f"- {discount['description']}: -${discount['amount']:.2f}")

        print(f"\nSubtotal: ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")

    return {
        'subtotal': subtotal,
        'total': total,
        'discount_details': discount_details,
        'item_totals': item_totals
    }

def generate_receipt(order_id, order, calc, payment_method, menu_items):
    receipt_lines = [
        "=== Receipt ===",
        f"Order ID: {order_id}",
        f"Order Type: {order['type']}",
        "",
        "Items:"
    ]
    for item_code, qty in order["items"]:
        item = menu_items[item_code]
        receipt_lines.append(f"- {item['name']}: {qty} x ${item['price']}")

    if calc['discount_details']:
        receipt_lines.append("\nDiscounts Applied:")
        for discount in calc['discount_details']:
            receipt_lines.append(f"- {discount['description']}: -${discount['amount']:.2f}")

    receipt_lines.extend([
        "",
        f"Subtotal: ${calc['subtotal']:.2f}",
        f"Total Amount Due: ${calc['total']:.2f}",
        f"Payment Method: {payment_method.capitalize()}",
        f"Transaction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "Thank you for your order!"
    ])

    receipt_text = "\n".join(receipt_lines)
    print(f"\n{receipt_text}")

    receipt_filename = f"receipt_{order_id}.txt"
    with open(receipt_filename, "w") as f:
        f.write(receipt_text)
    print(f"Receipt saved to {receipt_filename}")