import os
import time

GAME_TITLE = "TYPING GAME ALPHA"    # change this to your own title/theme
MAX_NAME_LENGTH = 10                # our own choice, not in the spec

# colors (ANSI codes)
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

LEADERBOARD_FILE = "leaderboard.txt"
LEADERBOARD_SIZE = 10


# ---------- Step 1: loading words ----------
def load_words(filename):
    words = []
    if not os.path.exists(filename):
        return words                      # missing file -> empty list, no crash

    file = open(filename, "r")
    for line in file:
        word = line.strip()               # remove newline and spaces
        if word != "":                    # skip blank lines
            words.append(word)
    file.close()
    return words


# ---------- Step 2: screen and input helpers ----------
def clear_screen():
    if os.name == "nt":                   # Windows
        os.system("cls")
    else:                                 # Mac / Linux
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
    # random whole number from 0 to limit - 1 (uses only the os library)
    return int.from_bytes(os.urandom(4), "big") % limit

def shuffle_list(items):
    # Fisher-Yates shuffle
    for i in range(len(items) - 1, 0, -1):
        j = random_number(i + 1)
        items[i], items[j] = items[j], items[i]

def pick_words(words, count):
    copy = words[:]                       # copy so the original isn't changed
    shuffle_list(copy)
    return copy[:count]                   # first 'count' items = no duplicates

def build_round():
    round_words = []
    for filename in ["words3.txt", "words4.txt", "words5.txt"]:
        words = load_words(filename)
        if len(words) < 7:                # not enough words -> tell the caller
            return []
        for word in pick_words(words, 7):
            round_words.append(word)
    shuffle_list(round_words)             # mix 3, 4 and 5-letter words together
    return round_words


# ---------- Step 4 + 8: playing the game ----------
def word_points(word):
    if len(word) == 3:
        return 2
    if len(word) == 4:
        return 5
    return 7                              # 5-letter words

def countdown():
    for number in [3, 2, 1]:
        clear_screen()
        print(YELLOW + "Starting in " + str(number) + "..." + RESET)
        time.sleep(1)

def play_game(round_words):
    score = 0
    mistyped = []                         # holds [actual, typed] pairs
    streak = 0
    best_streak = 0

    clear_screen()
    input("Ready? Press enter to start...")
    countdown()                           # runs BEFORE the timer starts

    start_time = time.time()              # the timer starts here
    number = 0
    for word in round_words:
        number = number + 1
        clear_screen()
        print("Word " + str(number) + "/" + str(len(round_words))
              + "   Streak: " + str(streak))
        print("TYPE THE WORD BELOW THEN PRESS ENTER")
        print("=" * 20)
        print(CYAN + word + RESET)
        print()
        typed = input("").strip()

        if typed == word:
            score = score + word_points(word)
            streak = streak + 1
            if streak > best_streak:
                best_streak = streak
        else:
            mistyped.append([word, typed])
            streak = 0

    elapsed = round(time.time() - start_time, 2)
    return score, elapsed, mistyped, best_streak


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
# each entry is a list: [name, time, score]
# the file stores each entry as one line:  score|time|name

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


# ---------- Step 7 + 8: results and main menu ----------
def show_results(score, elapsed, mistyped, best_streak, total):
    correct = total - len(mistyped)
    accuracy = round(correct * 100 / total, 1)
    wpm = 0
    if elapsed > 0:
        wpm = round(correct * 60 / elapsed, 1)

    print(GREEN + "Your score: " + str(score) + " out of 98" + RESET)
    print("Your time: " + str(elapsed) + " seconds")
    print("Accuracy: " + str(accuracy) + "%")
    print("Words per minute: " + str(wpm))
    print("Best streak: " + str(best_streak))
    print()

def start_game(entries):
    round_words = build_round()
    if len(round_words) == 0:
        clear_screen()
        print("Word files are missing or have fewer than 7 words each.")
        input("Press enter to go back...")
        return entries

    score, elapsed, mistyped, best_streak = play_game(round_words)
    show_misspelled(mistyped)

    clear_screen()
    show_results(score, elapsed, mistyped, best_streak, len(round_words))
    if score > 0 and qualifies(entries, score, elapsed):
        print("You made the leaderboard!")
        name = ask_player_name()
        entries = add_entry(entries, name, elapsed, score)
        save_leaderboard(entries)         # saved only when it changed
    else:
        print("Not on the leaderboard this time.")
    print()
    show_leaderboard(entries)
    input("Press enter to continue...")
    return entries

def main():
    if os.name == "nt":
        os.system("")                     # lets older Windows terminals show colors
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