import os
import json
import config

class DataManager:
    @staticmethod
    def load_data(file_key: str, default=None):
        path = config.PATHS[file_key]
        try:
            if not os.path.exists(path):
                return default() if callable(default) else default
                
            with open(path, 'r') as f:
                if file_key in ["menu", "promo"]:
                    return json.load(f)
                else:
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            if config.DEBUG:
                print(f"Error loading {file_key}: {e}")
            return default() if callable(default) else default

    @staticmethod
    def save_data(file_key: str, data):
        path = config.PATHS[file_key]
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                if file_key in ["menu", "promo"]:
                    json.dump(data, f, indent=2)
                elif file_key == "users":
                    for user in data:
                        f.write(f"{user['role']},{user['username']},{user['password']}\n")
                else:
                    if isinstance(data, list):
                        f.write("\n".join(data))
                    else:
                        f.write(str(data))
            return True
        except Exception as e:
            if config.DEBUG:
                print(f"Error saving {file_key}: {e}")
            return False

    @staticmethod
    def append_data(file_key: str, data):
        path = config.PATHS[file_key]
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'a') as f:
                if isinstance(data, list):
                    f.write("\n".join(data) + "\n")
                else:
                    f.write(str(data) + "\n")
            return True
        except Exception as e:
            if config.DEBUG:
                print(f"Error appending to {file_key}: {e}")
            return False