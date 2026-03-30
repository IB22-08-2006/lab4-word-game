import random
import string


WORDS = [
    "algorithm",
    "compiler",
    "dataset",
    "debugger",
    "function",
    "network",
    "python",
    "testing",
    "variable",
    "workflow",
]
MAX_LIVES = 6


# ---------------- LOGIC LAYER ----------------


def update_game_state(
    secret_word: str, guessed_letters: list[str], guess: str, lives: int
) -> tuple[list[str], int]:

    if guess not in guessed_letters:
        new_guessed = guessed_letters + [guess]
    else:
        new_guessed = guessed_letters

    if guess not in secret_word and guess not in guessed_letters:
        lives = max(lives - 1, 0)
    return new_guessed, lives


def get_masked_word(secret_word: str, guessed_letters: list[str]) -> str:
    return " ".join(
        [letter if letter in guessed_letters else "_" for letter in secret_word]
    )


def is_game_won(secret_word: str, guessed_letters: list[str]) -> bool:
    return all(letter in guessed_letters for letter in secret_word)


def is_game_lost(lives: int) -> bool:
    return lives <= 0


def normalize_guess(raw_guess: str) -> str:
    return raw_guess.strip().lower()


def is_valid_guess(guess: str) -> bool:
    return len(guess) == 1 and guess.isalpha()


# ---------------- UI LAYER ----------------


def play_game():
    secret_word = random.choice(WORDS)

    guessed_letters = []
    lives = MAX_LIVES

    while not is_game_lost(lives) and not is_game_won(secret_word, guessed_letters):
        print("\nWord:", get_masked_word(secret_word, guessed_letters))
        print("Guessed:", guessed_letters)
        print("Lives:", lives)

        guess = normalize_guess(input("Enter a letter: "))

        if not is_valid_guess(guess):
            print("Invalid input. Enter a single letter (a-z).")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters, lives = update_game_state(
            secret_word, guessed_letters, guess, lives
        )

    if is_game_won(secret_word, guessed_letters):
        print("🎉 You win! Word was:", secret_word)
    else:
        print("💀 You lost! Word was:", secret_word)


# ---------------- AUTO PLAY ----------------


def auto_play():
    secret_word = random.choice(WORDS)

    guessed_letters = []
    lives = MAX_LIVES
    available_letters = list(string.ascii_lowercase)

    while not is_game_lost(lives) and not is_game_won(secret_word, guessed_letters):
        guess = random.choice(available_letters)
        available_letters.remove(guess)

        print("\nAI guesses:", guess)

        guessed_letters, lives = update_game_state(
            secret_word, guessed_letters, guess, lives
        )

        print("Word:", get_masked_word(secret_word, guessed_letters))
        print("Lives:", lives)

    if is_game_won(secret_word, guessed_letters):
        print("🤖 AI WON! Word was:", secret_word)
    else:
        print("🤖 AI LOST! Word was:", secret_word)


# ---------------- MAIN LOOP ----------------


def main():
    choice = ""

    while choice != "q":
        print("\n1. Play")
        print("2. Auto Play")
        print("q. Quit")

        choice = input("Choose: ").lower()

        if choice == "1":
            play_game()
        elif choice == "2":
            auto_play()


if __name__ == "__main__":
    main()
