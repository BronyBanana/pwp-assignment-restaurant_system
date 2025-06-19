from utils.auth import login
import config

def main():
    print(f"=== {config.APP_NAME} ===")
    user = login()
    
    if user:
        if user["role"] == "manager":
            from users.manager import manager_menu
            manager_menu()
        elif user["role"] == "cashier":
            from users.cashier import cashier_menu
            cashier_menu()
        else:
            from users.customer import customer_main
            customer_main()
    else:
        print("Login failed. Starting in guest mode...")
        from users.customer import customer_main
        customer_main()

if __name__ == "__main__":
    main()