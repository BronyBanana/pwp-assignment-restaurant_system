import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_lines_from_file(filename, default=[]):
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        return default
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def manager_menu():
    while True:
        print("\n=== Manager Menu ===")
        print("1. Manage User Accounts")
        print("2. View Orders")
        print("3. Track Finances")
        print("4. Manage Inventory")
        print("5. View Customer Feedback")
        print("6. Exit")

        choice = input("Choose option (1-6): ").strip()

        if choice == "1":
            users = load_lines_from_file("users.txt", default=[])
            print("\n--- User Accounts ---")
            for user in users:
                print(user)

        elif choice == "2":
            orders = load_lines_from_file("orders.txt", default=[])
            print("\n--- Orders ---")
            for order in orders:
                print(order)

        elif choice == "3":
            finances = load_lines_from_file("finances.txt", default=[])
            print("\n--- Finances ---")
            for line in finances:
                print(line)

        elif choice == "4":
            inventory = load_lines_from_file("menu_items.txt", default=[])
            print("\n--- Inventory (Menu Items) ---")
            for item in inventory:
                print(item)

        elif choice == "5":
            feedback = load_lines_from_file("review.txt", default=[])
            print("\n--- Customer Feedback ---")
            for review in feedback:
                print(review)

        elif choice == "6":
            print("Exiting manager menu.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    manager_menu()
