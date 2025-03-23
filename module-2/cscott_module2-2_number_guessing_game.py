'''
Clint Scott
2025_0323
CSD325 Advanced Python
Module 2.2 Assignment - Number Guessing Game

Program Overview:
This program runs a number guessing game where the user attempts to guess a randomly chosen number between 1 and 10.
The program provides feedback on whether the guess is too high or too low and tracks the number of attempts.

Features & Flow:
- Generates a random number between 1 and 10.
- Prompts the user for input and validates that it is a valid integer within the range.
- Provides feedback on whether the guess is too high, too low, or correct.
- Tracks the number of attempts and displays it upon successful guessing.
- Handles invalid input gracefully to prevent crashes.

Prerequisites:
- Requires Python 3.13.x

References:
- Python 3.13 documentation: https://docs.python.org/3
- W3Schools Python Tutorial: https://www.w3schools.com/python
- Docstrings Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
'''

import random, sys, textwrap

def display_welcome_screen() -> None:
    """
    Displays a welcome message explaining the purpose of the program.
    """
    message = """
    *****************************************
    *  Welcome to the Number Guessing Game  *
    *****************************************
    
    Try to guess the randomly chosen number between 1 and 10.
    """
    print(textwrap.dedent(message))

def get_user_guess() -> int:
    """
    Prompts the user to enter a guess and ensures valid input.
    
    :return: The guessed number as an integer.
    """
    while True:
        try:
            guess = input("Enter your guess (1-10): ").strip()
            if not guess.isdigit():
                raise ValueError("Invalid input. Please enter a valid number.")
            guess = int(guess)
            if 1 <= guess <= 10:
                return guess
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError as e:
            print(e)

def number_guessing_game() -> None:
    """
    Runs a simple number guessing game where the user guesses a random number.
    """
    secret_number = random.randint(1, "10")
    attempts = 0
    
    display_welcome_screen()
    
    while True:
        user_guess = get_user_guess()
        attempts += 1
        
        if user_guess == secret_number:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            if attempts == 1:
                print("Are you a wizard?")
            break
        elif user_guess < secret_number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")

def main() -> None:
    """
    Main function to start the guessing game.
    Handles user interruptions gracefully.
    """
    try:
        number_guessing_game()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()