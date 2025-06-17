import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def manager_menu():
    while True:
        print("\n=== Manager Menu ===")
        print("1. Manage User Accounts")
        print("2. View Orders")
        print("3. Track Finances")
        print("4. Manage Inventory")
        print("5. View Customer Feedback")
        print("6. Exit")

        choice = input("Choose option (1–6): ")

        if choice == "1":
            manage_users()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            track_finances()
        elif choice == "4":
            manage_inventory()
        elif choice == "5":
            view_feedback()
        elif choice == "6":
            print("Exiting manager menu.")
            break
        else:
            print("Invalid option. Try again.")

def manage_users():
    print("\n--- Manage User Accounts ---")
    try:
        with open("data/users.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No users found.")

def view_orders():
    print("\n--- View Orders ---")
    try:
        with open("data/orders.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No orders found.")

def track_finances():
    print("\n--- Track Finances ---")
    try:
        with open("data/finances.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No finance records found.")

def manage_inventory():
    print("\n--- Manage Inventory ---")
    try:
        with open("data/inventory.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No inventory found.")

def view_feedback():
    print("\n--- View Customer Feedback ---")
    try:
        with open("data/feedback.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No feedback found.")
