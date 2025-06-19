def get_default_menu():
    return {
        "B1": {
            "name": "Cheese Burger",
            "base_price": 11.00,
            "category": "Burgers",
            "ingredients": {
                "Bun": {"price": 0.00, "default": True},
                "Beef Patty": {"price": 0.00, "default": True},
                "Cheese": {"price": 0.00, "default": True},
                "Lettuce": {"price": 0.00, "default": True},
                "Tomato": {"price": 0.00, "default": True},
                "Bacon": {"price": 2.50, "default": False},
                "Avocado": {"price": 1.50, "default": False}
            }
        },
        "B2": {
            "name": "Chicken Burger",
            "base_price": 10.00,
            "category": "Burgers",
            "ingredients": {
                "Bun": {"price": 0.00, "default": True},
                "Chicken Patty": {"price": 0.00, "default": True},
                "Spicy Sauce": {"price": 0.50, "default": False}
            }
        },
        "B3": {
            "name": "Fish Burger",
            "base_price": 10.00,
            "category": "Burgers",
            "ingredients": {
                "Bun": {"price": 0.00, "default": True},
                "Lettuce": {"price": 0.00, "default": True},
                "Cheese": {"price": 0.00, "default": True},
                "Tartar Sauce": {"price": 0.00, "default": True},
                "Fish Patty": {"price": 0.00, "default": True}
            }
        },
        "B4": {
            "name": "Beef Burger",
            "base_price": 11.00,
            "category": "Burgers",
            "ingredients": {
                "Bun": {"price": 0.00, "default": True},
                "Beef Patty": {"price": 0.00, "default": True},
                "Cheese": {"price": 0.00, "default": True},
                "Lettuce": {"price": 0.00, "default": True},
                "Tomato": {"price": 0.00, "default": True}
            }
        },
        "S1": {
            "name": "French Fries",
            "base_price": 5.00,
            "category": "Sides",
            "ingredients": {}
        },
        "S2": {
            "name": "Nugget (4 Pcs)",
            "base_price": 6.66,
            "category": "Sides",
            "ingredients": {}
        },
        "S3": {
            "name": "Nugget (6 Pcs)",
            "base_price": 8.88,
            "category": "Sides",
            "ingredients": {}
        },
        "S4": {
            "name": "Nugget (9 Pcs)",
            "base_price": 12.88,
            "category": "Sides",
            "ingredients": {}
        },
        "S5": {
            "name": "Chicken Tender",
            "base_price": 13.00,
            "category": "Sides",
            "ingredients": {}
        },
        "D1": {
            "name": "Cherry Coke",
            "base_price": 3.00,
            "category": "Drinks",
            "ingredients": {}
        },
        "D2": {
            "name": "Sprite",
            "base_price": 3.00,
            "category": "Drinks",
            "ingredients": {}
        },
        "D3": {
            "name": "Fanta",
            "base_price": 3.00,
            "category": "Drinks",
            "ingredients": {}
        },
        "D4": {
            "name": "Lemonade",
            "base_price": 2.00,
            "category": "Drinks",
            "ingredients": {}
        },
        "D5": {
            "name": "Mineral Water",
            "base_price": 1.00,
            "category": "Drinks",
            "ingredients": {}
        },
        "M1": {
            "name": "Family Combo",
            "base_price": 85.90,
            "category": "Meals",
            "contents": {
                "B1": 3,
                "B2": 2,
                "S4": 1,
                "S5": 1,
                "D1": 5
            }
        },
        "M2": {
            "name": "Children Combo",
            "base_price": 18.00,
            "category": "Meals",
            "contents": {
                "B3": 1,
                "S1": 1,
                "S5": 1,
                "D1": 1
            }
        },
        "M3": {
            "name": "Double Combo",
            "base_price": 25.90,
            "category": "Meals",
            "contents": {
                "B4": 2,
                "D1": 2
            }
        },
        "M4": {
            "name": "Single Combo",
            "base_price": 11.90,
            "category": "Meals",
            "contents": {
                "B2": 1,
                "D1": 1
            }
        }
    }
