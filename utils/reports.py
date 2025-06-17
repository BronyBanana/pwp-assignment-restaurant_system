from display import view_order_details
from datetime import datetime

def daily_sales_report(transactions, menu_items):
    """Generate a professional daily sales report with perfect number alignment"""
    # Constants for consistent formatting
    REPORT_WIDTH = 80
    LABEL_WIDTH = 50  # Fixed width for all labels
    VALUE_WIDTH = 25  # Fixed width for all values
    
    # Header
    print("\n" + "=" * REPORT_WIDTH)
    print(f"{'DAILY SALES REPORT':^{REPORT_WIDTH}}")
    print("=" * REPORT_WIDTH)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d')}\n")
    
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
    
    print(f"{'    - Dine-In:':<{LABEL_WIDTH-15}}{dine_in_text:>15}${dine_in_total:>{VALUE_WIDTH-1}.2f}")
    print(f"{'    - Take Away:':<{LABEL_WIDTH-15}}{take_away_text:>15}${take_away_total:>{VALUE_WIDTH-1}.2f}")
    
    # ==================== Top Selling Items ====================
    if top_items:
        print("\n" + "-" * REPORT_WIDTH)
        print(f"{'Top Selling Items':^{REPORT_WIDTH}}")
        print("-" * REPORT_WIDTH)
        
        for i, (item_code, qty) in enumerate(top_items, 1):
            item_name = menu_items[item_code]['name']
            print(f"{f'{i}. {item_name}':<{LABEL_WIDTH}}{qty:>{VALUE_WIDTH}} units")
    
    # ==================== Transaction Details ====================
    print("\n" + "-" * REPORT_WIDTH)
    print(f"{'Transaction Details':^{REPORT_WIDTH}}")
    print("-" * REPORT_WIDTH)
    
    # Calculate dynamic column widths for transaction table
    max_order_id = max(len(t['order_id']) for t in transactions) if transactions else 8
    max_payment = max(len(t['payment_method']) for t in transactions) if transactions else 10
    
    TRANS_ID_WIDTH = 4
    TRANS_ORDER_WIDTH = max(8, max_order_id)
    TRANS_PAYMENT_WIDTH = max(10, max_payment)
    TRANS_AMOUNT_WIDTH = 15
    
    # Header with perfect alignment
    print(f"{'#':<{TRANS_ID_WIDTH}} {'Order ID':<{TRANS_ORDER_WIDTH}} {'Payment':<{TRANS_PAYMENT_WIDTH}} {'Amount':>{TRANS_AMOUNT_WIDTH}}")
    
    # Transaction rows with perfect alignment - amounts right-aligned
    for i, trans in enumerate(transactions, 1):
        order_display = f"[{i}]:"
        payment_display = trans['payment_method'].title()
        
        print(f"{order_display:<{TRANS_ID_WIDTH}}{trans['order_id']:<{TRANS_ORDER_WIDTH}} {payment_display:<{TRANS_PAYMENT_WIDTH}} ${trans['total']:>{TRANS_AMOUNT_WIDTH-1}.2f}")
    
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
                    'status': 'COMPLETED'
                }
                view_order_details(transactions[idx]['order_id'], temp_order, menu_items)
            else:
                print("Invalid order number!")
        except ValueError:
            print("Please enter a valid number or 'done'")