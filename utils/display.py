"""
display.py
Functions for displaying menus, promo codes, and order details in a restaurant system.
"""

from datetime import datetime
from .helpers import get_total_ordered_quantity

# ==============================================
# CONSTANTS FOR FORMATTING
# ==============================================

# Display widths
MENU_WIDTH = 80
DETAILS_WIDTH = 50
PROMO_WIDTH = 80
REPORT_WIDTH = 80

# Column configurations
COLUMN_CONFIGS = {
    'menu': {
        'code': 6,
        'name': 35,
        'price': 7,
        'category': 10,
        'status': 9
    },
    'order': {
        'item': 30,
        'qty': 8,
        'price': 12,
        'desc': 15
    },
    'report': {
        'label': 50,
        'value': 25,
        'transaction': {
            'id': 4,
            'order_id': 8,
            'payment': 10,
            'amount': 15
        }
    }
}

# ==============================================
# CORE DISPLAY FUNCTIONS
# ==============================================

def show_menu(menu_items, current_orders=None):
    """Display the menu with consistent formatting and availability."""
    # Header section
    _print_section_header("MENU", MENU_WIDTH)
    
    # Column headers
    cols = COLUMN_CONFIGS['menu']
    print(f"{'Code':<{cols['code']}} | "
          f"{'Name':<{cols['name']}} | "
          f"{'Price':>{cols['price']}} | "
          f"{'Category':<{cols['category']}} | "
          f"{'Status':>{cols['status']}}")
    print("-" * MENU_WIDTH)

    # Menu items
    for code, item in menu_items.items():
        available = _calculate_available_quantity(item, code, current_orders)
        status = "Available" if available > 0 else "Sold Out"
        
        print(f"{code:<{cols['code']}} | "
              f"{item['name']:<{cols['name']}} | "
              f"${item['price']:>{cols['price']-1}.2f} | "
              f"{item['category']:<{cols['category']}} | "
              f"{status:>{cols['status']}}")
    
    print("=" * MENU_WIDTH)

def show_promo_codes(promo_codes):
    """Display promo codes with consistent formatting."""
    _print_section_header("PROMO CODES", PROMO_WIDTH)
    
    # Column headers
    print(f"{'Code':<17} | {'Type':<12} | {'Value':<8} | {'Description':<30}")
    print("-" * PROMO_WIDTH)

    # Promo items
    for code, promo in promo_codes.items():
        value_str = f"{promo['value']}%" if promo['type'] == 'percentage' else f"${promo['value']:.2f}"
        print(f"{code:<17} | {promo['type']:<12} | {value_str:<8} | {promo.get('description', ''):<30}")
    
    print("=" * PROMO_WIDTH)

# ==============================================
# ORDER DISPLAY FUNCTIONS
# ==============================================

def view_order_details(order_id, order, menu_items):
    """Display detailed breakdown of a single order with perfect alignment."""
    _print_section_header("ORDER DETAILS", DETAILS_WIDTH)
    
    # Order metadata
    _print_order_metadata(order_id, order)
    
    # Items section
    _print_order_items(order, menu_items)
    
    # Discounts and totals
    subtotal, total = _print_order_totals(order, menu_items)
    
    # Status
    print(f"\n{'Status:':<{COLUMN_CONFIGS['order']['desc']}}"
          f"{order.get('status', 'Preparing').capitalize()}")

# ==============================================
# REPORT FUNCTIONS
# ==============================================

def daily_sales_report(transactions, menu_items):
    """Generate a professional daily sales report with perfect alignment."""
    _print_section_header("DAILY SALES REPORT", REPORT_WIDTH)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    # Calculate report data
    report_data = _calculate_report_data(transactions, menu_items)
    
    # Financial summary
    _print_financial_summary(report_data)
    
    # Payment and order type breakdown
    _print_breakdowns(report_data)
    
    # Top selling items
    _print_top_items(report_data['top_items'], menu_items)
    
    # Transaction details
    _print_transaction_details(transactions, menu_items)

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def _print_section_header(title, width):
    """Print a consistent section header."""
    print(f"\n{'=' * width}")
    print(f"{f' {title} ':^{width}}")
    print(f"{'=' * width}")

