import random

def guess_the_number():
    name = input("Hello! What is your name? ")  
    number = random.randint(1, 20)  
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")

    attempts = 0

    while True:
        guess = int(input("Take a guess: "))  
        attempts += 1

        if guess == number:
            print(f"Good job, {name}! You guessed my number in {attempts} guesses!")
            break  
        print("Your guess is too low." if guess < number else "Your guess is too high.")

guess_the_number()
