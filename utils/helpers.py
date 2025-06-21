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

def generate_receipt_lines(order_id, order, calc, payment_method, menu_items):
    lines = []
    
    # Constants for receipt formatting
    RECEIPT_WIDTH = 80
    ITEM_NAME_WIDTH = 47
    QTY_WIDTH = 10
    PRICE_WIDTH = 10
    TOTAL_COL_WIDTH = 10
    
    # Header
    lines.append("=" * RECEIPT_WIDTH)
    lines.append(f"{'RECEIPT':^{RECEIPT_WIDTH}}")
    lines.append("=" * RECEIPT_WIDTH)
    lines.append(f"Order ID: {order_id}")
    lines.append(f"Type: {order.get('type', 'N/A')}")
    
    # Timestamp handling
    order_timestamp = order.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    lines.append(f"Date: {order_timestamp}")
    
    # Payment Method
    if payment_method:
        lines.append(f"Payment Method: {payment_method.title()}")
    
    lines.append("-" * RECEIPT_WIDTH)
    
    # Items header
    lines.append(f"{'Item':<{ITEM_NAME_WIDTH}} {'Qty':^{QTY_WIDTH}} {'Price':>{PRICE_WIDTH}} {'Total':>{TOTAL_COL_WIDTH}}")
    lines.append("-" * RECEIPT_WIDTH)
    
    subtotal = 0
    for item_code, qty in order.get("items", []):
        item = menu_items.get(item_code)
        if not item:
            lines.append(f"ERROR: Item '{item_code}' not found in menu. Skipping.")
            continue

        line_total = qty * item['price']
        subtotal += line_total
        lines.append(
            f"{item['name']:<{ITEM_NAME_WIDTH}} "
            f"{qty:^{QTY_WIDTH}} "
            f"${item['price']:>{PRICE_WIDTH-1}.2f} "
            f"${line_total:>{TOTAL_COL_WIDTH-1}.2f}"
        )
    
    # Totals section with perfect right-alignment
    lines.append("=" * RECEIPT_WIDTH)
    lines.append(f"{'Subtotal:':<{RECEIPT_WIDTH-TOTAL_COL_WIDTH}}${subtotal:>{TOTAL_COL_WIDTH-1}.2f}")
    
    total_discount = sum(d.get('amount', 0) for d in order.get('discounts', []))
    if total_discount > 0:
        lines.append(f"{'Discount:':<{RECEIPT_WIDTH-TOTAL_COL_WIDTH-1}}-${total_discount:>{TOTAL_COL_WIDTH-1}.2f}")
    
    lines.append("-" * RECEIPT_WIDTH)
    final_total = subtotal - total_discount
    lines.append(f"{'Total Amount Due:':<{RECEIPT_WIDTH-TOTAL_COL_WIDTH}}${final_total:>{TOTAL_COL_WIDTH-1}.2f}")
    lines.append("-" * RECEIPT_WIDTH)
    lines.append("=" * RECEIPT_WIDTH)
    
    return lines

def generate_receipt(order_id, order, calc, payment_method, menu_items):
    receipt_lines = [
        "=== Receipt ===",
        f"Order ID: {order_id}",
        f"Order Type: {order['type']}",
        "",
        "Items:"
    ]

    for item_code, qty in order["items"]:
        item = menu_items.get(item_code, {"name": "Unknown", "price": 0.0})
        receipt_lines.append(f"- {item['name']}: {qty} x ${item['price']:.2f}")

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

    os.makedirs("receipts", exist_ok=True)
    receipt_filename = os.path.join("receipts", f"receipt_{order_id}.txt")
    with open(receipt_filename, "w", encoding="utf-8") as f:
        f.write(receipt_text)

    print(f"Receipt saved to {receipt_filename}")

def save_order_receipts(orders, menu_items, filepath="data/receipt.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    receipt_data = {}

    for order_id, order in orders.items():
        items = []
        for item_code, qty in order.get("items", []):
            item = menu_items.get(item_code, {"name": f"[Unknown: {item_code}]", "price": 0})
            items.append({
                "name": item["name"],
                "code": item_code,
                "quantity": qty,
                "price_each": item["price"],
                "subtotal": round(item["price"] * qty, 2)
            })

        total_price = sum(i["subtotal"] for i in items)

        receipt_data[order_id] = {
            "status": order.get("status", "Pending"),
            "type": order.get("type", "N/A"),
            "timestamp": order.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "table_number": order.get("table_number", None),
            "remarks": order.get("remarks", ""),
            "system_user": order.get("system_user", "guest"),
            "items": items,
            "total": round(total_price, 2)
        }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(receipt_data, f, indent=4)
