'''
Clint Scott
CSD325 Advanced Python
Module 9.2 Assignment – APIs - People In Space
Updated: 2025-04-27

Program Overview:
This program retrieves the current list of astronauts in space from the Open Notify API.
It fetches the data, parses the JSON response, and then displays the total number of
people currently in space along with the name and spacecraft of each individual.

Features & Flow:
- Makes an HTTP GET request to the Open Notify API endpoint for astronauts.
- Handles potential network errors and invalid JSON responses.
- Extracts and prints the count of astronauts.
- Iterates through the list of astronauts and displays their name and associated spacecraft.
- Includes retry logic for handling transient network issues.

Prerequisites:
- Requires the 'requests' Python library.
'''

import requests
import time  # Import the time module for adding delays

# API endpoint URL
API_URL = 'http://api.open-notify.org/astros.json'

# Constants for retry mechanism
REQUEST_TIMEOUT = 5  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

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

def get_astronauts_in_space():
    """
    Fetches the current list of astronauts in space from the Open Notify API
    and prints the number of people and their names along with their spacecraft.
    Includes retry logic for handling potential network issues.
    """
    response = fetch_url_with_retry(API_URL)

    if response:
        try:
            # Parse the JSON response into a Python dictionary
            data = response.json()

            # Print the raw response from the API (useful for debugging)
            print(f"Raw Response:\n{data}\n")

            # Extract the number of people currently in space
            number_of_astronauts = data.get('number')
            if number_of_astronauts is not None:
                print(f"There are {number_of_astronauts} people in space right now!\n")
            else:
                print("Could not retrieve the number of people in space.\n")
                return

            # Extract the list of people in space
            people_in_space = data.get('people')
            if people_in_space:
                # Loop through the list of people and print their name and spacecraft
                print("Astronauts currently in space:")
                for person in people_in_space:
                    name = person.get('name')
                    craft = person.get('craft')
                    if name and craft:
                        print(f"- {name} ({craft})")
                    else:
                        print("- Could not retrieve name or spacecraft for an astronaut.")
            else:
                print("Could not retrieve the list of people in space.")

        except ValueError as e:
            # Handle exceptions if the response is not valid JSON
            print(f"Failed to decode JSON response: {e}")
    else:
        print(f"Failed to retrieve data from {API_URL} after multiple retries.")

if __name__ == "__main__":
    # Call the function to get and print the astronaut data when the script is executed
    get_astronauts_in_space()