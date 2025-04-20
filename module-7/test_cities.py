'''
Clint Scott
2025_0420
CSD325 Advanced Python
Module 7.2 Assignment – Test Cities
'''


import unittest
from city_functions import format_city_country

class CityCountryTestCase(unittest.TestCase):
    """Tests for the format_city_country function."""

    def test_city_country(self):
        """Do city and country names like 'Santiago' and 'Chile' work?"""
        formatted = format_city_country("Santiago", "Chile")
        self.assertEqual(formatted, "Santiago, Chile")

if __name__ == '__main__':
    unittest.main()