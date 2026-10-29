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

# ---------- Step 5: misspelled words screen ----------
def show_misspelled(mistyped):
    clear_screen()
    print("*" * 30)
    print("MISTYPED WORDS")
    print("ACTUAL".ljust(10) + "ANSWER")

    if len(mistyped) == 0:
        print("None! Perfect typing!")
    else:
        for pair in mistyped:
            actual = pair[0]
            typed = pair[1]
            if typed == "":
                typed = "(nothing)"
            print(actual.ljust(10) + typed)

    print("*" * 30)
    input("Press enter to continue...")

# ---------- Step 6: leaderboard ----------
LEADERBOARD_FILE = "leaderboard.txt"
LEADERBOARD_SIZE = 10

# each entry is a list: [name, time, score]

def split_line(line, separator):
    # our own split, so we don't depend on a built-in parser
    parts = []
    current = ""
    for character in line:
        if character == separator:
            parts.append(current)
            current = ""
        else:
            current = current + character
    parts.append(current)
    return parts

def is_whole_number(text):
    return text != "" and text.isdigit()

def is_decimal_number(text):
    if text == "":
        return False
    dots = 0
    digits = 0
    for character in text:
        if character == ".":
            dots = dots + 1
        elif character.isdigit():
            digits = digits + 1
        else:
            return False
    return dots <= 1 and digits >= 1

def is_better(a, b):
    # higher score wins; if tied, lower time wins
    if a[2] != b[2]:
        return a[2] > b[2]
    return a[1] < b[1]

def sort_leaderboard(entries):
    # insertion sort, best entry first
    for i in range(1, len(entries)):
        current = entries[i]
        j = i - 1
        while j >= 0 and is_better(current, entries[j]):
            entries[j + 1] = entries[j]
            j = j - 1
        entries[j + 1] = current
    return entries

def load_leaderboard():
    entries = []
    if not os.path.exists(LEADERBOARD_FILE):
        return entries

    file = open(LEADERBOARD_FILE, "r")
    for line in file:
        parts = split_line(line.strip(), "|")
        if len(parts) != 3:
            continue                      # skip damaged lines
        if not is_whole_number(parts[0]):
            continue
        if not is_decimal_number(parts[1]):
            continue
        if parts[2] == "":
            continue
        entries.append([parts[2], float(parts[1]), int(parts[0])])
    file.close()

    sort_leaderboard(entries)
    return entries[:LEADERBOARD_SIZE]

def save_leaderboard(entries):
    file = open(LEADERBOARD_FILE, "w")
    for entry in entries:
        file.write(str(entry[2]) + "|" + str(entry[1]) + "|" + entry[0] + "\n")
    file.close()

def qualifies(entries, score, elapsed):
    if len(entries) < LEADERBOARD_SIZE:
        return True
    last = entries[len(entries) - 1]
    return is_better(["", elapsed, score], last)

def add_entry(entries, name, elapsed, score):
    entries.append([name, elapsed, score])
    sort_leaderboard(entries)
    return entries[:LEADERBOARD_SIZE]

def show_leaderboard(entries):
    print("*" * 18)
    print("***LEADERBOARD***")
    print("*" * 18)
    print("RANK".ljust(8) + "NAME".ljust(14) + "TIME".ljust(10) + "SCORE")
    for i in range(LEADERBOARD_SIZE):
        rank = "[" + str(i + 1) + "]"
        if i < len(entries):
            name = entries[i][0]
            elapsed = str(entries[i][1])
            score = str(entries[i][2])
            print(rank.ljust(8) + name.ljust(14) + elapsed.ljust(10) + score)
        else:
            print(rank.ljust(8) + "---")

# ---------- Step 7: main menu ----------
def show_results(score, elapsed):
    print("Your score:", score, "out of 98")
    print("Your time:", elapsed, "seconds")
    print()

def start_game(entries):
    round_words = build_round()
    if len(round_words) == 0:
        clear_screen()
        print("Word files are missing or have fewer than 7 words each.")
        input("Press enter to go back...")
        return entries

    score, elapsed, mistyped = play_game(round_words)
    show_misspelled(mistyped)

    clear_screen()
    show_results(score, elapsed)
    if score > 0 and qualifies(entries, score, elapsed):
        print("You made the leaderboard!")
        name = ask_player_name()
        entries = add_entry(entries, name, elapsed, score)
        save_leaderboard(entries)
    else:
        print("Not on the leaderboard this time.")
    print()
    show_leaderboard(entries)
    input("Press enter to continue...")
    return entries

def main():
    entries = load_leaderboard()          # loaded once, when the program launches
    while True:
        clear_screen()
        show_title()
        print("1. Start game")
        print("2. View leaderboard")
        print("3. Exit")
        choice = ask_menu_choice(["1", "2", "3"])

        if choice == "1":
            entries = start_game(entries)
        elif choice == "2":
            clear_screen()
            show_leaderboard(entries)
            input("Press enter to go back...")
        else:
            clear_screen()
            print("Thanks for playing!")
            return

main()