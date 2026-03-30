from dataclasses import dataclass
import time
import random
import string


@dataclass
class DifficultyConfig:
    name: str
    max_lives: int
    turn_time_limit_sec: float
    score_multiplier: float


@dataclass
class RoundState:
    secret_word: str
    category: str
    guessed_letters: list[str]
    lives: int
    start_time: float
    ended: bool
    won: bool


@dataclass
class ScoreBoard:
    total_games: int
    wins: int
    losses: int
    total_score: int
    current_streak: int
    best_streak: int


WORD_BANK_BY_CATEGORY = {
    "programming": ["algorithm", "compiler", "debugger", "function", "variable"],
    "tech": ["network", "python", "dataset", "testing", "workflow"],
    "animals": ["tiger", "elephant", "giraffe", "dolphin"],
}

MAX_LIVES = 6


def build_difficulty_configs():
    return {
        "easy": DifficultyConfig("easy", 10, 30.0, 1.0),
        "medium": DifficultyConfig("medium", 7, 20.0, 1.5),
        "hard": DifficultyConfig("hard", 5, 10.0, 2.0),
    }


# ---------------- LOGIC LAYER ----------------


def select_secret_word(category, word_bank):
    return random.choice(word_bank[category])


def create_round_state(secret_word, category, max_lives):
    return RoundState(
        secret_word=secret_word,
        category=category,
        guessed_letters=[],
        lives=max_lives,
        start_time=time.monotonic(),
        ended=False,
        won=False,
    )


def timed_guess_input(prompt, time_limit_sec):
    start = time.monotonic()
    guess = input(prompt)
    end = time.monotonic()

    elapsed = end - start
    timeout = elapsed > time_limit_sec

    return normalize_guess(guess), elapsed, timeout


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


def process_player_turn(state: RoundState, difficulty: DifficultyConfig):
    print("\nWord:", get_masked_word(state.secret_word, state.guessed_letters))
    print("Guessed:", state.guessed_letters)
    print("Lives:", state.lives)

    guess, elapsed, timeout = timed_guess_input(
        "Enter a letter or full word: ", difficulty.turn_time_limit_sec
    )

    if timeout:
        print("⏰ Too slow!")
        state.lives = max(state.lives - 1, 0)
        if is_game_lost(state.lives):
            state.ended = True
            state.won = False
        return

    if not guess.isalpha():
        print("Invalid input.")
        return

    if len(guess) > 1:
        if guess == state.secret_word:
            state.guessed_letters = list(set(state.secret_word))
            state.ended = True
            state.won = True
        else:
            print("Wrong word guess.")
            state.lives = max(state.lives - 1, 0)
            if is_game_lost(state.lives):
                state.ended = True
                state.won = False
        return

    if not is_valid_guess(guess):
        print("Invalid input.")
        return

    if guess in state.guessed_letters:
        print("Already guessed.")
        return

    state.guessed_letters, state.lives = update_game_state(
        state.secret_word,
        state.guessed_letters,
        guess,
        state.lives,
    )

    if is_game_won(state.secret_word, state.guessed_letters):
        state.ended = True
        state.won = True

    elif is_game_lost(state.lives):
        state.ended = True
        state.won = False


def compute_round_score(won, lives_left, elapsed_total, difficulty):
    if not won:
        return 0

    base = 100
    life_bonus = lives_left * 10
    speed_bonus = max(0, int(50 - elapsed_total))

    return int((base + life_bonus + speed_bonus) * difficulty.score_multiplier)


def update_scoreboard(board, won, points):
    board.total_games += 1

    if won:
        board.wins += 1
        board.current_streak += 1
        board.best_streak = max(board.best_streak, board.current_streak)
    else:
        board.losses += 1
        board.current_streak = 0

    board.total_score += points


def play_round(difficulty, category, board, word_bank):
    word = select_secret_word(category, word_bank)
    state = create_round_state(word, category, difficulty.max_lives)

    while not state.ended:
        process_player_turn(state, difficulty)

    elapsed = time.monotonic() - state.start_time
    points = compute_round_score(state.won, state.lives, elapsed, difficulty)

    update_scoreboard(board, state.won, points)

    if state.won:
        print("🎉You win!", word)
    else:
        print("💀You lost!", word)

    print("Points earned:", points)


# ---------------- AUTO PLAY ----------------


def auto_play():
    all_words = [word for words in WORD_BANK_BY_CATEGORY.values() for word in words]
    secret_word = random.choice(all_words)

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
    board = ScoreBoard(0, 0, 0, 0, 0, 0)
    difficulties = build_difficulty_configs()

    while True:
        print("\n1. Play")
        print("2. Auto Play")
        print("3. Scoreboard")
        print("q. Quit")

        choice = input("Choose: ").lower()

        if choice == "1":
            diff_name = input("Choose difficulty (easy/medium/hard): ").lower()
            difficulty = difficulties.get(diff_name, difficulties["easy"])

            category = input(
                f"Choose category {list(WORD_BANK_BY_CATEGORY.keys())}: "
            ).lower()
            if category not in WORD_BANK_BY_CATEGORY:
                category = "programming"

            play_round(difficulty, category, board, WORD_BANK_BY_CATEGORY)

        elif choice == "2":
            auto_play()

        elif choice == "3":
            print(board)

        elif choice == "q":
            break


if __name__ == "__main__":
    main()
