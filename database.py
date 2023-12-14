from datetime import datetime

import mysql.connector
import os
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',  # MySQL service name in docker-compose.yml
            port='3306',
            user='root',
            password='root',
            database='bid_system'
        )
        self.cursor = self.conn.cursor()

    # User Operations
    def create_user(self, name, email_id, password, user_type):
        sql = "INSERT INTO users (name, email_id, password, user_type) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (name, email_id, password, user_type))
        self.conn.commit()

    def read_user(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def read_user_by_email(self, email_id):
        sql = "SELECT * FROM users WHERE email_id = %s"
        self.cursor.execute(sql, (email_id,))
        row = self.cursor.fetchone()
        if row:
            # Convert the tuple to a dictionary
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def update_user(self, user_id, name, email_id, password, user_type):
        sql = "UPDATE users SET name = %s, email_id = %s, password = %s, user_type = %s WHERE user_id = %s"
        self.cursor.execute(sql, (name, email_id, password, user_type, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()



    # Auction Item Operations
    def add_auction_item(self, user_id, item_name, image_url, start_time, end_time, min_bid):
        sql = "INSERT INTO auction_items (user_id, item_name, image_url, start_time, end_time, min_bid) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (user_id, item_name, image_url, start_time, end_time, min_bid))
        self.conn.commit()

    def view_auction_item(self, item_id):
        sql = "SELECT * FROM auction_items WHERE item_id = %s"
        self.cursor.execute(sql, (item_id,))
        return self.cursor.fetchone()

    def update_auction_item(self, item_id, user_id, item_name, image_url, start_time, end_time, min_bid):
        sql = "UPDATE auction_items SET user_id = %s, item_name = %s, image_url = %s, start_time = %s, end_time = %s, min_bid = %s WHERE item_id = %s"
        self.cursor.execute(sql, (user_id, item_name, image_url, start_time, end_time, min_bid, item_id))
        self.conn.commit()

    def delete_auction_item(self, item_id):
        sql = "DELETE FROM auction_items WHERE item_id = %s"
        self.cursor.execute(sql, (item_id,))
        self.conn.commit()

    def fetch_seller_items(self, user_id):
        sql = "SELECT * FROM auction_items WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def get_user_details(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        row = self.cursor.fetchone()
        columns = [col[0] for col in self.cursor.description]
        return dict(zip(columns, row)) if row else None

    def add_auction_item(self, user_id, item_name, image_path, start_time, end_time, min_bid):
        sql = "INSERT INTO auction_items (user_id, item_name, image_url, start_time, end_time, min_bid) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (user_id, item_name, image_path, start_time, end_time, min_bid))
        self.conn.commit()

    # ... similarly implement view_auction_item, update_auction_item, delete_auction_item

    # Bid Operations
    def place_bid(self, user_id, item_id, amount):
        sql = "INSERT INTO bids (user_id, item_id, amount) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (user_id, item_id, amount))
        self.conn.commit()

    def view_bid(self, bid_id):
        sql = "SELECT * FROM bids WHERE bid_id = %s"
        self.cursor.execute(sql, (bid_id,))
        return self.cursor.fetchone()

    def update_bid(self, bid_id, user_id, item_id, amount):
        sql = "UPDATE bids SET user_id = %s, item_id = %s, amount = %s WHERE bid_id = %s"
        self.cursor.execute(sql, (user_id, item_id, amount, bid_id))
        self.conn.commit()

    def delete_bid(self, bid_id):
        sql = "DELETE FROM bids WHERE bid_id = %s"
        self.cursor.execute(sql, (bid_id,))
        self.conn.commit()

    def fetch_bids_for_item(self, item_id):
        sql = """
        SELECT bids.bid_id, bids.user_id, bids.amount, users.email_id
        FROM bids
        JOIN users ON bids.user_id = users.user_id
        WHERE bids.item_id = %s
        """
        self.cursor.execute(sql, (item_id,))
        return self.cursor.fetchall()

    def mark_item_as_sold(self, item_id, buyer_id, sold_price):
        # Update the auction item as sold
        sql = "UPDATE auction_items SET is_sold = TRUE WHERE item_id = %s"
        self.cursor.execute(sql, (item_id,))

        # Add an entry to the sold_items table
        sold_time = datetime.now()  # Assuming you import datetime
        sql = "INSERT INTO sold_items (item_id, buyer_id, sold_price, sold_time) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (item_id, buyer_id, sold_price, sold_time))
        self.conn.commit()

    def fetch_item_details(self, item_id):
        sql = "SELECT * FROM auction_items WHERE item_id = %s"
        self.cursor.execute(sql, (item_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def get_highest_bid_for_item(self, item_id):
        sql = "SELECT user_id, MAX(amount) AS sold_price FROM bids WHERE item_id = %s GROUP BY user_id ORDER BY sold_price DESC LIMIT 1"
        self.cursor.execute(sql, (item_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
