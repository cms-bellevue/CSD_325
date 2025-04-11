"""Forest Fire Sim, modified by Sue Sampson, based on a program by Al Sweigart
A simulation of wildfires spreading in a forest. Press Ctrl-C to stop.
Inspired by Nicky Case's Emoji Sim http://ncase.me/simulating/model/
** use spaces, not indentation to modify **
Tags: short, bext, simulation"""

import random, sys, time, subprocess

def install_bext():
    """Install 'bext' if it's not installed and attempt to import it."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'bext'])
        print('bext has been successfully installed.')
        try:
            import bext
            print('Press Enter to continue...')  # Added pause for user confirmation -cms
            input()  # Added pause for user confirmation -cms
            return bext  # Return the imported module -cms
        except ImportError:
            print('Installation succeeded, but bext still cannot be imported. Please restart the script manually.')
            sys.exit(1)
    except Exception as e:
        print('Failed to install bext. Ensure pip is installed and try again manually.')
        print(f'Technical detail: {e}')
        sys.exit(1)

# Try importing bext
try:
    import bext
except ImportError:
    print('This program requires the bext module.')
    print('1. Install bext now') # Added option to install bext -cms
    print('2. Exit program')
    while True:
        choice = input('Choose an option (1 or 2): ').strip()
        if choice in ('1', '2'):
            break
        print('Invalid choice. Please enter 1 or 2.')

    if choice == '1':
        bext = install_bext()  # Get the imported module instead of restarting -cms
    else:
        print('Exiting program.')
        sys.exit()

# Set up the constants:
WIDTH = 79
HEIGHT = 22

TREE = 'A'
FIRE = '@'
EMPTY = ' '

# Try changing these settings to anything between 0.0 and 1.0:
INITIAL_TREE_DENSITY = 0.20  # Amount of forest that starts with trees.
GROW_CHANCE = 0.01  # Chance a blank space turns into a tree.
FIRE_CHANCE = 0.01  # Chance a tree is hit by lightning & burns.

# Try setting the pause length to 1.0 or 0.0:
PAUSE_LENGTH = 0.5

def main():
    forest = createNewForest()
    bext.clear()

    while True:  # Main program loop.
        displayForest(forest)

        # Run a single simulation step:
        nextForest = {'width': forest['width'], 'height': forest['height']}

        for x in range(forest['width']):
            for y in range(forest['height']):
                if (x, y) in nextForest:
                    # If we've already set nextForest[(x, y)] on a previous iteration, just do nothing here:
                    continue

                if (forest[(x, y)] == EMPTY) and (random.random() <= GROW_CHANCE):
                    # Grow a tree in this empty space.
                    nextForest[(x, y)] = TREE
                elif (forest[(x, y)] == TREE) and (random.random() <= FIRE_CHANCE):
                    # Lightning sets this tree on fire.
                    nextForest[(x, y)] = FIRE
                elif forest[(x, y)] == FIRE:
                    # This tree is currently burning.
                    # Loop through all the neighboring spaces:
                    for ix in range(-1, 2):
                        for iy in range(-1, 2):
                            # Fire spreads to neighboring trees:
                            if forest.get((x + ix, y + iy)) == TREE:
                                nextForest[(x + ix, y + iy)] = FIRE
                    # The tree has burned down now, so erase it:
                    nextForest[(x, y)] = EMPTY
                else:
                    # Just copy the existing object:
                    nextForest[(x, y)] = forest[(x, y)]
        forest = nextForest

        time.sleep(PAUSE_LENGTH)

def createNewForest():
    """Returns a dictionary for a new forest data structure."""
    forest = {'width': WIDTH, 'height': HEIGHT}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if (random.random() * 100) <= INITIAL_TREE_DENSITY:
                forest[(x, y)] = TREE  # Start as a tree.
            else:
                forest[(x, y)] = EMPTY  # Start as an empty space.
    return forest

def displayForest(forest):
    """Display the forest data structure on the screen."""
    bext.goto(0, 0)  # Fixed indentation from original code -cms
    for y in range(forest['height']):
        for x in range(forest['width']):
            if forest[(x, y)] == TREE:
                bext.fg('green')
                print(TREE, end='')
            elif forest[(x, y)] == FIRE:
                bext.fg('red')
                print(FIRE, end='')
            elif forest[(x, y)] == EMPTY:
                print(EMPTY, end='')
        print()
    bext.fg('reset')  # Use the default font color.
    print('Grow chance: {}%  '.format(GROW_CHANCE * 100), end='')
    print('Lightning chance: {}%  '.format(FIRE_CHANCE * 100), end='')
    print('Press Ctrl-C to quit.')

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nSimulation stopped. Thanks for running the Forest Fire Sim!')  # Enhanced exit message for better UX -cms
        sys.exit()  # Clean exit on Ctrl-C -cms