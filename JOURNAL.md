# This Journal gets updated automatically by the Journal Logger Agent

## 2026-03-10 - Recent Interaction Summary

- Discussed Hangman game states and identified a practical state model:
	- `NotStarted/Setup -> InProgress -> Won/Lost`
	- Optional: `Paused`, `Abandoned`, `GameOver`
- Listed core variables needed for a Python implementation:
	- `secret_word`, `guessed_letters`, `wrong_guesses`, `max_wrong_guesses`, `display_word`, `game_state`
	- Plus validation helpers like `normalized_guess`, `is_valid_guess`, and `repeated_guess`
- Clarified rules and invariants:
	- Lives decrease only on new incorrect guesses
	- Revealed letters never become hidden again
	- Win/Lose are mutually exclusive terminal outcomes
	- Replay must reinitialize round state
- Reviewed common bugs and edge cases:
	- Invalid input, repeated guesses, repeated-letter reveal bugs, off-by-one life logic, replay reset leaks, and post-game input handling
- Updated notes in [my_notes.md](my_notes.md) to make phase separation explicit:
	- Start phase (initialize)
	- Playing phase (input/validation/update)
	- End phase (result + replay/exit)

## 2026-03-11 - Code Review and Fixes

- Reviewed the implementation in [main.py](main.py) against the rules in [my_notes.md](my_notes.md).
- Main findings from review:
	- Repeated wrong guesses were still reducing lives.
	- Input validation was missing for empty, multi-character, and non-letter inputs.
	- State flow worked but was implicit rather than explicit.
	- Words list was duplicated across game functions.
- Implemented minimal gameplay fixes in [main.py](main.py):
	- Added input normalization (`strip` + lowercase).
	- Added single-letter alphabetic validation.
	- Prevented repeated guesses from affecting lives.
	- Clamped lives to never go below zero.
	- Reused `is_game_lost` in loop conditions for consistency.
- Refactored repeated configuration in [main.py](main.py):
	- Introduced shared constants `WORDS` and `MAX_LIVES`.
	- Updated both `play_game()` and `auto_play()` to use shared constants.
	- Replaced previous word set with a cleaner list of software-themed words.
- Diagnostics check after edits reported no errors in [main.py](main.py).