def _calculate_available_quantity(item, code, current_orders):
    """Calculate available quantity considering current orders."""
    available = item['available_quantity']
    if current_orders:
        try:
            available -= get_total_ordered_quantity(code, current_orders)
        except ImportError:
            pass  # Fallback if helper function not available
    return available

def _print_order_metadata(order_id, order):
    """Print order metadata section."""
    cols = COLUMN_CONFIGS['order']
    print(f"\n{'Order ID:':<{cols['desc']}}{order_id}")
    print(f"{'Type:':<{cols['desc']}}{order['type']}")
    
    if order['type'] == 'Dine-In':
        print(f"{'Table:':<{cols['desc']}}{order.get('table_num', 'N/A')}")
    
    print(f"{'Placed:':<{cols['desc']}}{order.get('timestamp', 'N/A')}")

def _print_order_items(order, menu_items):
    """Print order items section."""
    cols = COLUMN_CONFIGS['order']
    print(f"\n{'-' * DETAILS_WIDTH}")
    print(f"{'Item':<{cols['item']}} {'Qty':^{cols['qty']}} {'Price':>{cols['price']}}")
    print(f"{'-' * DETAILS_WIDTH}")
    
    for item_code, qty in order["items"]:
        item = menu_items.get(item_code)
        if not item:
            print(f"Warning: Item code '{item_code}' not found. Skipping.")
            continue
        
        print(f"{item['name']:<{cols['item']}} {f'x{qty}':^{cols['qty']}} ${item['price']:>{cols['price']-1}.2f}")
        
        # Display addons if present
        if 'addons' in order and item_code in order['addons']:
            for addon_code, addon_qty in order['addons'][item_code]:
                addon = menu_items.get(addon_code)
                if addon:
                    print(f"  + {addon['name']:<{cols['item']-2}} "
                          f"{f'x{addon_qty}':^{cols['qty']}} "
                          f"${addon['price']:>{cols['price']-1}.2f}")

def _print_order_totals(order, menu_items):
    """Print order totals section and return subtotal, total."""
    cols = COLUMN_CONFIGS['order']
    
    # Calculate subtotal
    subtotal = sum(
        menu_items[code]['price'] * qty 
        for code, qty in order["items"] 
        if code in menu_items
    )
    
    # Calculate discounts
    discount_amounts = []
    if order.get("discounts"):
        print(f"\n{'DISCOUNTS:':<{cols['item']}}")
        for discount in order["discounts"]:
            amount = _calculate_discount_amount(discount, order, menu_items, subtotal)
            discount_amounts.append(amount)
            print(f"- {discount.get('description', 'Unknown Discount'):<{cols['item']-2}} "
                  f"-${amount:>{cols['price']-3}.2f}")
    
    total = subtotal - sum(discount_amounts)
    
    # Print totals
    print(f"\n{'=' * DETAILS_WIDTH}")
    print(f"{'Subtotal:':<{cols['item']}} ${subtotal:>{cols['price']-1}.2f}")
    if discount_amounts:
        print(f"{'Total discounts:':<{cols['item']}} -${sum(discount_amounts):>{cols['price']-3}.2f}")
    print(f"{'=' * DETAILS_WIDTH}")
    print(f"{'TOTAL DUE:':<{cols['item']}} ${total:>{cols['price']-1}.2f}")
    print(f"{'=' * DETAILS_WIDTH}")
    
    return subtotal, total

def _calculate_discount_amount(discount, order, menu_items, subtotal):
    """Calculate discount amount based on discount type and application."""
    applicable = 0
    apply_to = discount.get("apply_to", "")
    
    if apply_to == "food":
        applicable = sum(
            menu_items[code]['price'] * qty 
            for code, qty in order["items"] 
            if menu_items.get(code, {}).get('category') == 'food'
        )
    elif apply_to == "beverage":
        applicable = sum(
            menu_items[code]['price'] * qty 
            for code, qty in order["items"] 
            if menu_items.get(code, {}).get('category') == 'beverage'
        )
    else:  # Applies to subtotal
        applicable = subtotal
    
    if discount.get("type") == "percentage":
        return applicable * discount.get("value", 0) / 100
    elif discount.get("type") == "fixed":
        return discount.get("value", 0)
    return 0

