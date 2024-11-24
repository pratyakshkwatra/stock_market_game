# 📈 Stock Market Game

Welcome to the **Stock Market Game**, a Grade 12 Computer Science project by **Pratyaksh Kwatra** and **Aarav Rai**. This project combines finance, technology, and gamification to offer users an engaging way to learn about stocks and the stock market.

## 🌟 Features

1. **Interactive Games**:
   - **Game 1**: Guess the stock based on its price trends and industry.
   - **Game 2**: Predict stock movement based on historical data trends.

2. **User Account Management**:
   - Create accounts with secure password hashing using SHA-256.
   - Update usernames or delete accounts.

3. **Leaderboard**:
   - View the top players based on their total scores.

4. **Score Tracking**:
   - Keep track of your performance across games.

5. **Stock Data**:
   - Fetch real-time stock data using APIs like Yahoo Finance (`yfinance`).
   - Visualize stock trends using `matplotlib`.

6. **Database Integration**:
   - User and game data is stored in a MySQL database for persistent storage.

---

## 🛠️ Technologies Used

- **Python**: Core programming language.
- **MySQL**: Database to store user accounts and game scores.
- **`yfinance`**: Fetch real-time stock market data.
- **`nsepython`**: Access NSE stock data.
- **`matplotlib`**: Visualize stock trends.
- **`inquirer3`**: Interactive CLI menus.
- **Secure Passwords**: SHA-256 hashing for user passwords.

---

## 🚀 Installation and Setup

### Prerequisites
- Python 3.9 or later
- MySQL server installed and running
- `pip` package manager

### Steps to Run the Game
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/stock-market-game.git
   cd stock-market-game
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database:
   - Update your MySQL password in the `keys.py` file.
   - Run the database setup script:
     ```bash
     python stock_market_game.py
     ```

4. Start the game:
   ```bash
   python stock_market_game.py
   ```

---

## 📊 How to Play

1. **Login or Create an Account**:
   - Choose to log in or create a new account.
   - Your progress and scores will be saved for future sessions.

2. **Main Menu Options**:
   - **Play Games**: Choose between Game 1 and Game 2.
   - **Account Settings**: Update your username or delete your account.
   - **Leaderboard**: See how you stack up against other players.
   - **View Score**: Check your total score.

3. **Game Modes**:
   - **Game 1**: Guess the stock based on industry and a chart.
   - **Game 2**: Predict whether the stock price moves up or down after a given time.

---

## 📂 Project Structure

```plaintext
stock-market-game/
├── database_integration.sql  # SQL scripts for database setup
├── stock_market_game.py      # Main Python file
├── requirements.txt          # Dependencies
├── keys.py                   # MySQL credentials (add your password here)
├── README.md                 # Documentation
```

---

## 📈 Data Sources

- **Yahoo Finance**: Provides global stock data.
- **NSE Python**: Retrieves data from the National Stock Exchange (NSE).

---

## 🤝 Contributors

- **Pratyaksh Kwatra**  
- **Aarav Rai**

---

## ⚠️ Disclaimer

This project is for educational purposes only. Stock data and predictions are for demonstration and should not be used for real trading.

---