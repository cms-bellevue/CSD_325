'''
Clint Scott
2025_0420
CSD325 Advanced Python
Module 9.2 Assignment – APIs
'''

import requests

# Test the connection
response = requests.get('http://api.open-notify.org/astros.json')
print(response.status_code)