def _calculate_report_data(transactions, menu_items):
    """Calculate all data needed for the sales report."""
    # Payment breakdown
    payment_types = {
        'cash': {'total': 0, 'count': 0},
        'card': {'total': 0, 'count': 0},
        'touch n go': {'total': 0, 'count': 0}
    }
    
    # Initialize other metrics
    total_sales = 0
    total_discounts = 0
    item_sales = {}
    
    for t in transactions:
        # Update totals
        total_sales += t['total']
        total_discounts += (t.get('subtotal', t['total']) - t['total'])
        
        # Update payment types
        payment_method = t.get('payment_method')
        if payment_method in payment_types:
            payment_types[payment_method]['total'] += t['total']
            payment_types[payment_method]['count'] += 1
        
        # Update item sales
        for item_code, qty in t.get('items', []):
            item_sales[item_code] = item_sales.get(item_code, 0) + qty
    
    # Order type breakdown
    dine_in = [t for t in transactions if t.get('type') == 'Dine-In']
    take_away = [t for t in transactions if t.get('type') == 'Take Away']
    
    return {
        'total_sales': total_sales,
        'total_discounts': total_discounts,
        'order_count': len(transactions),
        'payment_types': payment_types,
        'dine_in': {
            'count': len(dine_in),
            'total': sum(t['total'] for t in dine_in)
        },
        'take_away': {
            'count': len(take_away),
            'total': sum(t['total'] for t in take_away)
        },
        'top_items': sorted(item_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    }

def _print_financial_summary(report_data):
    """Print the financial summary section of the report."""
    cols = COLUMN_CONFIGS['report']
    _print_section_header("Financial Summary", REPORT_WIDTH)
    
    print(f"{'Total Discounts Given:':<{cols['label']}}${report_data['total_discounts']:>{cols['value']-1}.2f}")
    print(f"{'Total Sales Amount:':<{cols['label']}}${report_data['total_sales']:>{cols['value']-1}.2f}")
    print(f"{'Total Orders:':<{cols['label']}}{report_data['order_count']:>{cols['value']}}")

def _print_breakdowns(report_data):
    """Print payment and order type breakdowns."""
    cols = COLUMN_CONFIGS['report']
    
    # Payment breakdown
    print("\nBreakdown by Payment Method:")
    for method, data in report_data['payment_types'].items():
        print(f"{f'    - {method.title()}:':<{cols['label']}}${data['total']:>{cols['value']-1}.2f}")
    
    # Order type breakdown
    print("\nBreakdown by Order Type:")
    dine_in_text = f"({report_data['dine_in']['count']:>8} order{'s' if report_data['dine_in']['count'] != 1 else ''})"
    take_away_text = f"({report_data['take_away']['count']:>8} order{'s' if report_data['take_away']['count'] != 1 else ''})"
    
    print(f"{'    - Dine-In:':<{cols['label']-15}}{dine_in_text:>15}${report_data['dine_in']['total']:>{cols['value']-1}.2f}")
    print(f"{'    - Take Away:':<{cols['label']-15}}{take_away_text:>15}${report_data['take_away']['total']:>{cols['value']-1}.2f}")

def _print_top_items(top_items, menu_items):
    """Print top selling items section."""
    if not top_items:
        return
    
    cols = COLUMN_CONFIGS['report']
    _print_section_header("Top Selling Items", REPORT_WIDTH)
    
    for i, (item_code, qty) in enumerate(top_items, 1):
        item_name = menu_items.get(item_code, {}).get('name', f'Unknown Item ({item_code})')
        print(f"{f'{i}. {item_name}':<{cols['label']}}{qty:>{cols['value']}} units")

def _print_transaction_details(transactions, menu_items):
    """Print transaction details with interactive viewing."""
    _print_section_header("Transaction Details", REPORT_WIDTH)
    
    # Calculate dynamic column widths
    trans_cols = COLUMN_CONFIGS['report']['transaction']
    max_order_id = max(len(t['order_id']) for t in transactions) if transactions else trans_cols['order_id']
    max_payment = max(len(t['payment_method']) for t in transactions) if transactions else trans_cols['payment']
    
    order_id_width = max(trans_cols['order_id'], max_order_id)
    payment_width = max(trans_cols['payment'], max_payment)
    
    # Header
    print(f"{'#':<{trans_cols['id']}} {'Order ID':<{order_id_width}} "
          f"{'Payment':<{payment_width}} {'Amount':>{trans_cols['amount']}}")
    
    # Transaction rows
    for i, trans in enumerate(transactions, 1):
        print(f"{f'[{i}]:':<{trans_cols['id']}}{trans['order_id']:<{order_id_width}} "
              f"{trans['payment_method'].title():<{payment_width}} "
              f"${trans['total']:>{trans_cols['amount']-1}.2f}")
    
    # Interactive details
    while True:
        choice = input("\nEnter Order Number to view details or 'done' to exit: ")
        if choice.lower() == 'done':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(transactions):
                temp_order = {
                    'items': transactions[idx]['items'],
                    'type': transactions[idx]['type'],
                    'discounts': [],
                    'status': 'COMPLETED'
                }
                view_order_details(transactions[idx]['order_id'], temp_order, menu_items)
        except ValueError:
            print("Please enter a valid number or 'done'")

 
def daily_sales_report(transactions, menu_items):
    """Generate a professional daily sales report with perfect number alignment"""
    # Constants for consistent formatting
    REPORT_WIDTH = 80
    LABEL_WIDTH = 60  # Fixed width for all labels
    VALUE_WIDTH = 20  # Fixed width for all values
    
    # Header
    print("\n" + "=" * REPORT_WIDTH)
    print(f"{'DAILY SALES REPORT':^{REPORT_WIDTH}}")
    print("=" * REPORT_WIDTH)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d')}")

    # Calculate totals
    total_sales = sum(t['total'] for t in transactions)
    total_discounts = sum(t['subtotal'] - t['total'] for t in transactions)
    order_count = len(transactions)
    
    # Payment breakdown
    payment_types = {
        'cash': {'total': 0, 'count': 0},
        'card': {'total': 0, 'count': 0},
        'touch n go': {'total': 0, 'count': 0}
    }
    
    for t in transactions:
        payment_method = t['payment_method']
        if payment_method not in payment_types:
            print(f"Warning: Unknown payment method '{t['payment_method']}' found")
            continue
        payment_types[t['payment_method']]['total'] += t['total']
        payment_types[t['payment_method']]['count'] += 1
    
    # Order type breakdown
    dine_in = [t for t in transactions if t['type'] == 'Dine-In']
    take_away = [t for t in transactions if t['type'] == 'Take Away']
    
    # Top selling items
    item_sales = {}
    for t in transactions:
        for item_code, qty in t['items']:
            item_sales[item_code] = item_sales.get(item_code, 0) + qty
    
    top_items = sorted(item_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # ==================== Financial Summary ====================
    print("\n" + "-" * REPORT_WIDTH)
    print(f"{'Financial Summary':^{REPORT_WIDTH}}")
    print("-" * REPORT_WIDTH)
    
    # Perfectly aligned financial data - numbers right-aligned
    print(f"{'Total Discounts Given:':<{LABEL_WIDTH}}${total_discounts:>{VALUE_WIDTH-1}.2f}")
    print(f"{'Total Sales Amount:':<{LABEL_WIDTH}}${total_sales:>{VALUE_WIDTH-1}.2f}")
    print(f"{'Total Orders:':<{LABEL_WIDTH}}{order_count:>{VALUE_WIDTH}}")
    
    # Payment breakdown with perfect alignment
    print("\nBreakdown by Payment Method:")
    print(f"{'    - Cash:':<{LABEL_WIDTH}}${payment_types['cash']['total']:>{VALUE_WIDTH-1}.2f}")
    print(f"{'    - Card:':<{LABEL_WIDTH}}${payment_types['card']['total']:>{VALUE_WIDTH-1}.2f}")
    print(f"{'    - Touch N Go:':<{LABEL_WIDTH}}${payment_types['touch n go']['total']:>{VALUE_WIDTH-1}.2f}")
    
    # Order type breakdown with perfect alignment
    print("\nBreakdown by Order Type:")
    dine_in_count = len(dine_in)
    take_away_count = len(take_away)
    dine_in_total = sum(t['total'] for t in dine_in)
    take_away_total = sum(t['total'] for t in take_away)
    
    dine_in_text = f"({dine_in_count:>8} order{'s' if dine_in_count != 1 else '':>1})"
    take_away_text = f"({take_away_count:>8} order{'s' if take_away_count != 1 else '':>1})"
    
    print(f"{'    - Dine-In:':<{LABEL_WIDTH-20}}{dine_in_text:>20}${dine_in_total:>{VALUE_WIDTH-1}.2f}")
    print(f"{'    - Take Away:':<{LABEL_WIDTH-20}}{take_away_text:>20}${take_away_total:>{VALUE_WIDTH-1}.2f}")
    
    # ==================== Top Selling Items ====================
    if top_items:
        print("\n" + "-" * REPORT_WIDTH)
        print(f"{'Top Selling Items':^{REPORT_WIDTH}}")
        print("-" * REPORT_WIDTH)
        
        for i, (item_code, qty) in enumerate(top_items, 1):
            item_name = menu_items[item_code]['name']
            print(f"{f'{i}. {item_name}':<{LABEL_WIDTH}}{qty:>{VALUE_WIDTH-6}} units")
    
    # ==================== Transaction Details ====================
    print("\n" + "=" * REPORT_WIDTH)
    print(f"{'Transaction Details':^{REPORT_WIDTH}}")
    print("=" * REPORT_WIDTH)
    
    # Calculate column widths (with minimums)
    col_widths = {
        'num': 6,        # For the # column (e.g., "1", "10")
        'id': 15,
        'payment': 17,
        'type': 20,      # "Dine In"/"Take Away"
        'amount': 12     # For currency values
    }

    # Apply minimum widths
    col_widths['id'] = max(col_widths['id'], 8)
    col_widths['payment'] = max(col_widths['payment'], 10)

    # Header row
    header = (
        f"{'#':<{col_widths['num']}}  "
        f"{'Order ID':<{col_widths['id']}}  "
        f"{'Payment':<{col_widths['payment']}}  "
        f"{'Type':<{col_widths['type']}}  "
        f"{'Amount':>{col_widths['amount']}}"
    )
    print(header)
    print("-" * REPORT_WIDTH)
    print("=" * REPORT_WIDTH)
    
    # Transaction rows with perfect alignment - amounts right-aligned
    for i, trans in enumerate(transactions, 1):
        row = (
            f"{i:<{col_widths['num']}}  "
            f"{trans['order_id']:<{col_widths['id']}}  "
            f"{trans['payment_method'].title():<{col_widths['payment']}}  "
            f"{trans['type'].replace('-', ' ').title():<{col_widths['type']}}  "
            f"$ {(trans['total']):>{col_widths['amount']}}"
        )
        print(row)

    # Interactive section
    print("-" * REPORT_WIDTH)

    # Interactive order details
    while True:
        choice = input("\nEnter Order Number to view details or 'done' to exit: ")
        if choice.lower() == 'done':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(transactions):
                temp_order = {
                    'items': transactions[idx]['items'],
                    'type': transactions[idx]['type'],
                    'discounts': [],
                    'status': 'Completed'
                }
                view_order_details(transactions[idx]['order_id'], temp_order, menu_items)
            else:
                print("Invalid order number!")
        except ValueError:
            print("Please enter a valid number or 'done'")