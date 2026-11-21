# Typing Game Alpha: Code Explanation

*For learning and presenting the code. This matches the current `typing_game.py`.*

---

## 1. How beginner-friendly is the code?

The program uses only the basics:

- variables, numbers, and text
- `if` / `elif` / `else`
- `for` and `while` loops
- lists (including a list of lists)
- functions
- reading and writing a text file

**Not used anywhere:** classes, dictionaries, sets, list comprehensions, `lambda`, `try-except`, `with`, f-strings, slicing (`[:]`), or `+=`.

### Python tools the program uses

If your teacher asks "what did you use?", this is the complete list.

| Tool | What it does | Where it's used |
|---|---|---|
| `print()` | Shows text on the screen | Everywhere |
| `input()` | Waits for the player to type and press Enter | Menu, words, name |
| `len()` | Counts items in a list or letters in text | Word length, list size |
| `str()` | Turns a number into text so it can be joined with `+` | Printing scores and times |
| `int()` / `float()` | Turns text into a whole number / decimal number | Reading the leaderboard file |
| `round(x, 2)` | Rounds a number to 2 decimals | Time, accuracy |
| `range()` | Makes a sequence of numbers to loop over | Sorting, leaderboard rows |
| `open()`, `.write()`, `.close()` | Read and write files | Words, leaderboard |
| `.append()` | Adds an item to the end of a list | Building lists |
| `.pop()` | Removes the last item of a list | Trimming the leaderboard |
| `.strip()` | Removes spaces and the hidden new line from the ends of text | Words, input, file lines |
| `.split("\|")` | Cuts text into a list at each `\|` | Reading the leaderboard file |
| `.isdigit()` | True if the text is only digits | Checking numbers |
| `.ljust(10)` | Pads text with spaces on the right up to 10 characters | Lining up columns |
| `.center(40)` | Puts text in the middle of a 40-character line | Title |
| `os.path.exists()` | True if a file exists | Avoiding crashes |
| `os.name`, `os.system()` | Which system we're on, and run a command | Clearing the screen |
| `random.sample()` | Picks several different items from a list | Choosing 7 words |
| `random.shuffle()` | Mixes a list in random order | Mixing the 21 words |
| `time.time()` | The current time in seconds | The stopwatch |
| `time.sleep()` | Pauses the program | The 3-2-1 countdown |

### The few things that may be new to a beginner

Be ready to explain these five, since they're the most "unusual" parts:

1. **`.ljust()` and `.center()`**: only for looks (lining up text).
2. **Returning several values**: `return score, elapsed, mistyped, best_streak`, received with `score, elapsed, mistyped, best_streak = play_game(...)`.
3. **A list of lists**: each leaderboard entry is a small list inside the big list.
4. **`random.sample()`**: picks different items so there are no repeats.
5. **Insertion sort**: the sorting loop in `sort_leaderboard()`, explained in section 4.

Everything else is ordinary loops, ifs, and lists.

---

## 2. The big picture

```
main()                          <- the boss: shows the menu, repeats until Exit
 ├─ Option 1 → start_game()
 │    ├─ build_round()          pick 21 random words
 │    ├─ play_game()            show words, time it, score it
 │    ├─ show_misspelled()      show the wrong answers
 │    ├─ show_results()         score, time, accuracy, words per minute
 │    └─ qualifies? → ask_player_name() → add_entry() → save_leaderboard()
 ├─ Option 2 → show_leaderboard()
 └─ Option 3 → exit
```

The small functions are workers. `main()` decides when each one runs. Python reads the file from top to bottom, so each function is defined before it is used.

---

## 3. The settings at the top

```python
import os
import random
import time

GAME_TITLE = "TYPING GAME ALPHA"
MAX_NAME_LENGTH = 10
LEADERBOARD_FILE = "leaderboard.txt"
LEADERBOARD_SIZE = 10

NAME_INDEX = 0
TIME_INDEX = 1
SCORE_INDEX = 2
```

