import json

def view_receipt(username):
    try:
        with open("data/receipt.json", "r", encoding="utf-8") as f:
            all_receipts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNo receipts available.")
        return

    user_receipts = {
        oid: r for oid, r in all_receipts.items()
        if r.get("system_user") == username
    }

    if not user_receipts:
        print("\nYou have no receipts yet.")
        return

    # Найдём последний заказ по дате
    last_id, last = max(user_receipts.items(), key=lambda x: x[1]["timestamp"])

    print("\n" + "=" * 40)
    print(f"🧾 Receipt for Order {last_id}")
    print("-" * 40)
    print(f"Status   : {last.get('status')}")
    print(f"Type     : {last.get('type')}")
    print(f"Date     : {last.get('timestamp')}")
    if last.get("type") == "Dine-In":
        print(f"Table No : {last.get('table_number')}")
    if last.get("remarks"):
        print(f"Remarks  : {last.get('remarks')}")
    print("\nItems:")
    for item in last["items"]:
        print(f" - {item['name']} x{item['quantity']} @ ${item['price_each']:.2f} "
              f"= ${item['subtotal']:.2f}")
    print(f"\nTotal: ${last['total']:.2f}")
    print("=" * 40)
