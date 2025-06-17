# display.py
# This file contains functions for displaying menus, promo codes, and order details
# in a formatted way for a restaurant ordering system.

# Constants for consistent formatting
MENU_WIDTH = 80
DETAILS_WIDTH = 50
PROMO_WIDTH = 80

# Column widths for menu display
MENU_COLS = {
    'code': 6,
    'name': 35,
    'price': 7,
    'category': 10,
    'status': 9
}

# Column widths for order details
ORDER_COLS = {
    'item': 30,
    'qty': 8,
    'price': 12,
    'desc': 15
}

def show_menu(menu_items, current_orders=None):
    """Display the menu with consistent formatting and alignment"""
    # Header
    print(f"\n{'=' * MENU_WIDTH}")
    print(f"{' MENU ':^{MENU_WIDTH}}")
    print(f"{'=' * MENU_WIDTH}")
    
    # Column headers
    print(f"{'Code':<{MENU_COLS['code']}} | "
          f"{'Name':<{MENU_COLS['name']}} | "
          f"{'Price':>{MENU_COLS['price']}} | "
          f"{'Category':<{MENU_COLS['category']}} | "
          f"{'Status':>{MENU_COLS['status']}}")
    print(f"{'-' * MENU_WIDTH}")

    # Menu items
    for code, item in menu_items.items():
        available = item['available_quantity']
        if current_orders:
            from helpers import get_total_ordered_quantity
            available -= get_total_ordered_quantity(code, current_orders)

        status = "Available" if available > 0 else "Sold Out"
        print(f"{code:<{MENU_COLS['code']}} | "
              f"{item['name']:<{MENU_COLS['name']}} | "
              f"${item['price']:>{MENU_COLS['price']-1}.2f} | "
              f"{item['category']:<{MENU_COLS['category']}} | "
              f"{status:>{MENU_COLS['status']}}")
    
    print(f"{'=' * MENU_WIDTH}")

def show_promo_codes(promo_codes):
    """Display promo codes with consistent formatting"""
    # Header
    print(f"\n{'=' * PROMO_WIDTH}")
    print(f"{' PROMO CODES ':^{PROMO_WIDTH}}")
    print(f"{'=' * PROMO_WIDTH}")
    # Column headers
    print(f"{'Code':<17} | "
          f"{'Type':<12} | "
          f"{'Value':<8} | "
          f"{'Description':<30}")
    print(f"{'-' * PROMO_WIDTH}")

    # Promo codes
    for code, promo in promo_codes.items():
        value_str = f"{promo['value']}%" if promo['type'] == 'percentage' else f"${promo['value']:.2f}"
        print(f"{code:<17} | "
              f"{promo['type']:<12} | "
              f"{value_str:<8} | "
              f"{promo.get('description', ''):<30}")
    
    print(f"{'=' * PROMO_WIDTH}")

def view_order_details(oid, order, menu_items):
    """Display order details with perfect alignment"""
    # Header section
    print(f"\n{'=' * DETAILS_WIDTH}")
    print(f"{' ORDER DETAILS ':-^{DETAILS_WIDTH}}")
    print(f"{'=' * DETAILS_WIDTH}")
    
    # Order info
    print(f"\n{'Order ID:':<{ORDER_COLS['desc']}}{oid}")
    print(f"{'Type:':<{ORDER_COLS['desc']}}{order['type']}")
    if order['type'] == 'Dine-In':
        print(f"{'Table:':<{ORDER_COLS['desc']}}{order.get('table_num', 'N/A')}")
    print(f"{'Placed:':<{ORDER_COLS['desc']}}{order.get('timestamp', 'N/A')}")
    
    # Items section
    print(f"\n{'-' * DETAILS_WIDTH}")
    print(f"{'Item':<{ORDER_COLS['item']}} "
          f"{'Qty':^{ORDER_COLS['qty']}} "
          f"{'Price':>{ORDER_COLS['price']}}")
    print(f"{'-' * DETAILS_WIDTH}")
    
    subtotal = 0
    for item_code, qty in order["items"]:
        item = menu_items[item_code]
        item_total = item['price'] * qty
        subtotal += item_total
        print(f"{item['name']:<{ORDER_COLS['item']}} "
              f"{f'x{qty}':^{ORDER_COLS['qty']}} "
              f"${item['price']:>{ORDER_COLS['price']-1}.2f}")
        
        if 'addons' in order and item_code in order['addons']:
            for addon_code, addon_qty in order['addons'][item_code]:
                addon = menu_items[addon_code]
                print(f"  + {addon['name']:<{ORDER_COLS['item']-2}} "
                      f"{f'x{addon_qty}':^{ORDER_COLS['qty']}}")
    
    # Discounts section
    total = subtotal
    discount_amounts = []
    if order.get("discounts"):
        print(f"\n{'DISCOUNTS:':<{ORDER_COLS['item']}}")
        for discount in order["discounts"]:
            if discount["apply_to"] == "food":
                applicable = sum(item['price'] * qty for item_code, qty in order["items"] 
                              if menu_items[item_code]['category'] == 'food')
            elif discount["apply_to"] == "beverage":
                applicable = sum(item['price'] * qty for item_code, qty in order["items"] 
                              if menu_items[item_code]['category'] == 'beverage')
            else:
                applicable = subtotal
            
            amount = applicable * discount["value"] / 100 if discount["type"] == "percentage" else discount["value"]
            discount_amounts.append(amount)
            total -= amount
            print(f"- {discount['description']:<{ORDER_COLS['item']-2}} "
                  f"-${amount:>{ORDER_COLS['price']-3}.2f}")
    
    # Totals section
    print(f"\n{'=' * DETAILS_WIDTH}")
    print(f"{'Subtotal:':<{ORDER_COLS['item']}} "
          f"${subtotal:>{ORDER_COLS['price']-1}.2f}")
    if discount_amounts:
        print(f"{'Total discounts:':<{ORDER_COLS['item']}} "
              f"-${sum(discount_amounts):>{ORDER_COLS['price']-3}.2f}")
    print(f"{'=' * DETAILS_WIDTH}")
    print(f"{'TOTAL DUE:':<{ORDER_COLS['item']}} "
          f"${total:>{ORDER_COLS['price']-1}.2f}")
    print(f"{'=' * DETAILS_WIDTH}")
    
    # Status
    print(f"\n{'Status:':<{ORDER_COLS['desc']}}"
          f"{order.get('status', 'PREPARING').capitalize()}")