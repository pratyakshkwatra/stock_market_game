from mysql.connector import connect as mysql_connect, Error as mysql_Error
from yfinance import download as yf_download, ticker as yf_Ticker
from nsepython import nse_eq_symbols
from matplotlib.pyplot import figure as plt_figure, plot as plt_plot, title as plt_title, xlabel as plt_xlabel, ylabel as plt_ylabel, show as plt_show
from random import sample, choice, randint, random
from datetime import datetime, timedelta
from hashlib import sha256

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'stock_game'
}

def get_db_connection():
    return mysql_connect(**db_config)

def create_user(username, password):
    hashed_password = sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print("User created successfully!")
    except mysql_Error as err:
        print(f"Error: {err}")
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
        return None

def update_score(user_id, game_type, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET score = score + %s WHERE id = %s", (score, user_id))
    cursor.execute("INSERT INTO scores (user_id, game_type, score, date_played) VALUES (%s, %s, %s, %s)",
                   (user_id, game_type, score, datetime.now()))
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
        return yf_download(ticker, start=start, end=end)
    return yf_download(ticker, period='max')

def plot_stock_data(stock_data, title):
    plt_figure(figsize=(10, 5))
    plt_plot(stock_data['Close'])
    plt_title(title)
    plt_xlabel('Date')
    plt_ylabel('Close Price')
    plt_show(block=False)

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

    print("Options:")
    for i, stock in enumerate(selected_stocks, 1):
        name, _ = get_stock_info(stock)
        print(f"{i}. {name}")

    guess = int(input("Enter the number of your guess: "))

    if selected_stocks[guess - 1] == correct_stock:
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
    
    if random_start_date == None:
        return None
    
    random_end_date = random_start_date + timedelta(days=duration_years*365)

    three_year_data = stock_data[random_start_date:random_end_date]

    one_year_later_start = random_end_date + timedelta(days=1)
    one_year_later_end = one_year_later_start + timedelta(days=365)
    one_year_data = stock_data[one_year_later_start:one_year_later_end]
    average_price_one_year_later = one_year_data['Close'].mean()

    if random() < 0.8:
        display_title = f"Guess the Stock Movement (Stock: {stock_name}, Industry: {industry})"
    else:
        display_title = f"Guess the Stock Movement (Industry: {industry})"

    plot_stock_data(three_year_data, display_title)

    guess = input("Did the stock go up or down after the 3 year period? (up/down/up a lot/down a lot): ").strip().lower()

    final_price = three_year_data['Close'].iloc[-1]
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
    else:
        print(f"Wrong! The correct answer was {correct_answer}.")
        update_score(user['id'], 'game2', 0)

def main():
    print("1. Create User")
    print("2. Login")
    choice = int(input("Choose an option: "))

    if choice == 1:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        create_user(username, password)
    elif choice == 2:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login_user(username, password)
        if user:
            print("1. Play Game 1")
            print("2. Play Game 2")
            game_choice = int(input("Choose a game: "))
            if game_choice == 1:
                game1(user, global_stocks)
            elif game_choice == 2:
                game2_result = game2(user, nse_entirety)
                
                while game2_result == None:
                    game2_result = game2(user, nse_entirety)
        else:
            print("Login failed.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()