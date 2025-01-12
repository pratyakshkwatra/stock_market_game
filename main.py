import os
import subprocess
import sys

def check_requirements():
    if not os.path.isfile("requirements.txt"):
        print("Error: requirements.txt not found. Exiting program.")
        sys.exit(1)

    with open("requirements.txt") as f:
        packages = f.read().splitlines()

    for package in packages:
        try:
            __import__(package.split('==')[0])
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("All requirements are satisfied.")
    
check_requirements()

from mysql.connector import connect as mysql_connect, Error as mysql_Error
from yfinance import download as yf_download, Ticker as yf_Ticker
from nsepython import nse_eq_symbols
from matplotlib.pyplot import figure as plt_figure, plot as plt_plot, title as plt_title, xlabel as plt_xlabel, ylabel as plt_ylabel, show as plt_show
from random import sample, choice, randint, random
from datetime import datetime, timedelta
from hashlib import sha256
import keys
import inquirer3

db_config = {
    'user': 'root',
    'password': keys.password,
    'host': 'localhost',
    'database': 'stock_game'
}

def get_db_connection():
    try:
        conn = mysql_connect(**db_config)
        return conn
    except mysql_Error as err:
        print(f"Error: {err}")
        return None

def setup_database():
    conn = mysql_connect(user='root', password=db_config['password'], host='localhost')
    if conn:
        cursor = conn.cursor()
        
        try:
            with open("database_integration.sql", "r") as file:
                sql_code_lines = [line.replace("\n", "") + ";" if line else None for line in file.read().split(";")]
                
                for statement in sql_code_lines:
                    if statement:
                        cursor.execute(statement)
                        conn.commit()
        except Exception as e:
            print("Error: Missing some files")
            print(e)
            quit()
        
        cursor.close()
        conn.close()

def login_menu():
    global user
    questions = [
        inquirer3.List(
            'auth_choice',
            message="What would you like to proceed with?",
            choices=['Create User', 'Login'],
        ),
    ]
    choice = inquirer3.prompt(questions)["auth_choice"]
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if choice == "Create User":
        user = create_user(username, password)
        if user:
            main_menu()
    elif choice == "Login":
        user = login_user(username, password)
        if user:
            main_menu()
        else:
            print("Login failed.")
    else:
        print("Invalid choice.")

