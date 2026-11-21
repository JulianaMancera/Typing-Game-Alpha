# Typing Game Alpha

## 1. About the game

The player is shown 21 words, one at a time, and has to type each one exactly and press Enter. The game keeps track of the score and the total time. When the player finishes, it shows the words they got wrong and a top-10 leaderboard that is saved in a file.

- 7 words with 3 letters: 2 points each
- 7 words with 4 letters: 5 points each
- 7 words with 5 letters: 7 points each
- Maximum score: (7 × 2) + (7 × 5) + (7 × 7) = **98 points**

## 2. How to run it

1. Put these files in the same folder:
   - `typing_game.py`
   - `words3.txt`, `words4.txt`, `words5.txt`
2. Open PowerShell or Command Prompt **inside that folder**.
3. Run:

```
python typing_game.py
```

If `python` is not recognized, try `py typing_game.py`.

Only the `os` and `time` modules from Python's standard library are used. Nothing needs to be installed.

## 3. How to play

1. The main menu has three options:
   - **1. Start game**
   - **2. View leaderboard**
   - **3. Exit**
2. After choosing Start, press Enter when ready. A 3-2-1 countdown runs, and then the timer starts.
3. Each word appears under `TYPE THE WORD BELOW THEN PRESS ENTER`. Type it exactly (letter case matters) and press Enter. A wrong answer is still counted in the time but earns no points.
4. After the 21st word, the game shows the **MISTYPED WORDS** screen with the actual word next to what was typed. Press Enter to continue.
5. The results screen shows the score, time, accuracy, words per minute, and best streak.
6. If the score is good enough for the top 10, the player enters a name (up to 10 characters, no `|`) and the leaderboard is saved to a file.
7. The leaderboard is shown, and the game returns to the main menu.

**Ranking:** a higher score always ranks higher. Time is used only when two scores are equal. For example, 38 points in 50 seconds beats 37 points in 20 seconds.

## 4. Files

| File | What it is |
|---|---|
| `typing_game.py` | The whole program |
| `words3.txt` | List of 3-letter words, one per line |
| `words4.txt` | List of 4-letter words, one per line |
| `words5.txt` | List of 5-letter words, one per line |
| `leaderboard.txt` | Saved leaderboard, created automatically; one player per line as `score\|time\|name` |

Each word file needs at least 7 words. More words make the game less repetitive.

## 5. Project requirements and how they are met

| Requirement from the specification | How the program meets it |
|---|---|
| Words come from predefined files, 7 of each length, random order | `load_words()` reads the three files; `build_round()` picks 7 from each and shuffles all 21 |
| 3, 4, 5-letter words are worth 2, 5, 7 points | `word_points()` |
| Show misspelled words after the game, press Enter to continue | `show_misspelled()` |
| Leaderboard of 10 players with rank, name, time, score | `show_leaderboard()` |
| Leaderboard saved in a file, loaded at launch, saved when modified | `load_leaderboard()` at the start of `main()`; `save_leaderboard()` only when a player qualifies |
| Score is prioritized over time | `is_better()` compares score first, then time |
| Option to start the game or view the leaderboard | The menu in `main()` (plus Exit) |
| The program should not crash, and no try-except | Risky steps are checked first (see section 6) |
| No PyGame, third-party libraries, or data parsers | Only `os` and `time` are imported; line splitting is written by hand |
| Must run in a plain terminal | Tested in PowerShell / Command Prompt |

## 6. How crashes are avoided without try-except

Instead of catching errors after they happen, the program checks first:

| Possible problem | Check used |
|---|---|
| A word file is missing | `os.path.exists()`; the game shows a message and returns to the menu |
| A word file has fewer than 7 words | `build_round()` returns an empty list and `start_game()` reports it |
| `leaderboard.txt` is missing | `os.path.exists()`; the leaderboard simply starts empty |
| A line in `leaderboard.txt` is damaged | A wrong number of parts or a non-number is detected and the line is skipped |
| Menu input is wrong or empty | `ask_menu_choice()` loops until the input is valid |
| Name is empty, too long, or contains `\|` | `ask_player_name()` loops until the name is valid |
| Dividing by zero in words per minute | An `if elapsed > 0` check |

## 7. Design decisions

The specification leaves these open, so they were choices made for this project:

- The player enters a name **only after** making the leaderboard.
- A player must score above 0 to enter the leaderboard.
- If two players have the same score, the faster time ranks higher.
- If score and time are both equal, the earlier entry stays ahead.
- "Top 10" means 10 entries, so the same name can appear more than once.
- Names are at most 10 characters and cannot contain `|`.
- Times are rounded to 2 decimal places.
- Typing is case-sensitive.
- The countdown is not included in the timed portion.
- `os.urandom()` is used for randomness so that only the `os` library is needed for it.

## 8. Extra features

- Title screen and menu
- 3-2-1 countdown before the timer starts
- Word counter and streak counter during the game
- Accuracy %, words per minute, and best streak on the results screen
- Colored text (cyan words, yellow countdown, green score)

None of these change the required scoring or ranking rules.

## 9. Testing done

- Typing all 21 words correctly gives exactly 98 points.
- Wrong and empty answers appear correctly in the MISTYPED WORDS table.
- The leaderboard keeps exactly 10 players and sorts by score first, then time.
- A tie in score is broken by the lower time.
- Saved results are still there after closing and reopening the program.
- A damaged line in `leaderboard.txt` is ignored.
- A missing `leaderboard.txt` shows 10 empty ranks.
- A missing word file shows a message and returns to the menu.
- Invalid menu choices and invalid names are rejected.
- Runs in a plain PowerShell / Command Prompt window.
