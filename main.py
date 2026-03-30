import random

words = ["python", "robot", "code", "game"]

word = random.choice(words)
guessed = ["_"] * len(word)
attempts = 6

print("Guess the word!")

while attempts > 0 and "_" in guessed:
    print("Word:", " ".join(guessed))
    letter = input("Enter a letter: ")

    if letter in word:
        for i in range(len(word)):
            if word[i] == letter:
                guessed[i] = letter
    else:
        attempts -= 1
        print("Wrong! Attempts left:", attempts)

if "_" not in guessed:
    print("You win! The word was:", word)
else:
    print("You lost! The word was:", word)