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


def test_play_game_handles_invalid_then_repeated_then_wins(monkeypatch, capsys):
    monkeypatch.setattr(main.random, "choice", lambda _words: "python")

    # invalid -> valid -> repeated -> finish winning sequence
    inputs = iter(["", "p", "p", "y", "t", "h", "o", "n"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    main.play_game()
    out = capsys.readouterr().out

    assert "Invalid input. Enter a single letter (a-z)." in out
    assert "You already guessed that letter." in out
    assert "You win! Word was: python" in out


def test_play_game_loss_path(monkeypatch, capsys):
    monkeypatch.setattr(main.random, "choice", lambda _words: "python")

    # 6 unique wrong letters to exhaust lives
    inputs = iter(["a", "b", "c", "d", "e", "f"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    main.play_game()
    out = capsys.readouterr().out

    assert "You lost! Word was: python" in out


def test_auto_play_terminates_and_prints_result(monkeypatch, capsys):
    monkeypatch.setattr(main.random, "choice", lambda _seq: _seq[0])

    main.auto_play()
    out = capsys.readouterr().out

    assert "AI" in out
    assert "Word was:" in out


def test_main_menu_calls_play_and_quit(monkeypatch):
    called = {"play": 0, "auto": 0}

    monkeypatch.setattr(
        main, "play_game", lambda: called.__setitem__("play", called["play"] + 1)
    )
    monkeypatch.setattr(
        main, "auto_play", lambda: called.__setitem__("auto", called["auto"] + 1)
    )

    inputs = iter(["1", "q"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    main.main()

    assert called["play"] == 1
    assert called["auto"] == 0


def test_main_menu_calls_auto_and_quit(monkeypatch):
    called = {"play": 0, "auto": 0}

    monkeypatch.setattr(
        main, "play_game", lambda: called.__setitem__("play", called["play"] + 1)
    )
    monkeypatch.setattr(
        main, "auto_play", lambda: called.__setitem__("auto", called["auto"] + 1)
    )

    inputs = iter(["2", "q"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    main.main()

    assert called["play"] == 0
    assert called["auto"] == 1
