import random

# words = ['appreciate', 'apprentice', 'approachable', 'apparently','applicable','appropriate']
# word = random.choice(words)
# word_letters = set(word)
# guessed_letters = set()
# lives = 7

with open('words.txt', 'r') as file:
    words = [line.strip().lower() for line in file if line.strip()]

    word = random.choice(words)
    word_letters = set(word)
    guessed_letters = set()
    lives = 7

print("Welcome to Hangman!")

allowed_errors = 6
guesses = []
done = False

while not done:
    for letter in word:
        if letter.lower() in guesses:
            print(letter, end = " ")

        else:
            print("_", end= " ")
    print("")
    done = True

    guess = input (f"Allowed Errors left{allowed_errors},Next guess: ")
    guesses.append (guess.lower())
    if guess.lower()not in word.lower(): 
        allowed_errors = 1
        if allowed_errors == 0:
            break 

    done = True 
    for letter in word:
        if letter.lower() not in guesses:
            done = False 

if done:
    print (f"You found the word: It was {word}!")
else:
    print(f"Game Over! The word was ")

