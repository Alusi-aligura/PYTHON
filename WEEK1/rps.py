import random

play1 = input("Rock, Paper, or  Scissors?").strip().capitalize()
play2 = random.choice(["Rock", "Paper", "Scissors" ])
print("Bot:", play2) 

if play1 == play2:
    print("it's a tie!")

elif (play1 == "Rock" and play2 == "Scissors") or \
     (play1 == "Paper" and play2 == "Rock") or\
     (play1 == "Scissors" and play2 == "Paper"):
   print("You win!")
else:
   print(" sorry You lose!")

