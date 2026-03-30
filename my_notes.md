# My Original Thinking

## App States

- Start (game not started yet)
- Playing (user is guessing letters)
- Win (all letters guessed)
-  Lose (no lives left)
- Replay / Exit decision

## App Variables

- `secret_word` → the word to guess
- `guessed_letters` → list of letters already guessed
- `lives` → number of attempts left
- `guess` → current input letter
- `max_lives` → initial number of allowed attempts

## App Rules and Invariants

- The number of lives decreases only when the guess is incorrect
- A letter should not be counted twice if guessed multiple times
- The game ends when:

  - all letters are guessed → win
  - lives reach 0 → lose
- The displayed word must always reflect correctly guessed letters
- Only single-letter inputs should be accepted

## App Bugs and Edge Cases

- User inputs more than one letter
- User inputs non-letter characters (numbers, symbols)
- User repeats the same letter multiple times
- Empty input (just pressing enter)
- Word contains repeated letters (must reveal all occurrences)
- Case sensitivity issues (uppercase vs lowercase)


# CoPilot Suggestions

## App States

1. NotStarted (or Setup)
  - Word is chosen, attempts are initialized, hidden word is prepared.
2. InProgress
  - Player keeps guessing letters/words.
  - Sub-conditions inside this state are often tracked:
    - correct guess
    - incorrect guess
    - repeated guess
    - invalid input
3. Won
  - All letters are revealed before attempts run out.
4. Lost
  - Maximum wrong guesses reached before the word is completed.
5. Optional extra states (depending on your design):
  - Paused (if game can be paused/resumed)
  - Abandoned (player quits mid-game)
  - GameOver (a terminal wrapper for both Won and Lost)

A minimal implementation only needs: Setup -> InProgress -> Won/Lost.

## App Variables

1. Game setup
- secret_word: the word to guess
- guessed_letters: letters already guessed
- correct_letters: letters found in the word
- max_wrong_guesses: allowed mistakes
- wrong_guesses: current number of mistakes

2. Display and progress
- display_word: current visible form (example: _ _ a _ _)
- remaining_attempts: usually max_wrong_guesses - wrong_guesses
- game_state: NotStarted, InProgress, Won, Lost
- is_won: boolean flag (optional if you use game_state)
- is_lost: boolean flag (optional if you use game_state)

3. Input handling
- guess: current user input
- normalized_guess: cleaned input (lowercase, stripped spaces)
- is_valid_guess: whether input is a single alphabetic letter (or valid whole-word guess)
- repeated_guess: whether user already tried it

4. Optional but useful
- word_list: pool of possible words
- hint_used: whether hint was already used
- score: points across rounds
- round_number: current round in multi-round mode

Minimal working set:
- secret_word
- guessed_letters
- wrong_guesses
- max_wrong_guesses
- display_word
- game_state

## App Rules and Invariants

Rules and invariants in Hangman are the conditions that must always stay true while the game runs.

1. Hidden word and visibility
2. The secret word is fixed for one round.
3. The displayed pattern has the same length as the secret word.
4. A revealed letter stays revealed forever.
5. If a letter appears multiple times, all matching positions are revealed together.

6. Guess handling
7. Input must be valid according to game policy:
  - usually one alphabetic character (or optionally a full-word guess mode)
8. Repeated guesses do not change game progress unfairly:
  - no extra reveal
  - no extra life loss
9. Guess matching is consistent:
  - often case-insensitive comparison

10. Lives and penalties
11. Lives start at a fixed initial value.
12. Lives decrease only on a new incorrect guess.
13. Lives never go below zero.
14. Correct guesses never reduce lives.

15. Win/Lose conditions
16. Win invariant: player wins iff all unique letters in the secret word are revealed.
17. Lose invariant: player loses iff lives reach zero before full reveal.
18. Win and lose are mutually exclusive states.
19. Once in an end state, gameplay input no longer mutates round state.

20. State flow invariants
21. Normal phase flow is Start -> Playing -> End.
22. Replay starts a fresh round with reinitialized state.
23. Data from previous rounds must not leak unless intentionally tracked (score/history).

A compact formal view:
- Let R be set of revealed positions and W be word positions.
- Invariant: R only grows, never shrinks.
- Win when |R| = |W|.
- Lose when lives = 0 and |R| < |W|.

## App Bugs

Common bugs and edge cases in Hangman/word-guessing games:

1. Input validation bugs
2. Empty input (`""`)
3. Multiple characters when only one letter is allowed (`"ab"`)
4. Non-letter input (`"7"`, `"@"`, whitespace)
5. Leading/trailing spaces not stripped
6. Case handling inconsistency (`"A"` vs `"a"`)

7. Repeated guess handling
8. Re-guessing a correct letter reveals or scores again incorrectly
9. Re-guessing a wrong letter subtracts lives again (often unintended)
10. Duplicate tracking structures get out of sync (list vs set)

11. Word reveal logic issues
12. Only first occurrence revealed for repeated letters (e.g., `letter` and guess `t`)
13. Incorrect indexing causes wrong positions to reveal
14. Display string not updated after valid guess
15. Non-alphabetic chars in phrase words (spaces, hyphens, apostrophes) handled incorrectly

16. State transition bugs
17. Game allows guesses after win/loss
18. Win and loss can both be triggered in same turn
19. Replay does not fully reset state (old guessed letters/lives leak)
20. Start phase skipped without initialization

21. Lives/attempt counter bugs
22. Lives decremented on correct guess
23. Lives decremented on invalid input (if not intended)
24. Lives go negative
25. Off-by-one end condition (`lives < 0` vs `lives == 0`)

26. Win condition bugs
27. Win checked against all characters instead of unique letters
28. Win declared too early when repeated letters remain hidden
29. Full-word guess mode not integrated with letter-based win checks

30. Random word/source issues
31. Empty word list crashes selection
32. Words with uppercase/accents not normalized consistently
33. Unexpected punctuation in source words breaks validation
34. Very short/very long words create UI or balance problems

35. UX and messaging edge cases
36. No clear feedback for invalid or repeated guesses
37. Revealed word formatting breaks (`_ _a _` vs `_ _ a _`)
38. Remaining attempts display out of sync with internal value

A good test checklist is:
- repeated letters in word
- repeated guesses by player
- invalid inputs
- boundary attempts (`1 -> 0`)
- replay reset
- post-game input rejection