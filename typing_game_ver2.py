import os
import random
import time

# ---------- settings (you can change these) ----------
GAME_TITLE = "TYPING GAME ALPHA"
MAX_NAME_LENGTH = 10
LEADERBOARD_FILE = "leaderboard.txt"
LEADERBOARD_SIZE = 10

# Each leaderboard entry is a list: [name, time, score]
# These numbers say where each item sits inside that list.
NAME_INDEX = 0
TIME_INDEX = 1
SCORE_INDEX = 2


# ---------- Part 1: loading the words ----------
def load_words(filename):
    words = []
    # check first, so a missing file does not crash the program
    if not os.path.exists(filename):
        return words

    file = open(filename, "r")
    for line in file:
        word = line.strip()          # removes the hidden new line at the end
        if word != "":               # skip blank lines
            words.append(word)
    file.close()
    return words


# ---------- Part 2: screen and input helpers ----------
def clear_screen():
    if os.name == "nt":              # Windows
        os.system("cls")
    else:                            # Mac / Linux
        os.system("clear")

def show_title():
    print("=" * 40)
    print(GAME_TITLE.center(40))     # center() puts the text in the middle
    print("=" * 40)

def ask_menu_choice(valid_choices):
    # keeps asking until the player types one of the valid choices
    while True:
        choice = input("Choose: ").strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Try again.")

def ask_player_name():
    # keeps asking until the name follows all the rules
    while True:
        name = input("Enter your name: ").strip()
        if name == "":
            print("Name can't be empty.")
        elif len(name) > MAX_NAME_LENGTH:
            print("Name is too long (max " + str(MAX_NAME_LENGTH) + ").")
        elif "|" in name:
            # the | symbol separates the parts of a line in leaderboard.txt
            print("Please don't use the | symbol.")
        else:
            return name


# ---------- Part 3: choosing the random words ----------
def build_round():
    round_words = []
    for filename in ["words3.txt", "words4.txt", "words5.txt"]:
        words = load_words(filename)
        if len(words) < 7:
            return []                # not enough words, the caller will check this
        chosen = random.sample(words, 7)     # 7 different words from this file
        for word in chosen:
            round_words.append(word)
    random.shuffle(round_words)      # mix the 3, 4 and 5-letter words together
    return round_words


# ---------- Part 4: playing the game ----------
def word_points(word):
    if len(word) == 3:
        return 2
    if len(word) == 4:
        return 5
    return 7                         # 5-letter words

def countdown():
    for number in [3, 2, 1]:
        clear_screen()
        print("Starting in " + str(number) + "...")
        time.sleep(1)                # wait 1 second

def play_game(round_words):
    score = 0
    mistyped = []                    # will hold pairs: [actual word, typed word]
    streak = 0                       # correct words in a row
    best_streak = 0

    clear_screen()
    input("Ready? Press enter to start...")
    countdown()

    start_time = time.time()         # the timer starts here, after the countdown
    number = 0
    for word in round_words:
        number = number + 1
        clear_screen()
        print("Word " + str(number) + "/" + str(len(round_words))
              + "   Streak: " + str(streak))
        print("TYPE THE WORD BELOW THEN PRESS ENTER")
        print("=" * 20)
        print(word)
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

    elapsed = round(time.time() - start_time, 2)    # total seconds, 2 decimals
    # a function can give back several values at once
    return score, elapsed, mistyped, best_streak


# ---------- Part 5: the misspelled words screen ----------
def show_misspelled(mistyped):
    clear_screen()
    print("*" * 30)
    print("MISTYPED WORDS")
    print("ACTUAL".ljust(10) + "ANSWER")    # ljust(10) adds spaces up to 10 characters

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


# ---------- Part 6: the leaderboard ----------
# In the file, each line looks like this:  score|time|name
# Example:  98|30.5|juls

def is_decimal_number(text):
    # a time like "30.5" has two digit parts with one dot between them
    pieces = text.split(".")
    if len(pieces) != 2:
        return False
    return pieces[0].isdigit() and pieces[1].isdigit()

def is_valid_line(parts):
    # checks one line from the file BEFORE we try to use it
    if len(parts) != 3:
        return False
    if not parts[0].isdigit():           # the score
        return False
    if not is_decimal_number(parts[1]):  # the time
        return False
    if parts[2] == "":                   # the name
        return False
    return True

def is_better(a, b):
    # a higher score is better; if the scores are equal, a lower time is better
    if a[SCORE_INDEX] != b[SCORE_INDEX]:
        return a[SCORE_INDEX] > b[SCORE_INDEX]
    return a[TIME_INDEX] < b[TIME_INDEX]

def sort_leaderboard(entries):
    # insertion sort: take each entry and slide it left past the ones it beats
    for i in range(1, len(entries)):
        current = entries[i]
        j = i - 1
        while j >= 0 and is_better(current, entries[j]):
            entries[j + 1] = entries[j]
            j = j - 1
        entries[j + 1] = current
    return entries

def keep_top_entries(entries):
    while len(entries) > LEADERBOARD_SIZE:
        entries.pop()                    # removes the last (worst) entry
    return entries

def load_leaderboard():
    entries = []
    if not os.path.exists(LEADERBOARD_FILE):
        return entries

    file = open(LEADERBOARD_FILE, "r")
    for line in file:
        parts = line.strip().split("|")
        if is_valid_line(parts):         # damaged lines are simply ignored
            score = int(parts[0])
            elapsed = float(parts[1])
            name = parts[2]
            entries.append([name, elapsed, score])
    file.close()

    sort_leaderboard(entries)
    return keep_top_entries(entries)

def save_leaderboard(entries):
    file = open(LEADERBOARD_FILE, "w")   # "w" erases the file and writes it again
    for entry in entries:
        line = (str(entry[SCORE_INDEX]) + "|" + str(entry[TIME_INDEX])
                + "|" + entry[NAME_INDEX])
        file.write(line + "\n")
    file.close()

def qualifies(entries, score, elapsed):
    # does this result belong in the top 10?
    if len(entries) < LEADERBOARD_SIZE:
        return True
    last = entries[len(entries) - 1]
    return is_better(["", elapsed, score], last)

def add_entry(entries, name, elapsed, score):
    entries.append([name, elapsed, score])
    sort_leaderboard(entries)
    return keep_top_entries(entries)

def show_leaderboard(entries):
    print("*" * 18)
    print("***LEADERBOARD***")
    print("*" * 18)
    print("RANK".ljust(8) + "NAME".ljust(14) + "TIME".ljust(10) + "SCORE")
    for i in range(LEADERBOARD_SIZE):
        rank = "[" + str(i + 1) + "]"
        if i < len(entries):
            name = entries[i][NAME_INDEX]
            elapsed = str(entries[i][TIME_INDEX])
            score = str(entries[i][SCORE_INDEX])
            print(rank.ljust(8) + name.ljust(14) + elapsed.ljust(10) + score)
        else:
            print(rank.ljust(8) + "---")


# ---------- Part 7: results and the main menu ----------
def show_results(score, elapsed, mistyped, best_streak, total):
    correct = total - len(mistyped)
    accuracy = round(correct * 100 / total, 1)
    wpm = 0                              # words per minute
    if elapsed > 0:                      # never divide by zero
        wpm = round(correct * 60 / elapsed, 1)

    print("Your score: " + str(score) + " out of 98")
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
        save_leaderboard(entries)        # saved only when the leaderboard changed
    else:
        print("Not on the leaderboard this time.")
    print()
    show_leaderboard(entries)
    input("Press enter to continue...")
    return entries

def main():
    entries = load_leaderboard()         # loaded once, when the program starts
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