CREATE DATABASE IF NOT EXISTS stock_game;

USE stock_game;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    score INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    game_type VARCHAR(10),
    score INT,
    date_played DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);