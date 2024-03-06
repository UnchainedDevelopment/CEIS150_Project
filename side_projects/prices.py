## CEIS150 Week 1 Project prices.py
## Joseph Brisendine
## Professor Nana Liu
## 02/26/2024

full_name = input("Please enter your full name: ")
count = 0
total_price = 0
while True:
    min_price_str = input("Please tell us your lowest costing item (enter with $): ")
    if min_price_str.startswith('$'):
        try:
            min_price = float(min_price_str.replace('$', ''))
            break  # Exit the loop if the input is valid
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")
    else:
        print("Invalid input. Please include the '$' symbol.")
prices_str = "45.2, 62.8, 73.5, 88.7, 55.3, 78.6, 92.1, 64.4, 81.9, 95.0"
prices_list = [float(price) for price in prices_str.split(',')]

def prices():
    global count, total_price  # Use global keyword to modify the global variables
    print("Welcome to Unchained Pricing, " + full_name)
    for price in prices_list:
        total_price += price  # Add current price to total_price
        if price > min_price:
            count += 1  # Increment count by 1

prices()

print(full_name, "the minimum price is $"+ str(min_price))
print("There are ", count, "prices greater than the minimum price")
print("The total price is $" + str(total_price))
greater_prices = [price for price in prices_list if price > min_price]
print("The greater costing items are: $" + ", $".join(map(str, greater_prices)))



