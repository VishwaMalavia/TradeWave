import mysql.connector
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",        
            user='root', 
            password='', 
            database='stockmarketdb' 
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def admin_login(connection):
    try:
        username = input("Enter Admin Username: ").strip()
        password = input("Enter Admin Password: ").strip()
        cursor = connection.cursor()
        
        query = "SELECT * FROM Admin WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            print("Login successful!")
            return True
        else:
            print("Invalid credentials.")
            return False
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
            print(f"An error occurred: {e}")

def admin_actions(connection):
    while True:
        print("\nAdmin Menu:")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Update Stock")
        print("4. View All Stocks")
        print("5. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        try:
            if choice == '1':
                add_stock(connection)
            elif choice == '2':
                remove_stock(connection)
            elif choice == '3':
                update_stock(connection)
            elif choice == '4':
                view_all_stocks(connection)
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def add_stock(connection):
    try:
        stock_name = input("Enter stock name: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        while not validate_date(date):
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
            date = input("Enter date (YYYY-MM-DD): ").strip()
            
        open_price = float(input("Enter open price: ").strip())
        close_price = float(input("Enter close price: ").strip())
        high = float(input("Enter high price: ").strip())
        low = float(input("Enter low price: ").strip())
        volume = int(input("Enter volume: ").strip())

        cursor = connection.cursor()
        query = """
        INSERT INTO StockList (stock_name, date, open_price, close_price, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, (stock_name, date, open_price, close_price, high, low, volume))
        connection.commit()
        cursor.close()
        print("Stock added successfully.")
    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_stock(connection):
    try:
        view_all_stocks(connection)
        stock_id = input("Enter stock ID to remove: ").strip()
        cursor = connection.cursor()
        query = "DELETE FROM StockList WHERE stock_id = %s"
        cursor.execute(query, (stock_id,))
        connection.commit()
        cursor.close()
        print("Stock removed successfully.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_stock(connection):
    try:
        view_all_stocks(connection)
        stock_id = input("Enter stock ID to update: ").strip()
        column = input("Enter column to update (stock_name, date, open_price, close_price, high, low, volume): ").strip()
        value = input("Enter new value: ").strip()

        columns_list = column.split(",")
        values_list = value.split(",")

        if len(columns_list) != len(values_list):
            print("Error: Number of columns and values must match.")
            return
        
        cursor = connection.cursor()
        set_clause = ", ".join([f"{col.strip()} = %s" for col in columns_list])
        query = f"UPDATE StockList SET {set_clause} WHERE stock_id = %s"
        
        cursor.execute(query, (*[val.strip() for val in values_list], stock_id))
        connection.commit()
        cursor.close()
        print("Stock updated successfully.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_all_stocks(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM StockList"
        cursor.execute(query)
        stocks = cursor.fetchall()
        cursor.close()

        if stocks:
            print("\nStock List:")
            for stock in stocks:
                stock_list = list(stock)
                stock_list[2] = stock[2].strftime('%Y-%m-%d')  
                print(tuple(stock_list))
        else:
            print("No stocks available.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Fetch and analyze stock data
def analyze_stock_trends(connection):
    while True:
        print("\nAnalyze Stock Trends:")
        print("1. Line Chart for a Stock")
        print("2. Bar Chart for a Stock")
        print("3. Candlestick Chart")
        print("4. Revenue Growth Analysis")
        print("5. Depth Level Analysis")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            line_chart(connection)
        elif choice == '2':
            bar_chart(connection)
        elif choice == '3':
            candlestick_chart(connection)
        elif choice == '4':
            revenue_growth(connection)
        elif choice == '5':
            depth_level_analysis(connection)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to select a stock
def select_stock(connection):
    cursor = connection.cursor()
    query = "SELECT DISTINCT stock_name FROM StockList"
    cursor.execute(query)
    stock_names = [row[0] for row in cursor.fetchall()]
    cursor.close()

    print("\nAvailable Stocks:")
    for name in stock_names:
        print(name)

    stock_name = input("\nEnter stock name: ").strip().upper()
    if stock_name not in stock_names:
        print("Stock not found!")
        return None
    return stock_name

# Line chart for a single stock
def line_chart(connection):
    stock_name = select_stock(connection)
    if not stock_name:
        return

    try:
        cursor = connection.cursor()
        query = "SELECT date, close_price FROM StockList WHERE stock_name = %s ORDER BY date ASC"
        cursor.execute(query, (stock_name,))
        data = cursor.fetchall()
        cursor.close()

        if not data:
            print("No data available for the selected stock.")
            return

        dates = [row[0] for row in data]
        close_prices = [row[1] for row in data]

        for i in range(1, len(dates)):
            color = 'red' if close_prices[i] < close_prices[i - 1] else 'green'
            plt.plot(dates[i - 1:i + 1], close_prices[i - 1:i + 1], color=color, linewidth=2)

        plt.title(f'{stock_name} Stock Prices (Line Chart)')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

# Bar chart for a single stock
def bar_chart(connection):
    try:
        stock_name = select_stock(connection)
        if not stock_name:
            return

        cursor = connection.cursor()
        query = "SELECT date, open_price, close_price FROM StockList WHERE stock_name = %s ORDER BY date ASC"
        cursor.execute(query, (stock_name,))
        data = cursor.fetchall()
        cursor.close()

        if not data:
            print(f"No data found for {stock_name}.")
            return

        dates = []
        open_prices = []
        close_prices = []

        for row in data:
            try:
                dates.append(row[0])
                open_prices.append(float(row[1]))  # Ensure it's a float
                close_prices.append(float(row[2]))  # Ensure it's a float
            except (ValueError, TypeError):
                print(f"Skipping invalid data: {row}")
                continue

        if not dates:
            print("No valid stock data available for plotting.")
            return

        plt.figure(figsize=(10, 6))
        for i in range(len(dates)):
            color = 'green' if close_prices[i] >= open_prices[i] else 'red'
            plt.plot([dates[i], dates[i]], [open_prices[i], close_prices[i]], color=color, lw=3)

        plt.title(f'{stock_name} Stock Prices (Bar Chart)')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(axis='x')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Candlestick chart for a single stock
def candlestick_chart(connection):
    try:
        stock_name = select_stock(connection)
        if not stock_name:
            return

        cursor = connection.cursor()
        cursor.execute("SELECT date, open_price, high, low, close_price FROM StockList WHERE stock_name = %s ORDER BY date ASC", (stock_name,))
        data = cursor.fetchall()
        cursor.close()

        if not data:
            print(f"No data found for {stock_name}.")
            return

        dates, opens, highs, lows, closes = [], [], [], [], []

        for row in data:
            try:
                dates.append(row[0])
                opens.append(float(row[1]))
                highs.append(float(row[2]))
                lows.append(float(row[3]))
                closes.append(float(row[4]))
            except (ValueError, TypeError):
                print(f"Skipping invalid data: {row}")
                continue

        if not dates:
            print("No valid stock data available for plotting.")
            return

        plt.figure(figsize=(10, 6))
        for i in range(len(dates)):
            color = 'green' if closes[i] >= opens[i] else 'red'
            plt.plot([dates[i], dates[i]], [lows[i], highs[i]], color='black')
            plt.plot([dates[i], dates[i]], [opens[i], closes[i]], color=color, linewidth=5)

        plt.title(f'{stock_name} Candlestick Chart')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Revenue growth analysis    
def revenue_growth(connection):
    try:
        stock_name = select_stock(connection)
        if not stock_name:
            return

        cursor = connection.cursor()
        cursor.execute("SELECT date, close_price FROM StockList WHERE stock_name = %s ORDER BY date ASC", (stock_name,))
        data = cursor.fetchall()
        cursor.close()

        if not data:
            print(f"No data found for {stock_name}.")
            return

        months = []
        growth_values = []

        # Convert dates to months and sum revenue
        for row in data:
            try:
                date_obj = row[0]
                revenue = float(row[1])  # Ensure it's a valid number

                month_key = date_obj.strftime("%Y-%b")  # Format month as YYYY-MMM

                if month_key in months:
                    index = months.index(month_key)
                    growth_values[index] += revenue  # Add revenue to existing month
                else:
                    months.append(month_key)
                    growth_values.append(revenue)  # New month, add revenue
            except (ValueError, TypeError):
                print(f"Skipping invalid data: {row}")
                continue

        growth_values = np.array(growth_values)
        valid_indices = growth_values >= 0  
        months = [months[i] for i in range(len(months)) if valid_indices[i]]
        growth_values = growth_values[valid_indices]

        if len(growth_values) == 0:
            print("Error: No valid revenue growth data to plot.")
            return

        print("\nChoose a chart type:")
        print("1. Line Chart")
        print("2. Bar Chart")
        print("3. Pie Chart")
        chart_choice = input("Enter choice (1/2/3): ").strip()

        plt.figure(figsize=(10, 6))

        if chart_choice == "1":
            plt.plot(months, growth_values, marker='o', linestyle='-', color='blue', label="Growth %")
            plt.xlabel("Month")
            plt.ylabel("Growth (%)")
            plt.title(f'{stock_name} Revenue Growth (Line Chart)')
            
        elif chart_choice == "2":
            plt.bar(months, growth_values, color='purple', label="Growth %")
            plt.xlabel("Month")
            plt.ylabel("Growth (%)")
            plt.title(f'{stock_name} Revenue Growth (Bar Chart)')
            
        elif chart_choice == "3":
            if sum(growth_values) == 0:
                print("Error: Pie chart cannot be plotted with zero values.")
                return
            plt.pie(growth_values, labels=months, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            plt.title("Revenue Growth Distribution")
            
        else:
            print("Invalid choice! Defaulting to Line Chart.")
            plt.plot(months, growth_values, marker='o', linestyle='-', color='blue', label="Growth %")

        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()

    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Depth level analysis
def depth_level_analysis(connection):
    try:
        stock_name = select_stock(connection)
        if not stock_name:
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT date, high, low FROM StockList WHERE stock_name = %s ORDER BY date ASC", (stock_name,))
            data = cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return
        finally:
            cursor.close()

        if not data:
            print(f"No data found for {stock_name}.")
            return

        dates = []
        depth_levels = []

        for row in data:
            try:
                dates.append(row[0])
                depth_levels.append(row[1] - row[2])
            except Exception as e:
                print(f"Skipping invalid data row {row}: {e}")

        if not depth_levels:
            print("Error: No valid depth level data to plot.")
            return

        plt.bar(dates, depth_levels, color='purple')
        plt.title(f'{stock_name} Depth Level Analysis')
        plt.xlabel('Date')
        plt.ylabel('Price Range (High - Low)')
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main function
def main():
    connection = connect_to_database()

    while True:
        print("\nMain Menu:")
        print("1. Admin Login")
        print("2. Analyze Stock Trends")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            if admin_login(connection):
                admin_actions(connection)
        elif choice == '2':
            analyze_stock_trends(connection)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

def main():
    try:
        connection = connect_to_database()
        if not connection:
            print("Error: Could not establish database connection.")
            return
        
        while True:
            print("\nMain Menu:")
            print("1. Admin Login")
            print("2. Analyze Stock Trends")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                try:
                    if admin_login(connection):
                        admin_actions(connection)
                except Exception as e:
                    print(f"Error during admin login: {e}")

            elif choice == '2':
                try:
                    analyze_stock_trends(connection)
                except Exception as e:
                    print(f"Error analyzing stock trends: {e}")

            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("Database connection closed.")

    
if __name__ == "__main__":
    main()
    
