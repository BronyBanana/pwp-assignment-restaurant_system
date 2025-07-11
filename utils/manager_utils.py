import os

def load_lines_from_file(filename, default=[]):
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        return default
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def manage_user_accounts():
    while True:
        users = load_lines_from_file("users.txt", default=[])
        print("\n--- User Accounts ---")
        if users:
            for i, user in enumerate(users, 1):
                print(f"{i}. {user}")
        else:
            print("No users found.")

        print("\nOptions:")
        print("1. Add User")
        print("2. Delete User")
        print("3. Back")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            new_user = input("Enter new user info (e.g. username,password,role): ").strip()
            if new_user:
                users.append(new_user)
                save_lines_to_file("users.txt", users)
                print("User added successfully.")
            else:
                print("User info cannot be empty.")

        elif choice == "2":
            try:
                index = int(input("Enter the number of the user to delete: "))
                if 1 <= index <= len(users):
                    removed = users.pop(index - 1)
                    save_lines_to_file("users.txt", users)
                    print(f"User '{removed}' deleted.")
                else:
                    print("Invalid user number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            break

        else:
            print("Invalid choice. Try again.")

def save_lines_to_file(filename, lines):
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line.strip() + "\n")
            
def view_orders():
    orders = load_lines_from_file("orders.txt", default=[])
    print("\n--- Orders ---")
    for order in orders:
        print(order)
        
def track_finances():
    finances = load_lines_from_file("finances.txt", default=[])
    print("\n--- Finances ---")
    for line in finances:
        print(line)

def manage_inventory():
    inventory = load_lines_from_file("menu_data.py", default=[])
    print("\n--- Inventory (Menu Items) ---")
    for item in inventory:
        print(item)
        
def view_customer_feedback():
    feedback = load_lines_from_file("review.txt", default=[])
    print("\n--- Customer Feedback ---")
    for review in feedback:
        print(review)