def get_valid_choice(prompt, options):
    while True:
        choice = input(prompt)
        if choice in options:
            return choice
        print("Invalid choice. Try again.")
