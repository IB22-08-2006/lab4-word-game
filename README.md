# Guess The Word

A simple terminal-based Hangman-style game built in Python.
I designed this project to be clean, easy to run, and focused on core game logic, with both a human mode and a basic AI mode for testing.

## Overview

The game is implemented in a single file (`main.py`) and doesn’t require any external libraries. It includes a simple menu where you can:

* Play manually
* Watch the AI play
* Quit the game

Both modes share the same rules, word list, and life system.

## Features

* Random word selection from a predefined list
* Hidden word displayed with underscores
* 6 lives per game
* Clear win/lose conditions
* Input validation for human players:
  * trims spaces
  * converts input to lowercase
  * only accepts a single letter
* Repeated guesses are handled properly (no life penalty)
* Feedback for invalid or already used letters

## Game Rules

* You start with **6 lives**
* You lose a life only when guessing a **new incorrect letter**
* Repeating a letter does **not** cost a life
* The game ends when:
  * you **guess all letters** → win
  * you run out of lives → lose

## Word List

All words are software-related:
* algorithm
* compiler
* dataset
* debugger
* function
* network
* python
* testing
* variable
* workflow

## Project Structure

* `main.py` – contains the full game logic, UI loop, and AI mode
* `my_notes.md` – personal notes about design decisions and edge cases
* `JOURNAL.md` – development progress and reflections

## How to Run

Make sure you have Python 3.10+ installed.
From the project folder, run:
```bash
python main.py
```
On some systems:
```bash
python3 main.py
```

## How to Play

1. Start the program
2. Choose an option:
   * `1` → play manually
   * `2` → watch auto-play
   * `q` → quit
3. If playing manually, enter one letter per turn

## Current Limitations
* No score tracking between games
* Word list is hardcoded (not loaded from a file)
* No unit tests yet
* Game flow is loop-based (no explicit state model yet)

## Next Steps / Ideas
* Load words from an external file
* Add difficulty levels (lives, word complexity)
* Write unit tests for edge cases
* Refactor into a clearer game state model