
# Guess The Word

A small terminal-based Hangman-style game written in Python.

The project includes two modes:
- Human play mode
- Auto play mode (AI guesses random letters)

## Current Project State

This README reflects the actual implementation in [main.py](main.py):
- Single-file Python application
- No external dependencies
- Menu loop with three options: Play, Auto Play, Quit
- Shared word list and shared max lives constant
- Input normalization and validation in human mode
- Repeated guesses do not reduce lives

## Features

- Random secret word selected from a predefined list
- Masked word display using underscores
- Lives system with loss at zero lives
- Win when all letters of the word are revealed
- Validation for player input:
	- strips spaces
	- lowercases input
	- accepts only one alphabetic character
- Feedback for invalid and repeated guesses

## Rules

- You start each game with 6 lives.
- A life is lost only for a new incorrect guess.
- Repeating a previous guess does not cost a life.
- The game ends in one of two terminal states:
	- Win: all letters are revealed
	- Lose: lives reach zero

## Word List

The current words are software-themed:
- algorithm
- compiler
- dataset
- debugger
- function
- network
- python
- testing
- variable
- workflow

## Project Structure

- [main.py](main.py): game logic, UI loop, and auto-play mode
- [my_notes.md](my_notes.md): design thinking, rules, and edge cases
- [JOURNAL.md](JOURNAL.md): development log

## Run

Requirements:
- Python 3.10+ recommended

Run from the project folder:

```bash
python main.py
```

On some macOS setups:

```bash
python3 main.py
```

## How to Use

1. Start the program.
2. Choose:
	 - 1 for human play
	 - 2 for auto play
	 - q to quit
3. In human mode, enter one letter per turn.

## Known Limitations

- No persistent score tracking between rounds
- No external dictionary file yet (words are in code)
- No unit tests yet
- No explicit enum/object for phase state (flow is currently loop-based)

## Possible Next Improvements

- Load words from a text file
- Add difficulty levels (lives or word complexity)
- Add test coverage for edge cases
- Add explicit game phase state model