from utils.auth import login


def main():
    print("=== Restaurant Ordering & Management System ===")
    user = login()
    if user:
        if user["role"] == "manager":
            from users.manager import manager_menu
            manager_menu()
        elif user["role"] == "cashier":
            from users.cashier import cashier_menu
            cashier_menu()
    else:
        print("Login failed.")


if __name__ == "__main__":
    main()
