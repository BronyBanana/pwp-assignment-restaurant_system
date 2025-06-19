import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_manager import DataManager

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

        choice = input("Choose option (1-6): ")

        if choice == "1":
            users = DataManager.load_data("users", default=[])
            print("\n--- User Accounts ---")
            for user in users:
                print(user)
                
        elif choice == "2":
            orders = DataManager.load_data("orders", default=[])
            print("\n--- Orders ---")
            for order in orders:
                print(order)
                
        elif choice == "3":
            finances = DataManager.load_data("finances", default=[])
            print("\n--- Finances ---")
            for line in finances:
                print(line)
                
        elif choice == "4":
            inventory = DataManager.load_data("inventory", default=[])
            print("\n--- Inventory ---")
            for item in inventory:
                print(item)
                
        elif choice == "5":
            feedback = DataManager.load_data("feedback", default=[])
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