- `import` brings in tools that come with Python: `os` for files and the screen, `random` for chance, `time` for the stopwatch.
- The capital-letter names are **constants**: values set once and used everywhere. To change the title or the leaderboard size, you edit one line.
- Each leaderboard entry is a list `[name, time, score]`. `NAME_INDEX`, `TIME_INDEX`, and `SCORE_INDEX` say where each item sits. So `entry[SCORE_INDEX]` reads better than `entry[2]`. Positions in a list start at 0.

---

## 4. The code, part by part

### Part 1: Loading the words

```python
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
```

- `def` makes a function. `filename` is its input.
- `words = []` starts an empty list.
- If the file doesn't exist, the function returns the empty list right away. **This is how the program avoids a crash without try-except: check first.**
- `open(filename, "r")` opens the file to read. `for line in file` goes through it one line at a time.
- `line.strip()` removes the hidden new line at the end. Without it, `"sun\n"` would never equal `"sun"`.
- Blank lines are skipped, and every other word is added to the list.

### Part 2: Screen and input helpers

```python
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
```
Windows clears the screen with `cls`, and Mac/Linux with `clear`. `os.name` is `"nt"` on Windows.

```python
def show_title():
    print("=" * 40)
    print(GAME_TITLE.center(40))
    print("=" * 40)
```
`"=" * 40` repeats the symbol 40 times. `.center(40)` puts the title in the middle.

```python
def ask_menu_choice(valid_choices):
    while True:
        choice = input("Choose: ").strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Try again.")
```
`while True` repeats forever until the `return` runs. It only returns when the answer is in the allowed list, so empty or wrong input just asks again.

```python
def ask_player_name():
    while True:
        name = input("Enter your name: ").strip()
        if name == "":
            ...
        elif len(name) > MAX_NAME_LENGTH:
            ...
        elif "|" in name:
            ...
        else:
            return name
```
Same idea with three rules: not empty, not too long, no `|`. The `|` rule matters because `|` separates the parts of each line in `leaderboard.txt`. A name containing it would break the line.

### Part 3: Choosing the random words

```python
def build_round():
    round_words = []
    for filename in ["words3.txt", "words4.txt", "words5.txt"]:
        words = load_words(filename)
        if len(words) < 7:
            return []
        chosen = random.sample(words, 7)
        for word in chosen:
            round_words.append(word)
    random.shuffle(round_words)
    return round_words
```

- The loop goes through the three files.
- If a file has fewer than 7 words, it returns an empty list. `start_game()` checks for that later and shows a message instead of crashing.
- `random.sample(words, 7)` picks **7 different words** from the list, so there are no repeats. The original list isn't changed.
- All the chosen words go into one list of 21.
- `random.shuffle()` mixes the 3, 4, and 5-letter words together, so they appear in random order.

*Statistics connection:* `random.sample` is a simple random sample **without replacement**, and shuffling puts the 21 words in a random order.

### Part 4: Playing the game

```python
def word_points(word):
    if len(word) == 3:
        return 2
    if len(word) == 4:
        return 5
    return 7
```
The scoring rule is in one place. If a word isn't 3 or 4 letters, it must be 5, so it returns 7.

```python
def countdown():
    for number in [3, 2, 1]:
        clear_screen()
        print("Starting in " + str(number) + "...")
        time.sleep(1)
```
`time.sleep(1)` waits one second. `str(number)` turns the number into text, because `+` joins text with text.

```python
def play_game(round_words):
    score = 0
    mistyped = []
    streak = 0
    best_streak = 0
```
These are the counters: the score, a list for wrong answers, the current streak of correct words, and the best streak.

```python
    clear_screen()
    input("Ready? Press enter to start...")
    countdown()
    start_time = time.time()
```
The game waits until the player is ready, runs the countdown, and **only then** starts the timer. `time.time()` returns the current time in seconds. Subtracting two readings gives the elapsed time.

