# Variables store information for later use. 
product_name = "Kalki"
price = 500
is_variable = True
description = "a natural bioculture"

print(product_name)
print(price)
print(is_variable)
print(description) 

# F-strings - inserting variables into text
product_name = "Kalki"
price = 500
stock = 25

summary = f"Product: {product_name} | Price: Rs.{price} | Units in stock: {stock}"
print(summary)

# You can even do math inside f-strings
print(f"Total inventory value: Rs.{price * stock}")

# Lists - storing multiple items in one variable
products = ["Kalki", "Audumbar", "GauSanjeevan"]
prices = [500, 750, 300]

print(products)
print(prices)

# Accessing individual items (counting starts at 0, not 1!)
print(products[0])  # First item
print(products[1])  # Second item
print(products[2])  # Third item

# Loops - doing something for every item in a list
products = ["Kalki", "Audumbar", "GauSanjeevan"]
prices = [500, 750, 300]

# Basic loop
for product in products:
    print(f"Product: {product}")

# Loop with index number
for i, product in enumerate(products):
    print(f"{i+1}. {product} costs Rs.{prices[i]}")

# Conditionals - making decisions
products = ["Kalki", "Audumbar", "GauSanjeevan"]
prices = [500, 750, 300]

for i, product in enumerate(products):
    price = prices[i]
    
    if price > 600:
        print(f"{product}: Premium product (Rs.{price})")
    elif price > 400:
        print(f"{product}: Mid-range product (Rs.{price})")
    else:
        print(f"{product}: Budget product (Rs.{price})")    

# Functions - reusable blocks of code
def analyze_product(product_name, price):
    if price > 600:
        category = "Premium"
    elif price > 400:
        category = "Mid-range"
    else:
        category = "Budget"
    
    return f"{product_name} is a {category} product at Rs.{price}"

# Now call the function for different products
result1 = analyze_product("Kalki", 500)
result2 = analyze_product("Audumbar", 750)
result3 = analyze_product("GauSanjeevan", 300)

print(result1)
print(result2)
print(result3)

# Dictionary - storing labeled information (like a real dictionary with words and definitions)
product = {
    'name': 'Kalki',
    'price': 500,
    'category': 'Bioculture',
    'in_stock': True
}

# Accessing values by their labels (called "keys")
print(product['name'])
print(product['price'])
print(product['category'])

# Adding new information
product['supplier'] = 'Audumbar Kalki'
print(product)

# Dictionary inside a list - like your HN analyzer!
comments_data = [
    {
        'author': 'deathanatos',
        'date': '2024-01-15',
        'story': 'Rain simulator',
        'comment': 'Oh man, as a southerner stuck in California...'
    },
    {
        'author': 'tremendo',
        'date': '2024-01-16',
        'story': 'Ask HN: Favorite poets',
        'comment': 'Gustavo Adolfo Becquer...'
    }
]

# Loop through list of dictionaries (this is EXACTLY what your HN analyzer does!)
for comment in comments_data:
    print(f"Author: {comment['author']}")
    print(f"Story: {comment['story']}")
    print(f"Comment: {comment['comment'][:50]}...")  # First 50 characters only
    print("---")

# Looping through dictionary keys and values
product = {'name': 'Kalki', 'price': 500, 'category': 'Bioculture'}

# Just the keys
for key in product.keys():
    print(key)

print("---")

# Keys AND values together
for key, value in product.items():
    print(f"{key}: {value}")

# Imports - using code that other people wrote
import random
import datetime

# random library - generates random numbers
random_number = random.randint(1, 100)
print(f"Random number between 1-100: {random_number}")

# datetime library - works with dates and times
today = datetime.datetime.now()
print(f"Current date and time: {today}")
print(f"Just the date: {today.date()}")        

# The 'requests' library is what makes your HN analyzer work!
# It's not built into Python, so we installed it with: pip install requests

import requests

# Making a web request (this is what your analyzer does)
response = requests.get("https://hn.algolia.com/api/v1/search?query=python&tags=comment")

print(f"Status code: {response.status_code}")  # 200 means success
print(f"Got {len(response.json()['hits'])} results")

# Without error handling - this would crash
# result = 10 / 0  # Can't divide by zero!

# With error handling - catches the error gracefully
try:
    result = 10 / 0
    print(result)
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
    
print("Program continues running...")

# Practical example - handling missing data
products = [
    {'name': 'Kalki', 'price': 500},
    {'name': 'Audumbar'}  # Missing price!
]

for product in products:
    try:
        total = product['price'] * 2
        print(f"{product['name']}: Rs.{total}")
    except KeyError:
        print(f"{product['name']}: Price not available")

import csv

# Your comments_data from before (list of dictionaries)
comments_data = [
    {'author': 'deathanatos', 'date': '2024-01-15', 'story': 'Rain simulator', 'comment': 'Oh man...'},
    {'author': 'tremendo', 'date': '2024-01-16', 'story': 'Ask HN: Poets', 'comment': 'Gustavo...'}
]

# Writing to CSV - let's break it down line by line
filename = 'test_comments.csv'

# 'with open()' - opens a file and automatically closes it when done
# 'w' = write mode (creates new file or overwrites existing)
# 'newline' and 'encoding' = technical settings for CSV format
with open(filename, 'w', newline='', encoding='utf-8') as f:
    
    # DictWriter - writes dictionaries to CSV
    # fieldnames - tells it which dictionary keys become column headers
    writer = csv.DictWriter(f, fieldnames=['author', 'date', 'story', 'comment'])
    
    # Write the header row (column names)
    writer.writeheader()
    
    # Write all the data rows
    writer.writerows(comments_data)

print(f"Created {filename} successfully!")