# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 22:57:11 2021

@author: Joseph Brisendine
"""
from datetime import datetime
from stock_class import Stock, DailyData
from account_class import  Traditional, Robo
import matplotlib.pyplot as plt
import csv
import os

def add_stock(stock_list):
    print("Add New Stock ----")
    
    # Get information for the new stock
    symbol = input("Enter Stock Symbol: ").upper()
    name = input("Enter Company Name: ")
    shares = int(input("Enter Number of Shares: "))

    # Check if the stock with the given symbol already exists
    existing_stock = next((stock for stock in stock_list if stock.symbol == symbol), None)

    if existing_stock:
        print(f"Stock with symbol {symbol} already exists. Updating shares.")
        existing_stock.shares += shares
    else:
        # Create a new stock and add it to the stock_list
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        print(f"Stock {symbol} added successfully.")

    _ = input("Press Enter to Continue ***")
    return stock_list  # Return the updated stock_list

# Remove stock and all daily data
def delete_stock(stock_list):
    print("Delete Stock ----")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, " ", end="")
    print("]")
    symbol = input("Which stock do you want to delete?: ").upper()

    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock_list.remove(stock)
            print(f"{symbol} deleted successfully.")
            break

    if not found:
        print(f"Stock with symbol {symbol} not found.")

    _ = input("Press Enter to Continue ***")

    
    
# List stocks being tracked
def list_stocks(stock_list):
    print("\nStock List\n")
    print("{:<10} {:<20} {:<10}".format("Symbol", "Name", "Shares"))
    print("-" * 40)

    for stock in stock_list:
        print("{:<10} {:<20} {:<10}".format(stock.symbol, stock.name, stock.shares))

    input("\nPress Enter to view more details...")

    for stock in stock_list:
        print("\nStock Details:")
        print(f"Symbol: {stock.symbol}")
        print(f"Name: {stock.name}")
        print(f"Shares: {stock.shares}")

        _ = input("\nPress Enter for the next stock...")

    input("\nPress Enter to continue...")

    
def add_stock_data(stock_list):
    print("Add Daily Stock Data ----")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, " ", end="")
    print("]")

    symbol = input("Which stock do you want to add data for?: ").upper()

    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
            break

    if found:
        print(f"Ready to add data for: {symbol}")

        date = input("Enter Date (or press Enter to quit): ")
        while date:
            try:
                price = float(input("Enter Price: "))
                volume = float(input("Enter Volume: "))

                daily_data = DailyData(date, price, volume)
                current_stock.add_data(daily_data)
                print("Data added successfully.")

            except ValueError:
                print("Invalid input. Please enter valid numerical values.")

            date = input("\nEnter Date (or press Enter to quit): ")

        print("Data Entry Complete")
    else:
        print(f"Symbol Not Found: {symbol}")

    _ = input("Press Enter to Continue ***")


    
def investment_type(stock_list):
    print("Investment Account ---")
    balance = float(input("What is your initial balance: "))
    number = input("What is your account number: ")
    acct= input("Do you want a Traditional (t) or Robo (r) account: ")
    if acct.lower() == "r":
        years = float(input("How many years until retirement: "))
        robo_acct = Robo(balance, number, years)
        print("Your investment return is ",robo_acct.investment_return())
        print("\n\n")
    elif acct.lower() == "t":
        trad_acct = Traditional(balance, number)
        temp_list=[]
        print("Choose stocks from the list below: ")
        while True:
            print("Stock List: [",end="")
            for stock in stock_list:
                print(stock.symbol," ",end="")
            print("]")
            symbol = input("Which stock do you want to purchase, 0 to quit: ").upper()
            if symbol =="0":
                break
            shares = float(input("How many shares do you want to buy?: "))
            found = False
            for stock in stock_list:
              if stock.symbol == symbol:
                  found = True
                  current_stock = stock
            if found == True:
                current_stock.shares += shares 
                temp_list.append(current_stock)
                print("Bought ",shares,"of",symbol)
            else:
                print("Symbol Not Found ***")
        trad_acct.add_stock(temp_list)
        current_stock.buy(shares)

# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    date = []
    price = []
    volume = []
    company = ""

    for stock in stock_list:
        if stock.symbol == symbol:
            company = stock.name
            for dailyData in stock.DataList:
                date.append(dailyData.date)
                price.append(dailyData.close)
                volume.append(dailyData.volume)
            break

    if date and price:
        plt.plot(date, price)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(company)
        plt.show()
    else:
        print("No data found for the specified symbol.")

# Function to display chart 
def display_chart(stock_list):
    print("Display Stock Chart ----")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, " ", end="")
    print("]")

    symbol = input("Enter the stock symbol you want to see the chart for: ").upper()

    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
            break

    if found:
        display_stock_chart(stock_list, symbol)
    else:
        print(f"Symbol Not Found: {symbol}")

    _ = input("Press Enter to Continue ***")

def import_stock_csv(stock_list):
    print("Import Stock Screen")
    for stock in stock_list:
        print(stock.symbol, end=" ")  # Output stock symbol without newline
    print("]")  # End of stock list

    filename = input("Input filename: ")  # Prompt user for filename

    # Construct the full path by joining the filename with the directory where the program is located
    full_path = os.path.join(os.getcwd(), filename)

    if not os.path.isfile(full_path):
        print(f"File not found: {filename}")
        return

    # Extract symbol from filename (assuming filename is in the format 'project_files/SYMBOL.csv')
    _, basename = os.path.split(filename)
    symbol = os.path.splitext(basename)[0].upper()

    # Prompt user to enter the symbol for the stock
    symbol_input = input(f"Enter symbol for {basename}: ").upper()

    # Check if the symbol already exists in the stock_list
    existing_stock = next((stock for stock in stock_list if stock.symbol == symbol_input), None)

    if existing_stock:
        print(f"Stock with symbol {symbol_input} already exists. Updating data.")
    else:
        # Create a new stock and add it to the stock_list
        name = input("Enter company name: ")
        shares = int(input("Enter number of shares: "))
        new_stock = Stock(symbol_input, name, shares)
        stock_list.append(new_stock)
        print(f"Stock {symbol_input} added successfully.")
        existing_stock = new_stock  # Assign the new stock as the existing_stock

    # Check if the symbol was found and data was successfully loaded
    try:
        with open(full_path, 'r') as stockdata:  # Open file as stockdata
            datareader = csv.reader(stockdata, delimiter=',')  # Set up CSV reader
            next(datareader)  # Skip header row
            for row in datareader:
                daily_data = DailyData(str(row[0]), float(row[4]), float(row[6]))  # Create DailyData object
                existing_stock.add_data(daily_data)  # Add daily_data to existing_stock's DataList
        print("Data uploaded successfully.")
        display_report(stock_list)  # Call display_report function passing stock_list
    except FileNotFoundError:
        print(f"File not found: {filename}")



   # Display Report 
def display_report(stock_list):
    print("Stock Report Screen")

    for stock in stock_list:
        print("Report for:", stock.symbol, stock.name)
        print("Shares:", stock.shares)

        count = 0
        price_total = 0
        volume_total = 0
        lowPrice = 999999.99
        highPrice = 0
        lowVolume = 999999999999
        highVolume = 0

        for daily_data in stock.DataList:  # Change 'data' to 'DataList'
            count += 1
            price_total += daily_data.close
            volume_total += daily_data.volume

            if daily_data.close < lowPrice:
                lowPrice = daily_data.close
            if daily_data.close > highPrice:
                highPrice = daily_data.close
            if daily_data.volume < lowVolume:
                lowVolume = daily_data.volume
            if daily_data.volume > highVolume:
                highVolume = daily_data.volume

        if count > 0:
            print("Summary ---")
            print("Low Price:", "${:,.2f}".format(lowPrice))
            print("High Price:", "${:,.2f}".format(highPrice))
            print("Average Price:", "${:,.2f}".format(price_total / count))
            print("Low Volume:", lowVolume)
            print("High Volume:", highVolume)
            print("Average Volume:", volume_total / count)
            priceChange = stock.DataList[-1].close - stock.DataList[0].close  # Change 'data' to 'DataList'
            print("Change in Price:", "${:,.2f}".format(priceChange))
            print("Profit/Loss:", "${:,.2f}".format(priceChange * stock.shares))
        else:
            print("No daily history")
        
        print("\n" * 3)  # Output 3 blank lines between stocks

    input("Report Complete. Press Enter to continue.")

def save_stock_data(stock_list):
    filename = input("Enter filename to save: ")

    try:
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            for stock in stock_list:
                for daily_data in stock.DataList:
                    writer.writerow([stock.symbol, daily_data.date, daily_data.close, daily_data.volume])
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")
    
def main_menu(stock_list):
    while True:
        print("Stock Analyzer ---")
        print("1 - Add Stock")
        print("2 - Delete Stock")
        print("3 - List stocks")
        print("4 - Add Daily Stock Data (Date, Price, Volume)")
        print("5 - Show Chart")
        print("6 - Investor Type")
        print("7 - Load Data")
        print("8 - Save Data")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        
        if option =="0":
            print("Goodbye")
            break
        
        elif option == "1":
            stock_list = add_stock(stock_list)
        
        elif option == "2":
            delete_stock(stock_list)
        
        elif option == "3":
            list_stocks(stock_list)
        
        elif option == "4":
            add_stock_data(stock_list) 
        
        elif option == "5":
            display_chart(stock_list)
        
        elif option == "6":
            investment_type(stock_list)
        
        elif option == "7":
            import_stock_csv(stock_list)
        
        elif option == "8":
            save_stock_data(stock_list)
        
        else:
            print("Invalid option. Please select a valid menu option.")
# Begin program
def main():
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