```python
    number = 0
    for word in round_words:
        number = number + 1
        clear_screen()
        print("Word " + str(number) + "/" + str(len(round_words)) + "   Streak: " + str(streak))
        print("TYPE THE WORD BELOW THEN PRESS ENTER")
        print("=" * 20)
        print(word)
        print()
        typed = input("").strip()
```
The loop runs once for each of the 21 words. It shows the word and stores the player's answer in `typed`.

```python
        if typed == word:
            score = score + word_points(word)
            streak = streak + 1
            if streak > best_streak:
                best_streak = streak
        else:
            mistyped.append([word, typed])
            streak = 0
```
`==` checks that the two texts are exactly the same, capital letters included.
- Correct: add the points and extend the streak.
- Wrong: save the pair `[actual word, typed word]` for the mistyped screen, and reset the streak to 0.

```python
    elapsed = round(time.time() - start_time, 2)
    return score, elapsed, mistyped, best_streak
```
The time now minus the start time is the total time, rounded to 2 decimals. A function can return several values at once, and the caller receives them in the same order.

### Part 5: The misspelled words screen

```python
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
```

- `.ljust(10)` adds spaces after a word until it's 10 characters long, so the second column lines up.
- If the list is empty, there were no mistakes.
- Otherwise each pair is taken apart: `pair[0]` is the actual word and `pair[1]` is what was typed.
- An empty answer is shown as `(nothing)`, so the column doesn't look broken.
- The last `input()` just pauses the screen until the player presses Enter.

### Part 6: The leaderboard

In the file, each player is one line: `score|time|name`, for example `98|30.5|juls`.
In memory, each player is a list: `[name, time, score]`. Notice the order is different.

```python
def is_decimal_number(text):
    pieces = text.split(".")
    if len(pieces) != 2:
        return False
    return pieces[0].isdigit() and pieces[1].isdigit()
```
`"30.5".split(".")` gives `["30", "5"]`. A valid time has exactly two pieces, and both must be digits. We check **before** converting, because `float("abc")` would crash the program.

```python
def is_valid_line(parts):
    if len(parts) != 3:
        return False
    if not parts[0].isdigit():
        return False
    if not is_decimal_number(parts[1]):
        return False
    if parts[2] == "":
        return False
    return True
```
This checks one line from the file: three parts, a whole-number score, a decimal time, and a non-empty name. If anything is wrong, it says `False`.

```python
def is_better(a, b):
    if a[SCORE_INDEX] != b[SCORE_INDEX]:
        return a[SCORE_INDEX] > b[SCORE_INDEX]
    return a[TIME_INDEX] < b[TIME_INDEX]
```
**This is the ranking rule.** If the scores are different, the higher score wins. Only if the scores are equal does the lower time win. That is how 38 points in 50 seconds beats 37 points in 20 seconds. If both are equal, it returns `False`, so the earlier entry stays ahead.

```python
def sort_leaderboard(entries):
    for i in range(1, len(entries)):
        current = entries[i]
        j = i - 1
        while j >= 0 and is_better(current, entries[j]):
            entries[j + 1] = entries[j]
            j = j - 1
        entries[j + 1] = current
    return entries
```
This is **insertion sort**. Think of sorting playing cards in your hand:
1. Take the next card (`current`).
2. Slide it to the left past every card it beats. The `while` loop shifts those cards one place right.
3. Drop it into the gap.

Repeat for every card. When it finishes, the best entry is first.

To teach it, take 5 numbers on paper and do it by hand.

```python
def keep_top_entries(entries):
    while len(entries) > LEADERBOARD_SIZE:
        entries.pop()
    return entries
```
While there are more than 10 entries, `.pop()` removes the last one (the worst).

