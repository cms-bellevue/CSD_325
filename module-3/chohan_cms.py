'''
Clint Scott
2025_0323
CSD325 Advanced Python
Module 2.2 Assignment: Cho-Han Revision

Cho-Han, by Al Sweigart al@inventwithpython.com
The traditional Japanese dice game of even-odd.
View this code athttps://nostarch.com/big-book-small-python-projects
Tags: short, beginner, game

Revisions:
- Implemented house fee percentage for each win.
- Added bonus for specific rolls (2 and 7).
- Included more detailed prompts and input validation.
- Improved handling of the game summary when quitting.
- Added purse balance checks to end the game when the player runs out of money or chooses to quit.

Features & Flow:
1. Initial Setup: The game starts with the player having 5000 mon in their purse.
2. Main Game Loop: 
   - The player is prompted to place a valid bet or quit the game.
   - Two dice are rolled, and the player guesses whether the total will be CHO (even) or HAN (odd).
   - The dice and their total are displayed, and the winner is determined based on the player's guess.
   - If the player wins, they earn the bet amount (minus a house fee). If they lose, the bet is subtracted from their purse.
   - Special bonus rolls (2 or 7) reward the player with 10 mon.
3. End Conditions: The game ends when the player chooses to quit or their purse reaches zero.
4. Game Summary: After quitting or finishing, the game displays the player's wins, losses, money won, money lost, and the net result of their betting.

Prerequisites:
- Requires Python 3.13.x

References:
- Python 3.13 documentation: https://docs.python.org/3
- W3Schools Python Tutorial: https://www.w3schools.com/python
- Docstrings Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
'''


import random
import sys

# Constants
JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN', 4: 'SHI', 5: 'GO', 6: 'ROKU'}
HOUSE_FEE_PERCENTAGE = 12  # House fee percentage
BONUS_ROLLS = {2, 7}  # Rolls that trigger a bonus
MINIMUM_BET = 10

def get_valid_bet(purse):
    """
    Prompts the user to place a valid bet. Validates input for positive integers.

    Args:
        purse (int): The amount of money the player currently has.

    Returns:
        int: The valid bet placed by the player.
    """
    
    while True:
        print(f'You have {purse} mon. How much do you bet? (or QUIT)')
        try:
            bet_input = input('cms: ')

            if bet_input.upper() == 'QUIT':
                return 'QUIT'

            if not bet_input.isdecimal():
                print('Please enter a positive integer for your bet.')
                continue

            bet = int(bet_input)
            if bet > purse:
                print('You do not have enough to make that bet.')
            elif bet <= 0:
                print('Please enter a positive number greater than zero for your bet.')
            elif bet < MINIMUM_BET:
                print(f'Please enter a bet of at least {MINIMUM_BET} mon.')
            else:
                return bet
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting...")
            sys.exit()

def get_bet_choice():
    """
    Prompts the user to choose between 'CHO' (even) or 'HAN' (odd). Handles invalid inputs.

    Returns:
        str: The valid bet choice ('CHO' or 'HAN').
    """
    while True:
        bet_choice = input('cms: ').upper()
        if bet_choice in ['CHO', 'HAN']:
            return bet_choice
        print('Invalid choice. Please enter "CHO" (even) or "HAN" (odd).')

def play_game():
    """
    The main game loop for Cho-Han. Handles player input, game logic, and updates purse.
    """
    purse = 5000
    wins = 0
    losses = 0
    money_won = 0
    money_lost = 0
    starting_purse = purse

    print('''Cho-Han, by Al Sweigart al@inventwithpython.com

In this traditional Japanese dice game, two dice are rolled in a bamboo
cup by the dealer sitting on the floor. The player must guess if the
dice total to an even (cho) or odd (han) number.

NOTICE: If the dice roll totals to 2 or 7, you receive a 10 mon bonus!
''')

    while True:
        pot = get_valid_bet(purse)
        
        if pot == 'QUIT':
            print('Thanks for playing!')
            print(f'Game Summary:')
            print(f'Wins: {wins}, Losses: {losses}')
            net_money = money_won - money_lost
            print(f'Money Won: {money_won} mon, Money Lost: {money_lost} mon')
            print(f'Net Result: {"+" if net_money >= 0 else ""}{net_money} mon')
            print(f'Final Purse: {purse} mon (Started with {starting_purse} mon)')
            sys.exit()

        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        total = dice1 + dice2

        print('The dealer swirls the cup and you hear the rattle of dice.')
        print('The dealer slams the cup on the floor, still covering the')
        print('dice and asks for your bet.')
        print()
        print('    CHO (even) or HAN (odd)?')

        bet = get_bet_choice()

        print('The dealer lifts the cup to reveal:')
        print(f'  {JAPANESE_NUMBERS[dice1]} - {JAPANESE_NUMBERS[dice2]}')
        print(f'    {dice1} - {dice2}')
        print(f'    Total: {total}')  # Added total display

        roll_is_even = total % 2 == 0
        correct_bet = 'CHO' if roll_is_even else 'HAN'
        player_won = bet == correct_bet

        if player_won:
            wins += 1
            print(f'You won! You take {pot} mon.')
            purse += pot
            money_won += pot
            house_fee = pot * HOUSE_FEE_PERCENTAGE // 100
            print(f'The house collects a {house_fee} mon fee.')
            purse -= house_fee
            money_lost += house_fee
            if purse <= 0:  # Check after house fee
                print('The house fee has left you with no money!')
                print('Thanks for playing!')
                print(f'Game Summary: Wins: {wins}, Losses: {losses}')
                print(f'Money Won: {money_won} mon, Money Lost: {money_lost} mon')
                sys.exit()
        else:
            losses += 1
            purse -= pot
            money_lost += pot
            print('You lost!')

        if total in BONUS_ROLLS:
            print(f'Lucky roll! The total was {total}. You receive a 10 mon bonus!')
            purse += 10
            money_won += 10

        print(f'Your purse: {purse} mon')  # Added purse summary
        if purse <= 0:
            print('You have run out of money!')
            print('Thanks for playing!')
            print(f'Game Summary: Wins: {wins}, Losses: {losses}')
            print(f'Money Won: {money_won} mon, Money Lost: {money_lost} mon')
            sys.exit()

if __name__ == "__main__":
    play_game()