from customer.customer_acc import customer_account_management
from customer.menu_data import get_default_menu
from customer.product_browsing import product_browsing
from customer.cart_management import cart_management
from customer.order_tracking import order_tracking
from customer.dishes_review import dishes_review
from utils.data_manager import DataManager
import config

def load_initial_data():
    menu = get_default_menu()
    DataManager.save_data("menu", menu)
    return {
        'current_user': None,
        'menu': menu
    }

def customer_main():
    state = load_initial_data()

    while True:
        print("\n" + "=" * 40)
        print(f"Status: {'Logged in as ' + state['current_user'] if state['current_user'] else 'Not logged in'}")
        print("=" * 40)
        print("1. Account Management")
        print("2. Browse Menu")
        print("3. My Cart")
        print("4. Order Tracking")
        print("5. Dish Reviews")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            state['current_user'] = customer_account_management(state['current_user'])
        elif choice == "2":
            product_browsing(state['menu'])
        elif choice == "3":
            state['current_user'] = cart_management(state['current_user'], state['menu'])
        elif choice == "4":
            state['current_user'] = order_tracking(state['current_user'])
        elif choice == "5":
            state['current_user'] = dishes_review(state['current_user'])
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")