```python
def load_leaderboard():
    entries = []
    if not os.path.exists(LEADERBOARD_FILE):
        return entries

    file = open(LEADERBOARD_FILE, "r")
    for line in file:
        parts = line.strip().split("|")
        if is_valid_line(parts):
            score = int(parts[0])
            elapsed = float(parts[1])
            name = parts[2]
            entries.append([name, elapsed, score])
    file.close()

    sort_leaderboard(entries)
    return keep_top_entries(entries)
```
- No file means an empty leaderboard.
- `"98|30.5|juls".split("|")` gives `["98", "30.5", "juls"]`.
- Each line is checked with `is_valid_line()` **before** it is used. Damaged lines are simply ignored. This is the "no crash" rule again.
- Valid lines become entries `[name, time, score]`, with `int()` and `float()` turning the text into numbers.
- At the end it sorts and keeps the top 10.

```python
def save_leaderboard(entries):
    file = open(LEADERBOARD_FILE, "w")
    for entry in entries:
        line = (str(entry[SCORE_INDEX]) + "|" + str(entry[TIME_INDEX])
                + "|" + entry[NAME_INDEX])
        file.write(line + "\n")
    file.close()
```
`"w"` means write: it erases the old file and writes a new one. Each entry becomes `score|time|name` followed by `\n` to end the line.

```python
def qualifies(entries, score, elapsed):
    if len(entries) < LEADERBOARD_SIZE:
        return True
    last = entries[len(entries) - 1]
    return is_better(["", elapsed, score], last)
```
If there are fewer than 10 players, anyone qualifies. Otherwise, the new result must beat the last place. The `""` is just a placeholder name, because `is_better()` only looks at the score and time.

```python
def add_entry(entries, name, elapsed, score):
    entries.append([name, elapsed, score])
    sort_leaderboard(entries)
    return keep_top_entries(entries)
```
Add the new entry, sort, and trim to 10.

```python
def show_leaderboard(entries):
    ...
    for i in range(LEADERBOARD_SIZE):
        rank = "[" + str(i + 1) + "]"
        if i < len(entries):
            ...
        else:
            print(rank.ljust(8) + "---")
```
It always prints 10 rows. `i` starts at 0, so the rank is `i + 1`. If there is an entry for that row it prints it, otherwise it prints `---`.

### Part 7: Results and the main menu

```python
def show_results(score, elapsed, mistyped, best_streak, total):
    correct = total - len(mistyped)
    accuracy = round(correct * 100 / total, 1)
    wpm = 0
    if elapsed > 0:
        wpm = round(correct * 60 / elapsed, 1)
```
- Correct words = total minus mistakes.
- Accuracy = correct ÷ total × 100 (a percentage).
- Words per minute = correct words × 60 ÷ seconds (a rate).
- `if elapsed > 0` prevents dividing by zero.

```python
def start_game(entries):
    round_words = build_round()
    if len(round_words) == 0:
        ...
        return entries

    score, elapsed, mistyped, best_streak = play_game(round_words)
    show_misspelled(mistyped)

    clear_screen()
    show_results(score, elapsed, mistyped, best_streak, len(round_words))
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
```
- If the word files are missing or too short, it shows a message and returns without playing.
- Otherwise it plays, shows the mistakes, and shows the results.
- If the score is above 0 and good enough, it asks for a name, adds the entry, and **saves the file**. The file is saved only when the leaderboard changed.
- It returns the updated list so the menu keeps the new leaderboard.

```python
def main():
    entries = load_leaderboard()
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
            ...
        else:
            clear_screen()
            print("Thanks for playing!")
            return
```
- The leaderboard is loaded **once**, when the program starts.
- `while True` shows the menu again and again.
- `entries = start_game(entries)` matters. Without `entries =`, the menu would keep showing the old leaderboard.
- `return` in the last branch ends `main()`, so the program ends.

The very last line of the file, `main()`, starts everything.

---

## 5. One full run, step by step

