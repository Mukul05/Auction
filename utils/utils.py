import sqlite3
def authorize_user(USER_DB, username,password)->bool:

    for record in USER_DB:
        if record['username'] == username.lower() and record['password'] == password :
            return True
    return False


def remove_auction_item_by_id(AUCTION_ITEMS, id):

    for item in AUCTION_ITEMS:
        if item['id'] == int(id):
            AUCTION_ITEMS.remove(item)
            break


def add_item_to_auction_list(AUCTION_ITEMS,item):

    id = len(AUCTION_ITEMS) +1
    item['id'] = id
    AUCTION_ITEMS.append(item)

def find_auction_item(AUCTION_ITEMS,id):
    for idx,item in enumerate(AUCTION_ITEMS):
        if item['id'] == int(id):
            return idx



def create_db():
    conn = sqlite3.connect('auction.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 role TEXT NOT NULL)''')

    # Create Items table
    c.execute('''CREATE TABLE IF NOT EXISTS items (
                 id INTEGER PRIMARY KEY,
                 seller_id INTEGER NOT NULL,
                 name TEXT NOT NULL,
                 description TEXT,
                 image_url TEXT,
                 price REAL NOT NULL,
                 quantity INTEGER NOT NULL,
                 start_time TEXT,
                 end_time TEXT,
                 FOREIGN KEY (seller_id) REFERENCES users (id))''')

    # Optional: Create Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY,
                 buyer_id INTEGER NOT NULL,
                 item_id INTEGER NOT NULL,
                 quantity INTEGER NOT NULL,
                 transaction_time TEXT,
                 FOREIGN KEY (buyer_id) REFERENCES users (id),
                 FOREIGN KEY (item_id) REFERENCES items (id))''')

    conn.commit()
    conn.close()

# Call this function at the start of your app to ensure the database and tables are created.



