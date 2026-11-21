# Typing Game Alpha: Presentation Guide

*For practicing the presentation. This is not part of the project submission.*

---

## 1. A 2-minute explanation

> "This is a typing game that runs in the terminal. It loads three word lists, picks 7 random words of each length, and shows them in random order. The player types each word, and the game scores 2, 5, or 7 points depending on the word length, for a maximum of 98. When the player finishes, it shows the words they got wrong, then updates a top-10 leaderboard that is saved in a text file. The leaderboard ranks by score first and uses time only to break ties. The project rules didn't allow try-except, so instead of catching errors, I check things before using them: whether a file exists, whether a line in the leaderboard is valid, and whether the player's input is valid."

## 2. Suggested demo order

1. Start the program and show the menu.
2. Play a game. Type most words correctly and misspell one or two on purpose.
3. Show the MISTYPED WORDS screen.
4. Enter a name and show the leaderboard.
5. Exit, run the program again, and show that the leaderboard is still there.
6. Open `leaderboard.txt` and show the saved format.

## 3. How the code works, section by section

The file reads from top to bottom. Each section only uses functions from the sections above it, so it can be taught in the same order.

### Loading words: `load_words(filename)`
Opens a word file and puts each line into a list. `strip()` removes the hidden newline at the end of each line, otherwise `"sun\n"` would never equal `"sun"`. If the file doesn't exist, it returns an empty list instead of crashing.

### Screen and input helpers
- `clear_screen()` clears the terminal (`cls` on Windows, `clear` on Mac/Linux).
- `show_title()` prints the game title.
- `ask_menu_choice()` keeps asking until the player types one of the allowed choices.
- `ask_player_name()` keeps asking until the name is not empty, is at most 10 characters, and has no `|` character.

### Picking random words
- `random_number(limit)` gives a random whole number from 0 to `limit - 1`, using `os.urandom()`.
- `shuffle_list()` uses the **Fisher-Yates shuffle**: go from the end of the list to the start and swap each item with a randomly chosen item at or before it.
- `pick_words()` shuffles a *copy* of a word list and takes the first 7. Because it takes the first 7 of a shuffled list, no word repeats.
- `build_round()` does this for the three files, then shuffles all 21 words together. If any file has fewer than 7 words, it returns an empty list.

*Statistics connection:* picking 7 words this way is a simple random sample **without replacement**, and Fisher-Yates produces every possible ordering with equal probability.

### Playing the game: `play_game()`
1. Shows "Ready? Press enter to start..." and a 3-2-1 countdown.
2. **Then** starts the timer, so the countdown and reading time are not counted.
3. For each word: show it, read the player's answer, and compare it with `==`. If it matches, add `word_points()` to the score and extend the streak. If not, save `[actual word, typed word]` and reset the streak.
4. Stops the timer and returns the score, time, mistakes, and best streak.

### Misspelled words screen: `show_misspelled()`
Prints the saved wrong answers in two columns (ACTUAL and ANSWER). `ljust(10)` pads the first word with spaces so the columns line up. An empty answer is shown as `(nothing)`. If there are no mistakes, it prints "None! Perfect typing!".

### Leaderboard
Each entry is a small list: `[name, time, score]`. The leaderboard is a list of those entries.

- `is_better(a, b)`: the higher score wins; if the scores are equal, the lower time wins.
- `sort_leaderboard()`: an **insertion sort** using `is_better()`, best entry first. It works like sorting playing cards in your hand.
- `split_line()`: cuts a line at each `|`. It is written by hand because the project does not allow data parsers.
- `is_whole_number()` and `is_decimal_number()`: check that text really is a number *before* converting it, because converting bad text would crash the program.
- `load_leaderboard()`: reads the file, skips any damaged lines, sorts, and keeps the top 10.
- `save_leaderboard()`: writes every entry back to the file as `score|time|name`.
- `qualifies()`: tells whether a new result is good enough for the top 10.
- `add_entry()`: inserts the new result, re-sorts, and keeps only 10.
- `show_leaderboard()`: prints the table. Empty ranks show `---`.

*Statistics connection:* ranking by score with time as a tie-breaker is a two-key ordering, like ranking by one variable and breaking ties with another.

### Results and main menu
- `show_results()` shows the score (out of 98), time, accuracy (correct ÷ total × 100), words per minute (correct words × 60 ÷ seconds), and best streak.
- `start_game()` runs one full game: build the words, play, show mistakes, show results. If the player qualifies and scored above 0, it asks for a name, adds the entry, and saves the file.
- `main()` loads the leaderboard once at launch and then shows the menu in a loop until the player chooses Exit.

## 4. Questions a teacher may ask, with answers

**Why is there no try-except?**
The project doesn't allow it, so the program checks first: `os.path.exists()` for files, loops for input, and skipping damaged leaderboard lines.

**Why `os.urandom()` and not `random`?**
The project only mentions the `os` library. `os.urandom()` gives random bytes, and the shuffle turns them into a random order. (If `random` is allowed, `random.sample()` and `random.shuffle()` would do the same job in fewer lines.)

**Why do you write your own `split_line()`?**
The project doesn't allow data parsers, so splitting each line by hand avoids any doubt. It walks through the characters and cuts at each `|`.

**Why is a copy of the list made in `pick_words()`?**
Shuffling changes a list. Without a copy, the original word list would be changed too.

**How does the shuffle work?**
Fisher-Yates: from the last position to the first, swap each item with a randomly chosen item at or before it.

**Is the random choice perfectly fair?**
Almost. Turning `os.urandom` bytes into a number with `%` (remainder) has a very small bias, because 2³² is not an exact multiple of the list size. For lists of 21 items or fewer it is negligible. Fisher-Yates itself is fair if the random numbers are.

**How does the ranking work?**
`is_better()` compares scores first. Only if they are equal does it compare times. That is how a 38 in 50 seconds beats a 37 in 20 seconds.

**Why insertion sort?**
It is simple, easy to write by hand, and the leaderboard has at most 11 entries, so speed doesn't matter.

**What if two players have the same score and time?**
Neither is "better", so the earlier entry stays ahead.

**What happens if someone edits `leaderboard.txt` incorrectly?**
Lines with the wrong number of parts or invalid numbers are skipped when the file is loaded. The next save removes them from the file.

**Why does the timer start after the countdown?**
So only typing time is measured. The time affects ranking, so it should be fair.

**When is the leaderboard file saved?**
Only when a new result qualifies, which is the "saved if modified" rule.

**Is typing case-sensitive?**
Yes. `Sun` does not match `sun`.

**Why is `time` imported?**
For the stopwatch and the countdown pause. The leaderboard needs a TIME column, and `os` has no reliable stopwatch. (Check with the instructor that `time` is allowed.)

**Which parts are your own additions?**
The countdown, counters, accuracy, words per minute, streak, colors, and title screen. They don't change the required scoring.

## 5. Words to know

| Term | Plain meaning |
|---|---|
| Function | A named block of code you can run whenever you need it |
| List | An ordered collection of items, like `["sun", "map"]` |
| Loop | Code that repeats |
| Validation | Checking that input is acceptable before using it |
| Index | An item's position in a list; the first item is position 0 |
| Return value | What a function gives back to the code that called it |
| Sorting | Putting items in order |

## 6. Practice checklist

- [ ] Run the game once without looking at the code
- [ ] Explain each section of the code out loud in your own words
- [ ] Answer 5 of the questions in section 4 without reading the answers
- [ ] Practice the demo in section 2 start to finish
- [ ] Fill in your name and course in `README.md`
- [ ] Delete or keep `leaderboard.txt`, depending on what you want to show
