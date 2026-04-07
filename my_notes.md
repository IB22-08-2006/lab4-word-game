# My Original Thinking

## App States

So the game basically moves through a few clear phases, and I like thinking of it as a little “journey” for the user:

* **Start** → the game hasn’t begun yet, kind of like a waiting/setup state
* **Playing** → this is the main part, where the user is actively guessing letters and interacting
* **Win** → all letters are guessed correctly (best case scenario, obviously)
* **Lose** → the user runs out of lives 
* **Replay / Exit decision** → giving the user control at the end feels important, like do they want revenge or are they done

I feel like separating these states clearly makes the logic cleaner and also helps if I ever want to turn this into something bigger (like with a UI or animations).

## App Variables
These are basically the core pieces that keep the game alive:

* `secret_word` → the actual word the user is trying to guess
* `guessed_letters` → keeps track of everything the user has already tried (important to avoid repetition issues)
* `lives` → how many chances the user has left 
* `guess` → the current input from the user
* `max_lives` → the starting number of lives (useful if I ever want difficulty levels)

I could also maybe add stuff like:
* `display_word` → what the user currently sees (with _ _ _ and revealed letters)
* `game_state` → to explicitly track whether we’re in Start / Playing / Win / Lose


## App Rules and Invariants
These are like the “laws of the universe” for the game—things that should *always* be true no matter what:

* Lives only go down if the guess is wrong (no punishing correct answers obviously)
* If a letter is guessed multiple times, it shouldn’t affect lives again (otherwise it’s unfair + annoying)
* The game ends in only two valid ways:
  * all letters guessed → **win**
  * lives = 0 → **lose**
* The displayed word should *always* match the correctly guessed letters (no glitches where letters disappear or don’t show)
* Only single-letter inputs should be accepted (keeping it simple and controlled)

I also feel like consistency here is key—if one rule breaks, the whole game starts feeling buggy or unreliable.


## App Bugs and Edge Cases
This is honestly where things get interesting, because users will *always* find a way to break stuff 

Some obvious (and not-so-obvious) cases I need to handle:
* User inputs more than one letter (like “ab”)
* User inputs non-letter characters (numbers, symbols, random stuff)
* User repeats the same letter multiple times (shouldn’t be penalized again)
* Empty input (just pressing enter… classic)
* Word contains repeated letters → all occurrences should be revealed, not just one
* Case sensitivity issues → “A” vs “a” should be treated the same

Extra things I’m thinking about:
* What if the user inputs spaces?
* What if they try uppercase + lowercase mixes?
* Maybe give feedback messages like “you already guessed that” instead of silently ignoring
* Prevent crashing no matter what input is given (like making it super robust)


Overall, I feel like thinking through all of this makes the app way more solid. It’s not just about making it *work*, but making it feel smooth, fair, and actually enjoyable to use. Also it feels like this could evolve into a bigger project later if I add UI, difficulty levels, or even categories of words.






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

## Extra features 
**Implementation Plan**

1. Define the target design first (one short spec).
2. Decide scoring formula.
3. Decide difficulty presets.
4. Decide category list and how words are stored.
5. Decide timer behavior on timeout.
6. Confirm whether these features apply to human mode only or also auto-play.

7. Refactor foundations before adding features.
8. Introduce a `GameConfig` object for difficulty, timer, and category.
9. Introduce a `GameSession` object for one round state.
10. Introduce a `PlayerProfile`/`ScoreBoard` object for multi-game score.
11. Keep current functions, but route them through config/session objects.

12. Add score system across multiple games.
13. Add persistent in-memory stats for current run:
  - total_games
  - wins
  - losses
  - total_score
  - streak
14. Scoring formula (recommended baseline):
  - base points per win
  - bonus for remaining lives
  - bonus for faster completion
  - category/difficulty multiplier
  - zero points on loss
15. Show scoreboard at end of each round and from main menu.
16. Add reset-score option in menu.

17. Add difficulty levels.
18. Create presets:
  - Easy: more lives, longer timer, simpler words
  - Medium: default lives/timer
  - Hard: fewer lives, shorter timer, harder words
19. Tie difficulty to:
  - `max_lives`
  - per-turn time limit
  - word pool filtering
  - score multiplier
20. Add difficulty selection before game start.
21. Save last selected difficulty for replay convenience.

22. Add word categories.
23. Create a structured dictionary like:
  - category name -> list of words
24. Add category selection menu:
  - explicit choice
  - random category option
25. Validate category has enough words.
26. Show selected category in UI and final summary.

27. Add timer-based guessing.
28. Choose implementation strategy:
  - soft timer (measure elapsed after input) for best portability
  - hard timeout input only if you accept OS/platform complexity
29. Per turn:
  - start timer
  - collect guess
  - compute elapsed
  - if elapsed > limit: count as timeout penalty
30. Timeout penalty policy:
  - recommended: lose 1 life, no guessed letter added
31. Display remaining/allowed time each turn.

32. Update game flow to support all features cleanly.
33. Start phase:
  - choose mode, difficulty, category
  - initialize session and score context
34. Playing phase:
  - process guesses with timer + validation
  - apply scoring events
35. End phase:
  - show round summary (result, points gained, total score)
  - replay or return to menu

36. Testing plan (must be added as features land).
37. Scoring tests:
  - win/loss scoring
  - difficulty multiplier
  - streak updates
38. Difficulty tests:
  - preset values applied correctly
39. Category tests:
  - category selection and random category behavior
40. Timer tests:
  - timeout path  
  - normal path within time
41. Integration tests:
  - two consecutive games update scoreboard correctly
  - replay keeps score but resets round state

42. Milestone rollout (low risk).
43. Milestone 1: Config/session refactor only.
44. Milestone 2: Difficulty + categories.
45. Milestone 3: Scoreboard across rounds.
46. Milestone 4: Timer logic.
47. Milestone 5: polish UI, docs, and tests.

48. Definition of done.
49. All new menu options work end-to-end.
50. Score carries across multiple games in one run.
51. Difficulty changes lives/timer/word complexity.
52. Category selection affects chosen secret words.
53. Timer timeout behavior is deterministic and tested.
54. Tests pass and README reflects new behavior.
