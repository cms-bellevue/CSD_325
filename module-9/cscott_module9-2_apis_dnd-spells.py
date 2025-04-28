'''
Clint Scott
CSD325 Advanced Python
Module 9.2 Assignment – APIs - D&D Highest Damage Spells
Updated: 2025-04-27

Program Overview:
This program fetches a list of spells from the D&D 5e API, identifies spells that deal damage,
calculates their potential maximum damage based on the highest available spell slot, and
displays the top 10 highest damage spells in a formatted table.

Features & Flow:
- Fetches spell data from the Open5e API.
- Extracts damage information, prioritizing the highest spell slot level.
- Calculates the maximum potential damage based on the damage dice notation (e.g., '3d6').
- Displays the top 10 damaging spells in a four-column table: Rank, Spell Name, Dice Roll, and Max Damage.
- Includes robust error handling for API requests and data parsing with retry logic.

Prerequisites:
- Requires the 'requests' and 'tabulate' Python libraries.
'''

import requests
from tabulate import tabulate
import time  # Import the time module for adding delays

# Base URL for accessing the D&D 5e API
BASE_URL = "https://www.dnd5eapi.co"
REQUEST_TIMEOUT = 5  # Set a timeout for API requests in seconds
RETRY_ATTEMPTS = 3  # Number of times to retry a failed request
RETRY_DELAY = 2  # Delay between retries in seconds

def calculate_potential_damage(damage_string):
    """
    Calculates the potential maximum damage of a spell based on its damage dice notation.

    For example, '3d6' is interpreted as 3 rolls of a 6-sided die, with a maximum
    potential damage of 3 * 6 = 18.

    Args:
        damage_string (str): A string representing the damage in 'd' notation (e.g., '3d6').

    Returns:
        tuple: A tuple containing the calculated potential maximum damage (int) and
               the original damage string (str), or (0, damage_string) if the damage
               string is not in the expected format or if an error occurs during parsing.
    """
    try:
        parts = damage_string.lower().split('d')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            num_dice = int(parts[0])
            die_sides = int(parts[1])
            max_damage = num_dice * die_sides
            return max_damage, damage_string
    except AttributeError:
        print(f"Error: Invalid damage string format: {damage_string}")
    except ValueError:
        print(f"Error: Non-numeric characters in damage string: {damage_string}")
    return 0, damage_string

def fetch_url_with_retry(url, timeout=REQUEST_TIMEOUT, retries=RETRY_ATTEMPTS, delay=RETRY_DELAY):
    """
    Fetches data from a given URL with retry logic for connection-related errors.

    Args:
        url (str): The URL to fetch.
        timeout (int): The request timeout in seconds.
        retries (int): The maximum number of retry attempts.
        delay (int): The delay between retries in seconds.

    Returns:
        requests.Response or None: The response object if successful, None otherwise.
    """
    for i in range(retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL '{url}' (Attempt {i+1}/{retries+1}): {e}")
            if i < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to fetch URL '{url}' after {retries + 1} attempts.")
                return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching '{url}': {e}")
            return None
    return None

def fetch_all_spells():
    """
    Fetches a list of all spells from the D&D 5e API.

    Returns:
        list: A list of spell dictionaries (from fetch_all_spells), or an empty
              list if the request fails.
    """
    api_url = f"{BASE_URL}/api/spells"
    response = fetch_url_with_retry(api_url)
    if response:
        try:
            spells_data = response.json()
            return spells_data.get('results', [])
        except ValueError as e:
            print(f"Error decoding JSON for all spells: {e}")
            return []
    return []

def fetch_spell_details(spell_url):
    """
    Fetches detailed information for a specific spell from the D&D 5e API with retry logic.

    Args:
        spell_url (str): The API URL for the spell.

    Returns:
        dict: A dictionary containing the spell details, or None if the request fails after retries.
    """
    full_url = f"{BASE_URL}{spell_url}"
    response = fetch_url_with_retry(full_url)
    if response:
        try:
            return response.json()
        except ValueError as e:
            print(f"Error decoding JSON for spell '{spell_url}': {e}")
            return None
    return None

def find_highest_damage_spells(spells):
    """
    Identifies spells with damage information and determines their potential maximum damage
    at the highest available slot level.

    Args:
        spells (list): A list of spell dictionaries (from fetch_all_spells).

    Returns:
        list: A list of dictionaries, where each dictionary contains the spell name,
              the dice roll needed, and its potential maximum damage, sorted in
              descending order of damage.
    """
    damage_spells = []
    for spell in spells:
        spell_details = fetch_spell_details(spell['url'])
        if spell_details and 'damage' in spell_details:
            spell_name = spell_details.get('name', 'Unknown Spell')
            damage_info = spell_details['damage']
            damage_at_slot_level = damage_info.get('damage_at_slot_level')

            if damage_at_slot_level:
                try:
                    highest_slot = max(damage_at_slot_level.keys(), key=int)
                    damage_string = damage_at_slot_level[highest_slot]
                    max_damage, dice_roll = calculate_potential_damage(damage_string)
                    damage_spells.append({"name": spell_name, "dice": dice_roll, "damage": max_damage})
                except ValueError:
                    print(f"Warning: Non-integer slot level found for spell '{spell_name}'.")
                except Exception as e:
                    print(f"Error processing damage for spell '{spell_name}': {e}")
            else:
                # Check for immediate damage dice if no slot level scaling
                damage_dice = damage_info.get('damage_dice')
                if damage_dice:
                    max_damage, dice_roll = calculate_potential_damage(damage_dice)
                    damage_spells.append({"name": spell_name, "dice": dice_roll, "damage": max_damage})

    damage_spells.sort(key=lambda x: x["damage"], reverse=True)
    return damage_spells

def display_top_damage_spells_table(top_spells, num_spells=10):
    """
    Displays the top N highest damage spells in a column-based table format.

    Args:
        top_spells (list): A sorted list of dictionaries, where each dictionary
                           contains the spell name, the dice roll needed, and its
                           potential maximum damage.
        num_spells (int): The number of top spells to display (default is 10).
    """
    print(f"\nTop {num_spells} Highest Potential Damage Magic User Spells:")
    if not top_spells:
        print("No damage-dealing spells found.")
        return

    headers = ["Rank", "Spell Name", "Dice Roll", "Max Damage"]
    table_data = []
    for i, spell_data in enumerate(top_spells[:num_spells], 1):
        table_data.append([i, spell_data["name"], spell_data["dice"], spell_data["damage"]])

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def main():
    """
    Main function to fetch D&D spells, identify those with damage, calculate their
    potential maximum damage, and display the top 10 highest damage spells in a table
    showing the rank, spell name, the dice roll needed, and the maximum damage.
    Includes retry logic for API requests.
    """
    all_spells = fetch_all_spells()
    if all_spells:
        highest_damage_spells = find_highest_damage_spells(all_spells)
        display_top_damage_spells_table(highest_damage_spells)
    else:
        print("Could not retrieve the list of spells from the API.")

if __name__ == "__main__":
    main()