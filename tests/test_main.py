import builtins

import pytest

import main


def test_update_game_state_new_correct_guess_adds_letter_and_keeps_life():
    guessed, lives = main.update_game_state("python", [], "p", 6)
    assert guessed == ["p"]
    assert lives == 6


def test_update_game_state_new_wrong_guess_adds_letter_and_decrements_life():
    guessed, lives = main.update_game_state("python", [], "z", 6)
    assert guessed == ["z"]
    assert lives == 5


def test_update_game_state_repeated_wrong_guess_no_extra_life_loss():
    guessed, lives = main.update_game_state("python", ["z"], "z", 5)
    assert guessed == ["z"]
    assert lives == 5


def test_update_game_state_repeated_correct_guess_no_change():
    guessed, lives = main.update_game_state("python", ["p"], "p", 6)
    assert guessed == ["p"]
    assert lives == 6


def test_update_game_state_lives_never_below_zero():
    guessed, lives = main.update_game_state("python", [], "z", 0)
    assert guessed == ["z"]
    assert lives == 0


def test_get_masked_word_no_guesses():
    assert main.get_masked_word("robot", []) == "_ _ _ _ _"


def test_get_masked_word_reveals_all_occurrences_of_letter():
    # All 't' positions in letter are revealed.
    assert main.get_masked_word("letter", ["t"]) == "_ _ t t _ _"


def test_get_masked_word_order_of_guesses_does_not_matter():
    first = main.get_masked_word("python", ["p", "o"])
    second = main.get_masked_word("python", ["o", "p"])
    assert first == second


def test_is_game_won_true_when_all_letters_present():
    assert main.is_game_won("aba", ["a", "b"]) is True


def test_is_game_won_false_when_letter_missing():
    assert main.is_game_won("python", ["p", "y", "t"]) is False


def test_is_game_lost_true_at_zero_and_below():
    assert main.is_game_lost(0) is True
    assert main.is_game_lost(-1) is True


def test_is_game_lost_false_above_zero():
    assert main.is_game_lost(1) is False


def test_normalize_guess_strips_and_lowercases():
    assert main.normalize_guess("  A  ") == "a"


def test_is_valid_guess_accepts_single_alpha_only():
    assert main.is_valid_guess("a") is True
    assert main.is_valid_guess("Z") is True
    assert main.is_valid_guess("") is False
    assert main.is_valid_guess("ab") is False
    assert main.is_valid_guess("7") is False
    assert main.is_valid_guess("@") is False


def test_select_secret_word_returns_word_from_category():
    word = main.select_secret_word("programming", main.WORD_BANK_BY_CATEGORY)
    assert word in main.WORD_BANK_BY_CATEGORY["programming"]


def test_create_round_state_initializes_correctly():
    state = main.create_round_state("python", "programming", 6)
    assert state.secret_word == "python"
    assert state.category == "programming"
    assert state.guessed_letters == []
    assert state.lives == 6
    assert state.ended is False
    assert state.won is False


def test_compute_round_score_win():
    difficulty = main.build_difficulty_configs()["easy"]
    # Won with 5 lives and took 5 seconds
    score = main.compute_round_score(True, 5, 5.0, difficulty)
    assert score > 0


def test_compute_round_score_loss_is_zero():
    difficulty = main.build_difficulty_configs()["easy"]
    score = main.compute_round_score(False, 5, 5.0, difficulty)
    assert score == 0


def test_update_scoreboard_increments_wins():
    board = main.ScoreBoard(0, 0, 0, 0, 0, 0)
    main.update_scoreboard(board, True, 100)
    assert board.total_games == 1
    assert board.wins == 1
    assert board.total_score == 100
    assert board.current_streak == 1


def test_update_scoreboard_increments_losses():
    board = main.ScoreBoard(0, 0, 0, 0, 0, 0)
    main.update_scoreboard(board, False, 0)
    assert board.total_games == 1
    assert board.losses == 1
    assert board.current_streak == 0


def test_auto_play_terminates_and_prints_result(monkeypatch, capsys):
    monkeypatch.setattr(
        main.random, "choice", lambda _seq: _seq[0] if isinstance(_seq, list) else _seq
    )

    main.auto_play()
    out = capsys.readouterr().out

    assert "AI" in out
    assert "Word was:" in out


def test_build_difficulty_configs_has_all_levels():
    configs = main.build_difficulty_configs()
    assert "easy" in configs
    assert "medium" in configs
    assert "hard" in configs
    assert configs["easy"].max_lives == 10
    assert configs["hard"].max_lives == 5
