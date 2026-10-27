import os

GAME_TITLE = "TYPING GAME ALPHA"  
MAX_NAME_LENGTH = 10               # our own choice, not in the spec

def clear_screen():
    if os.name == "nt":          
        os.system("cls")
    else:                          
        os.system("clear")

def show_title():
    print("=" * 40)
    print(GAME_TITLE.center(40))
    print("=" * 40)

def ask_menu_choice(valid_choices):
    while True:
        choice = input("Choose: ").strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Try again.")

def ask_player_name():
    while True:
        name = input("Enter your name: ").strip()
        if name == "":
            print("Name can't be empty.")
        elif len(name) > MAX_NAME_LENGTH:
            print("Name is too long (max " + str(MAX_NAME_LENGTH) + ").")
        elif "|" in name:
            print("Please don't use the | symbol.")
        else:
            return name

# quick test
clear_screen()
show_title()
print("1. Start game")
print("2. View leaderboard")
print("3. Exit")
choice = ask_menu_choice(["1", "2", "3"])
print("You chose", choice)