1. Run the file. `main()` loads `leaderboard.txt` into `entries`.
2. The player chooses 1, and `start_game()` builds 21 random words.
3. `play_game()` runs the countdown, starts the timer, and goes through the words.
4. The player gets 20 right. One word goes into `mistyped`.
5. `show_misspelled()` and `show_results()` display the outcome.
6. `qualifies()` says yes, so the player enters a name.
7. `add_entry()` inserts the entry and sorts. `save_leaderboard()` writes the file.
8. The leaderboard is shown and the menu returns.

---

## 6. How the project rules are met

| Rule | How |
|---|---|
| Words from 3 predefined files, 7 of each, random order | `load_words()`, then `build_round()` |
| 2 / 5 / 7 points | `word_points()` |
| Mistyped words screen | `show_misspelled()` |
| Leaderboard of 10 in a file, loaded at launch, saved when changed | `load_leaderboard()`, `save_leaderboard()`, `qualifies()` |
| Score has priority over time | `is_better()` |
| Menu with start and view leaderboard | `main()` |
| No crashing, no try-except | Check first: `os.path.exists()`, input loops, `is_valid_line()` |
| No PyGame, third-party libraries, or data parsers | Only `os`, `random`, and `time`, which come with Python; no `json` or `csv` |
| Runs in a plain terminal | Tested in PowerShell / Command Prompt |

---

## 7. Questions a teacher may ask

**Why is there no try-except?**
The project doesn't allow it. Instead, the program checks first: `os.path.exists()` for files, loops that repeat until input is valid, and `is_valid_line()` to skip damaged lines.

**Why do you use `random` and `time`? The project only mentions `os`.**
They come with Python, so they aren't third-party libraries, which is what the rules ban. The game needs random words and a time for the leaderboard, so these tools are needed.

**Why do you use `.split("|")`? Isn't that a parser?**
`.split()` is a basic string method, like `.strip()`. The rule is about data parsers like `json`.

**How do you make sure the 7 words don't repeat?**
`random.sample()` picks different items from the list.

**How does the ranking work?**
`is_better()` compares scores first. Time is used only if the scores are equal. That's how a 38 in 50 seconds beats a 37 in 20 seconds.

**Why insertion sort?**
It's simple, and the leaderboard is tiny, so speed doesn't matter. It's like sorting cards in your hand.

**Why `NAME_INDEX`, `TIME_INDEX`, and `SCORE_INDEX`?**
So the code says `entry[SCORE_INDEX]` instead of `entry[2]`. It's easier to read, and you can't mix up the positions.

**What happens if someone edits `leaderboard.txt` wrongly?**
`is_valid_line()` finds lines with the wrong number of parts or non-numbers, and they're ignored. The next save removes them.

**Why must a time contain a dot?**
Python writes decimal numbers like `30.0` or `30.5`, so every time saved by the program has a dot.

**Why does the timer start after the countdown?**
So only typing time is measured. The time affects the ranking, so it should be fair.

**When is the leaderboard file saved?**
Only when a new result qualifies. That is the "saved if modified" rule.

**Why can't a name contain `|`?**
`|` separates the parts of each line in the file. A name containing it would break the line when it's read back.

**Is typing case-sensitive?**
Yes. `Sun` does not match `sun`.

**Which parts are your own additions?**
The countdown, the word and streak counters, accuracy, words per minute, and the title screen. They don't change the required scoring.

**What would you improve?**
Possible answers: a practice mode, a difficulty level, a rule that each player appears once on the leaderboard, or more words in the word files.

---

## 8. Tips for explaining it

- **10-second version:** "It picks 21 random words, times how long you take to type them, scores by word length, and keeps a top-10 leaderboard in a file."
- **1-minute version:** the 2-minute explanation in `PRESENTATION_GUIDE.md`, shortened.
- **Deep version:** go through section 4 in order. Each part only uses things from the parts above it.
- If you forget something, read the **comments** in the code. Every part has plain-English notes.
- It's fine to say "I'm not sure, but I think..." The teacher cares more that you understand how the program works than that you remember every word.
