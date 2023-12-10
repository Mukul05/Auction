
import sqlite3
from datetime import datetime

# Database setup and initialization
def init_db():
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AuctionItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            userid INTEGER NOT NULL,
            start_bid REAL NOT NULL,
            start_bid_time TEXT NOT NULL,
            end_bid_time TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_item_id INTEGER NOT NULL,
            userid INTEGER NOT NULL,
            amount REAL NOT NULL,
            username TEXT NOT NULL,
            user_email TEXT NOT NULL,
            FOREIGN KEY (auction_item_id) REFERENCES AuctionItems (id)
        )
    ''')
    conn.commit()
    conn.close()

def add_auction_item(item, userid, start_bid, start_bid_time, end_bid_time):
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO AuctionItems (item, userid, start_bid, start_bid_time, end_bid_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (item, userid, start_bid, start_bid_time, end_bid_time))
    conn.commit()
    conn.close()

def place_bid(auction_item_id, userid, amount, username, user_email):
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Bids (auction_item_id, userid, amount, username, user_email)
        VALUES (?, ?, ?, ?, ?)
    ''', (auction_item_id, userid, amount, username, user_email))
    conn.commit()
    conn.close()

def update_auction_item(item_id, **kwargs):
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    updates = ', '.join([f"{key} = ?" for key in kwargs])
    values = list(kwargs.values()) + [item_id]
    cursor.execute(f'''
        UPDATE AuctionItems
        SET {updates}
        WHERE id = ?
    ''', values)
    conn.commit()
    conn.close()

def delete_auction_item(item_id):
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM AuctionItems WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def view_auction_items():
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AuctionItems')
    items = cursor.fetchall()
    conn.close()
    return items

def view_bids(auction_item_id):
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bids WHERE auction_item_id = ?', (auction_item_id,))
    bids = cursor.fetchall()
    conn.close()
    return bids

init_db()

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);")
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
