from utils.data_manager import DataManager

def login():
    print("=== Login ===")
    username = input("Username: ")
    password = input("Password: ")
    
    users = DataManager.load_data("users", default=[])
    for user_line in users:
        if "," in user_line:
            parts = user_line.split(',')
            if len(parts) >= 3:
                role = parts[0].strip()
                user = parts[1].strip()
                pwd = parts[2].strip()
                if username == user and password == pwd:
                    print(f"Welcome, {username} ({role})!")
                    return {"username": username, "role": role}
    
    print("Invalid username or password.\n")
    return None