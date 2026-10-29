# Typing Game Alpha

## How to play

1. Keep `typing_game.py`, `words3.txt`, `words4.txt`, and `words5.txt` in the same folder.
2. Open PowerShell or Command Prompt in that folder and run:

   ```text
   python typing_game.py
   ```

   If `python` is not recognized, try `py typing_game.py`.
3. Choose an option from the menu:
   - Enter `1` to start a game.
   - Enter `2` to view the leaderboard.
   - Enter `3` to exit.
4. When prompted, press Enter to begin. A 3-2-1 countdown appears before the timer starts.
5. Type each displayed word exactly as shown, including capitalization, then press Enter. There are 21 words. Incorrect answers count toward your time but do not earn points.
6. After the last word, review any mistyped words and press Enter to see your results.
7. If your score qualifies for the top 10, enter a name of up to 10 characters. Names cannot be empty or contain `|`.
8. Review the leaderboard, then press Enter to return to the menu.

Three-letter words are worth 2 points, four-letter words are worth 5 points, and five-letter words are worth 7 points. The maximum score is 98. Higher scores rank first; for equal scores, the faster time ranks higher.

The game needs at least seven words in each of `words3.txt`, `words4.txt`, and `words5.txt`. The leaderboard is saved automatically in `leaderboard.txt`.
