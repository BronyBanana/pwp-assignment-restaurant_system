def load_orders(user):
    orders = []
    try:
        with open("data/orders.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|||")
                if len(parts) >= 5 and parts[0] == user:  # Check for remarks field
                    try:
                        orders.append({
                            "user": parts[0],
                            "items": eval(parts[1]),
                            "total": float(parts[2]),
                            "time": parts[3],
                            "remarks": parts[4] if len(parts) > 4 else ""
                        })
                    except:
                        continue
    except FileNotFoundError:
        pass
    return orders


def order_tracking(current_user):
    if not current_user:
        print("Please login first")
        return current_user

    orders = load_orders(current_user)

    if not orders:
        print("\nNo orders found!")
        return current_user

    print(f"\nOrder History for {current_user}:")
    for order in orders:
        print(f"\nOrder at {order['time']}")
        if order.get('remarks'):
            print(f"Remarks: {order['remarks']}")
        print("-" * 40)
        for item in order["items"]:
            name = item.get('display_name', item.get('name', 'Unknown Item'))
            remarks = f" [Remarks: {item.get('remarks', '')}]" if item.get('remarks') else ""
            print(f"  {name} x{item.get('quantity', 1)} - RM{item.get('price', 0):.2f}{remarks}")
        print("-" * 40)
        print(f"TOTAL: RM{order.get('total', 0):.2f}\n")

    input("\nPress Enter to continue...")
    return current_user