'''
Clint Scott
2025_0323
CSD325 Advanced Python
Module 1.3 Assignment - On the Wall

Program Overview:
This program prints the lyrics of the "99 Bottles of Beer on the Wall" song based on a user-provided bottle count.
It ensures valid user input and follows a structured approach to output the lyrics.

Features & Flow:
- Prompts the user for the number of bottles to start with.
- Validates user input to ensure a positive integer is entered.
- Iterates through the countdown, printing each verse of the song.
- Properly formats singular and plural forms of "bottle" for grammatical correctness.
- Ends with a message prompting to buy more beer when the countdown is complete.

Prerequisites:
- Requires Python 3.13.x

References:
- Python 3.13 documentation: https://docs.python.org/3
- W3Schools Python Tutorial: https://www.w3schools.com/python
- Docstrings Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
'''

import sys
import textwrap

def display_welcome_screen() -> None:
    """
    Displays a welcome message explaining the purpose of the program.
    """
    message = """
    ***********************************************
    *  Welcome to the 99 Bottles of Beer Program  *
    ***********************************************
    
    This program will print the lyrics to the classic
    "99 Bottles of Beer on the Wall" song, starting
    from a number of bottles you choose.
    """
    print(textwrap.dedent(message))

def get_bottle_lyrics(count: int) -> None:
    """
    Prints the lyrics of the "99 Bottles of Beer on the Wall" song, counting down from the given number.
    
    :param count: The starting number of bottles to count down from.
    """
    for num in range(count, 0, -1):
        bottle_word = "bottle" if num == 1 else "bottles"
        next_bottle_word = "bottle" if (num - 1) == 1 else "bottles"
        next_num = num - 1

        print(f"{num} {bottle_word} of beer on the wall, {num} {bottle_word} of beer.")
        print(f"Take one down and pass it around, {next_num if next_num > 0 else '0'} {next_bottle_word} of beer on the wall.\n")

def get_user_input() -> int:
    """
    Prompts the user to enter the number of bottles to start with, ensuring a valid positive integer is provided.
    
    :return: An integer representing the number of bottles to start the countdown.
    """
    while True:
        try:
            bottles = input("Enter number of bottles: ").strip()
            print()
            if not bottles.isdigit():
                raise ValueError("Invalid input. Please enter a valid number.")
            bottles = int(bottles)
            if bottles < 1:
                print("Please enter a number greater than zero.")
                continue
            return bottles
        except ValueError as e:
            print(e)

def main() -> None:
    """
    Main function to execute the beer bottle countdown program.
    Prompts the user for input, prints the lyrics, and concludes with a message.
    """
    try:
        display_welcome_screen()
        bottles = get_user_input()
        get_bottle_lyrics(bottles)
        print("Time to buy more bottles of beer.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
