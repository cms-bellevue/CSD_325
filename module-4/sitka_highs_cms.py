'''
Clint Scott  
2025_0405  
CSD325 Advanced Python  
Module 4.2 Assignment: Sitka Weather Graph - Highs and Lows Interactive with Combined Option  

Based on the Sitka weather data CSV used in the Python Crash Course examples.  
Original code by Eric Matthes.  
Modified to allow dynamic user selection between highs, lows, both, with looping and error handling.  

Revisions:
- Added interactive menu to select between high temps, low temps, both, or exit.
- Implemented loop to allow multiple graph selections until user exits.
- Incorporated graceful exit handling via sys.exit().
- Included error handling for file access, data parsing, and invalid inputs.
- Added detailed comments, docstrings, and structure to reflect consistent coding style.

Features & Flow:
1. Program displays a menu offering four options: Highs, Lows, Both, or Exit.
2. Based on user input, the program reads and parses the CSV file to collect the appropriate temperature data.
3. It generates and displays a Matplotlib line chart with the selected data:
   - Highs: red line
   - Lows: blue line
   - Both: both lines on same chart
4. The loop continues until the user chooses to exit.
5. On exit, a confirmation message is shown and the program ends cleanly.

Prerequisites:
- Requires Python 3.13.x
- Requires matplotlib for graphing: pip install matplotlib

References:
- Python 3.13 documentation: https://docs.python.org/3
- W3Schools Python Tutorial: https://www.w3schools.com/python
- Matplotlib Docs: https://matplotlib.org/stable/contents.html
- Docstrings Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
'''

import csv
import sys
from datetime import datetime
import matplotlib.pyplot as plt

# Constants
FILENAME = 'sitka_weather_2018_simple.csv'
HIGH_INDEX = 5
LOW_INDEX = 6
DATE_INDEX = 2

# Initialize data lists
dates, highs, lows = [], [], []

def read_weather_data(filename):
    """
    Reads weather data from the given CSV file and populates
    the global lists: dates, highs, and lows.
    """
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)

            for row_num, row in enumerate(reader, start=2):
                try:
                    current_date = datetime.strptime(row[DATE_INDEX], '%Y-%m-%d')
                    high = int(row[HIGH_INDEX])
                    low = int(row[LOW_INDEX])
                except (ValueError, IndexError) as e:
                    print(f"[Warning] Skipping invalid row {row_num}: {e}")
                    continue
                dates.append(current_date)
                highs.append(high)
                lows.append(low)

    except FileNotFoundError:
        print(f"[Error] File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] Unexpected error reading file: {e}")
        sys.exit(1)

def plot_temps(temp_type):
    """
    Plots temperature data based on user input.
    temp_type -- 'high', 'low', or 'both'.
    """
    fig, ax = plt.subplots()
    try:
        if temp_type == 'high':
            ax.plot(dates, highs, c='red')
            plt.title("Daily High Temperatures - 2018", fontsize=24)
        elif temp_type == 'low':
            ax.plot(dates, lows, c='blue')
            plt.title("Daily Low Temperatures - 2018", fontsize=24)
        elif temp_type == 'both':
            ax.plot(dates, highs, c='red', label='Highs')
            ax.plot(dates, lows, c='blue', label='Lows')
            plt.title("Daily High/Low Temperatures - 2018", fontsize=24)
            ax.legend()

        plt.xlabel('', fontsize=16)
        fig.autofmt_xdate()
        plt.ylabel("Temperature (F)", fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=16)

        plt.show()
    except KeyboardInterrupt:
        print("\n[Notice] Plot window closed or interrupted.")
    except Exception as e:
        print(f"[Error] Failed to display plot: {e}")

def display_menu():
    """Displays the temperature selection menu."""
    print("\nWeather Data Viewer")
    print("Select an option:")
    print("  1 - View High Temperatures")
    print("  2 - View Low Temperatures")
    print("  3 - View Both High and Low Temperatures")
    print("  4 - Exit")

def main():
    """Main program loop."""
    read_weather_data(FILENAME)
    while True:
        display_menu()
        try:
            choice = input("Enter choice (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Info] Input interrupted. Exiting program.")
            sys.exit(0)

        if choice == '1':
            plot_temps('high')
        elif choice == '2':
            plot_temps('low')
        elif choice == '3':
            plot_temps('both')
        elif choice == '4':
            print("\nThanks for using the weather data viewer. Goodbye!")
            sys.exit(0)
        else:
            print("[Warning] Invalid selection. Please choose 1, 2, 3, or 4.")

if __name__ == '__main__':
    main()