def create_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.execute("SELECT id, score FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        print("User created successfully!")
        return {'id': user[0], 'score': user[1]}
    except mysql_Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, score FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid credentials")
        login_menu()
        return None

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM scores WHERE user_id = {user_id}")
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    cursor.close()
    conn.close()
    print("Account deleted successfully!")
    login_menu()

def update_username(user_id, new_username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_username, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Username changed successfully!")

def update_score(user_id, game_type, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET score = score + %s WHERE id = %s", (score, user_id))
    cursor.execute("INSERT INTO scores (user_id, game_type, score, date_played) VALUES (%s, %s, %s, %s)",
                   (user_id, game_type, score, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

def view_leaderboard():
    global user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM users where score != 0 order by score desc")
    result = cursor.fetchall()
    for players in result:
        print(f"Player: {players[0]}, Total Score: {players[1]}")
    conn.commit()
    cursor.close()
    conn.close()

def view_score():
    global user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT score FROM users WHERE id = {user['id']}")
    result = cursor.fetchone()
    total_score = result[0] if result[0] is not None else 0
    print("Total Score:", total_score)
    conn.commit()
    cursor.close()
    conn.close()    

    
global_stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
    'TSLA', 'BRK-B', 'NVDA', 'JPM', 'JNJ',
    'V', 'WMT', 'PG', 'DIS', 'MA',
    'UNH', 'HD', 'VZ', 'PYPL', 'ADBE'
]
nse_small = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'KOTAKBANK.NS', 'SBIN.NS', 'HDFC.NS', 'BHARTIARTL.NS', 'ITC.NS',
    'LT.NS', 'HCLTECH.NS', 'AXISBANK.NS', 'MARUTI.NS', 'ASIANPAINT.NS',
    'ULTRACEMCO.NS', 'M&M.NS', 'SUNPHARMA.NS', 'BAJFINANCE.NS', 'TITAN.NS'
]
nse_entirety = nse_eq_symbols()

def fetch_stock_data(ticker, start=None, end=None):
    if start and end:
        return yf_download(ticker, start=start, end=end, progress=False)
    return yf_download(ticker, period='max', progress=False)

def plot_stock_data(stock_data, title):
    plt_figure(figsize=(10, 5))
    plt_plot(stock_data['Close'])
    plt_title(title)
    plt_xlabel('Date')
    plt_ylabel('Close Price')
    plt_show(block=True)

def get_stock_info(ticker):
    stock_info = yf_Ticker(ticker).info
    name = stock_info.get('shortName', ticker)
    industry = stock_info.get('industry', 'Unknown')
    return name, industry

def game1(user, stock_list):
    select_stocks = sample(stock_list, 4) 
    select_stocks_nse = [stc + '.NS' for stc in select_stocks]
    if stock_list == nse_entirety:
        selected_stocks = select_stocks_nse
    else:
        selected_stocks = select_stocks
    correct_stock = choice(selected_stocks)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    stock_data = fetch_stock_data(correct_stock, start=start_date, end=end_date)
    
    _, industry = get_stock_info(correct_stock)
    
    plot_stock_data(stock_data, f"Guess the Stock (Industry: {industry})")
    
    import time
    time.sleep(2)
    questions = [
        inquirer3.List(
            'game_stock_choice',
            message="Guess a stock: ",
            choices=[get_stock_info(stock)[0] for stock in selected_stocks],
        ),
    ]
    guess = inquirer3.prompt(questions)["game_stock_choice"]

    if guess == correct_stock:
        print("Correct!")
        update_score(user['id'], 'game1', 10)
    else:
        correct_name, _ = get_stock_info(correct_stock)
        print(f"Wrong! The correct answer was {correct_name}.")
        update_score(user['id'], 'game1', 0)

def game2(user, stock_list):
    select_stocks = sample(stock_list, 4)
    select_stocks_nse = [stc + '.NS' for stc in select_stocks]
    if stock_list == nse_entirety:
        selected_stocks = select_stocks_nse
    else:
        selected_stocks = select_stocks
    correct_stock = choice(selected_stocks)
    stock_data = fetch_stock_data(correct_stock)

    stock_name, industry = get_stock_info(correct_stock)

    start_date = stock_data.index[0]
    end_date = stock_data.index[-1]
    duration_years = 3

    def get_random_start_date(first_date, last_date, duration_years):
        max_start_date = last_date - timedelta(days=duration_years*365)
        
        try:
            random_start_date = first_date + timedelta(
                days=randint(0, (max_start_date - first_date).days)
            )
        except:
            return None
        
        return random_start_date

    random_start_date = get_random_start_date(start_date, end_date, duration_years)
    
    if random_start_date is None:
        return
    
    random_end_date = random_start_date + timedelta(days=duration_years*365)

    three_year_data = stock_data[random_start_date:random_end_date]

    one_year_later_start = random_end_date + timedelta(days=1)
    one_year_later_end = one_year_later_start + timedelta(days=365)
    one_year_data = stock_data[one_year_later_start:one_year_later_end]
    average_price_one_year_later = one_year_data['Close'].mean().item()

    if random() < 0.8:
        display_title = f"Guess the Stock Movement (Stock: {stock_name}, Industry: {industry})"
    else:
        bonus = True
        print("Bonus Question! Guess without the stock name for extra points!")
        display_title = f"Guess the Stock Movement (Industry: {industry})"

    plot_stock_data(three_year_data, display_title)

    questions = [
        inquirer3.List(
            'choice',
            message="Did the stock go up or down after the 3 year period?",
            choices=['up a lot', 'up', 'down', 'down a lot'],
        ),
    ]
    guess = inquirer3.prompt(questions)

    final_price = three_year_data['Close'].iloc[-1].item()
    
    if average_price_one_year_later > final_price:
        correct_answer = "up"
    else:
        correct_answer = "down"

    if average_price_one_year_later > final_price * 1.3:
        correct_answer = "up a lot"
    elif average_price_one_year_later < final_price * 0.7:
        correct_answer = "down a lot"

    if guess == correct_answer:
        print("Correct!")
        update_score(user['id'], 'game2', 10)
        if 'bonus' in locals() and bonus == True:
            print("Extra 5 points for answering bonus question!")
            update_score(user['id'], 'game2', 5)
    else:
        print(f"Wrong! The correct answer was {correct_answer}.")
        update_score(user['id'], 'game2', 0)

def main():
    setup_database()
    login_menu()
    while True:
        main_menu()

def main_menu():
    questions = [
        inquirer3.List(
            'main_menu_choice',
            message="What would you like to proceed with?",
            choices=['Play', 'Account Settings', "View Leaderboard", "View Score", "Quit"],
        ),
    ]
    choice = inquirer3.prompt(questions)["main_menu_choice"]
    
    if choice == "Play":
        game_menu()
    elif choice == "Account Settings":
        account_menu()
    elif choice == "View Leaderboard":
        view_leaderboard()
    elif choice == "View Score":
        view_score()
    elif choice == "Quit":
        quit()
    else:
        print("Invalid Choice")
        main_menu()

def account_menu():
    global user
    questions = [
        inquirer3.List(
            'account_menu_choice',
            message="What would you like to proceed with?",
            choices=['Delete Account', 'Update Username', "Main Menu", "Quit"],
        ),
    ]
    menu_choice = inquirer3.prompt(questions)["account_menu_choice"]
    if menu_choice == "Delete Account":
        delete_user(user['id'])
    elif menu_choice == "Update Username":
        new_username = input("Enter new username:")
        update_username(user['id'], new_username)
    elif menu_choice == "Main Menu":
        return
    elif menu_choice == "Quit":
        quit()
    else:
        print("Invalid Choice")
        return

def game_menu():
    global user
    
    questions = [
        inquirer3.List(
            'game_menu_choice',
            message="What would you like to proceed with?",
            choices=['Game 1', 'Game 2', "Main Menu", "Quit"],
        ),
    ]
    game_choice = inquirer3.prompt(questions)["game_menu_choice"]
    
    if game_choice == "Game 1":
        while True:
            game1(user, global_stocks)
    elif game_choice == "Game 2":
        while True:
            game2(user, nse_entirety)
    elif game_choice == "Main Menu":
        return
    elif game_choice == "Quit":
        quit()
    else:
        print("Invalid Choice")
        return

if __name__ == "__main__":
    main()
