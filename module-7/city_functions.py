# city_functions.py

def format_city_country(city, country, population=None, language=None):
    """
    Return a formatted string based on provided values:
    - City, Country
    - City, Country - population xxx
    - City, Country - population xxx, Language
    """
    result = f"{city}, {country}"

    if population:
        result += f" - population {population}"

    if language:
        result += f", {language}"

    return result


# Call the function three times with explanations

print("Call 1 (City, Country):")
print(format_city_country("Tokyo", "Japan"))

print("\nCall 2 (City, Country, Population):")
print(format_city_country("New York City", "USA", 8300000))

print("\nCall 3 (City, Country, Population, Language):")
print(format_city_country("Santiago", "Chile", 5000000, "Spanish"))
