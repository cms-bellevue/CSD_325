import random

def get_user_guess():
    """
    Prompts the user to enter a guess and ensures valid input.
    :return: The guessed number as an integer.
    """
    while True:
        try:
            guess = int(input("Enter your guess (1-10): "))
            if 1 <= guess <= 10:
                return guess
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def number_guessing_game():
    """
    Runs a simple number guessing game where the user guesses a random number.
    """
    secret_number = random.randint(1, 10)
    attempts = 0
    
    print("Welcome to the Number Guessing Game!")
    
    while True:
        user_guess = get_user_guess()
        attempts += 1
        
        if user_guess == secret_number:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            break
        elif user_guess < secret_number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")

def main():
    """Main function to start the guessing game."""
    number_guessing_game()
    
if __name__ == "__main__":
    main()
