import os
import time

GAME_TITLE = "TYPING GAME ALPHA"
MAX_NAME_LENGTH = 10


# ---------- Step 1: loading words ----------
def load_words(filename):
    words = []
    if not os.path.exists(filename):
        return words

    file = open(filename, "r")
    for line in file:
        word = line.strip()
        if word != "":
            words.append(word)
    file.close()
    return words


# ---------- Step 2: screen and input helpers ----------
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


# ---------- Step 3: picking random words ----------
def random_number(limit):
    return int.from_bytes(os.urandom(4), "big") % limit

def shuffle_list(items):
    for i in range(len(items) - 1, 0, -1):
        j = random_number(i + 1)
        items[i], items[j] = items[j], items[i]

def pick_words(words, count):
    copy = words[:]
    shuffle_list(copy)
    return copy[:count]

def build_round():
    round_words = []
    for filename in ["words3.txt", "words4.txt", "words5.txt"]:
        words = load_words(filename)
        if len(words) < 7:
            return []
        for word in pick_words(words, 7):
            round_words.append(word)
    shuffle_list(round_words)
    return round_words

# ---------- Step 4: playing the game ----------
def word_points(word):
    if len(word) == 3:
        return 2
    if len(word) == 4:
        return 5
    return 7                      # 5-letter words

def play_game(round_words):
    score = 0
    mistyped = []                 # will hold [actual, typed] pairs

    clear_screen()
    input("Ready? Press enter to start...")

    start_time = time.time()      # the timer starts here
    for word in round_words:
        clear_screen()
        print("TYPE THE WORD BELOW THEN PRESS ENTER")
        print("=" * 20)
        print(word)
        print()
        typed = input("").strip()

        if typed == word:
            score = score + word_points(word)
        else:
            mistyped.append([word, typed])

    elapsed = round(time.time() - start_time, 2)
    return score, elapsed, mistyped

# ---------- quick test (delete when we move on) ----------
round_words = build_round()
if len(round_words) == 0:
    print("Word files are missing or too short.")
else:
    score, elapsed, mistyped = play_game(round_words)
    print("Score:", score)
    print("Time:", elapsed)
    print("Mistyped:", mistyped)