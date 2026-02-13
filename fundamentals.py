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
