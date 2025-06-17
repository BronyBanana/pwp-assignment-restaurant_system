

def login():
    print("=== Login ===")
    username = input("Username: ")
    password = input("Password: ")
    try:
        with open("data/users.txt", "r") as file:
            for line in file:
                role, user, pw = line.strip().split(",")
                if username == user and password == pw:
                    print(f"Welcome, {username} ({role})!")
                    return {"username": user, "role": role}
        print("Invalid username or password.\n")
        return None
    except FileNotFoundError:
        print("User database not found.")
        return None
