import json

def load_orders(username):
    try:
        with open("data/orders.txt", "r") as f:
            all_orders = json.load(f)
            return {
                order_id: order
                for order_id, order in all_orders.items()
                if order.get("system_user") == username  # Consistent tracking
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def order_tracking(current_user):
    if not current_user:
        print("Please login first")
        return current_user

    orders = load_orders(current_user)

    if not orders:
        print("\nNo orders found for your account!")
        print("Debug: Current user is", current_user)
        input("Press Enter to continue...")
        return current_user

    print(f"\n=== YOUR ORDER HISTORY ===")
    for order_id, order in sorted(orders.items(),
                                 key=lambda x: x[1]['timestamp'],
                                 reverse=True):
        print(f"\nOrder ID: {order_id}")
        print(f"Date: {order['timestamp']}")
        print(f"Type: {order['type']}")
        if order['type'] == "Dine-In":
            print(f"Table: {order['table_number']}")
        print("Items:")
        for item_id, qty in order['items']:
            print(f"  - {item_id} x{qty}")
        if order['remarks']:
            print(f"Remarks: {order['remarks']}")
        print("-" * 40)

    input("\nPress Enter to continue...")
    return current_user