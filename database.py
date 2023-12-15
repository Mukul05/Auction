from datetime import datetime

import mysql.connector
import os
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',  # MySQL service name in
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
        # Delete all bids associated with the item
        delete_bids_sql = "DELETE FROM bids WHERE item_id = %s"
        self.cursor.execute(delete_bids_sql, (item_id,))

        # Delete the record from sold_items if it exists
        delete_sold_sql = "DELETE FROM sold_items WHERE item_id = %s"
        self.cursor.execute(delete_sold_sql, (item_id,))

        # Finally, delete the item from auction_items
        delete_item_sql = "DELETE FROM auction_items WHERE item_id = %s"
        self.cursor.execute(delete_item_sql, (item_id,))
        self.conn.commit()

    def fetch_seller_items(self, user_id):
        sql = "SELECT * FROM auction_items WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def fetch_all_items_with_sellers(self):
        sql = """
        SELECT auction_items.*, users.name AS seller_name
        FROM auction_items
        JOIN users ON auction_items.user_id = users.user_id
        """
        self.cursor.execute(sql)
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
        SELECT bids.bid_id, bids.amount, users.name as bidder_name, users.email_id
        FROM bids
        JOIN users ON bids.user_id = users.user_id
        WHERE bids.item_id = %s
        ORDER BY bids.amount DESC
        """
        self.cursor.execute(sql, (item_id,))
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]


    def fetch_item_details(self, item_id):
        sql = "SELECT * FROM auction_items WHERE item_id = %s"
        self.cursor.execute(sql, (item_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def fetch_bids_for_seller(self, item_id):
        sql = """
        SELECT bids.amount, users.name AS bidder_name
        FROM bids
        JOIN users ON bids.user_id = users.user_id
        WHERE bids.item_id = %s
        ORDER BY bids.amount DESC
        """
        self.cursor.execute(sql, (item_id,))
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    def fetch_highest_bid_for_item(self, item_id):
        sql = "SELECT user_id, MAX(amount) as sold_price FROM bids WHERE item_id = %s GROUP BY user_id ORDER BY sold_price DESC LIMIT 1"
        self.cursor.execute(sql, (item_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def delete_auction_item(self, item_id):
        delete_bids_sql = "DELETE FROM bids WHERE item_id = %s"
        self.cursor.execute(delete_bids_sql, (item_id,))
        delete_sold_sql = "DELETE FROM sold_items WHERE item_id = %s"
        self.cursor.execute(delete_sold_sql, (item_id,))

        # Then, delete the item
        delete_item_sql = "DELETE FROM auction_items WHERE item_id = %s"
        self.cursor.execute(delete_item_sql, (item_id,))
        self.conn.commit()

    def fetch_available_auction_items(self):
        sql = """
        SELECT auction_items.*, users.name as seller_name 
        FROM auction_items 
        JOIN users ON auction_items.user_id = users.user_id 
        WHERE auction_items.is_sold = FALSE AND auction_items.end_time > NOW()
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def submit_bid(self, item_id, user_id, bid_amount):
        sql = "INSERT INTO bids (user_id, item_id, amount) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (user_id, item_id, bid_amount))
        self.conn.commit()



    def fetch_emails_for_notification(self, item_id):
        # Fetch the seller's and all bidders' email addresses for the item
        sql = """
        SELECT DISTINCT u.email_id FROM users u
        JOIN bids b ON u.user_id = b.user_id OR u.user_id = (SELECT user_id FROM auction_items WHERE item_id = %s)
        WHERE b.item_id = %s
        """
        self.cursor.execute(sql, (item_id, item_id))
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_sold_item_details(self, item_id):
        sql = """
        SELECT ai.item_name, si.sold_price, u.email_id AS buyer_email, si.sold_time
        FROM auction_items ai
        JOIN sold_items si ON ai.item_id = si.item_id
        JOIN users u ON si.buyer_id = u.user_id
        WHERE ai.item_id = %s AND ai.is_sold = TRUE
        """
        self.cursor.execute(sql, (item_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def mark_item_as_sold(self, item_id, buyer_id, sold_price):
        # Update auction item as sold
        update_sql = "UPDATE auction_items SET is_sold = TRUE WHERE item_id = %s"
        self.cursor.execute(update_sql, (item_id,))

        # Insert into sold_items table
        insert_sql = """
        INSERT INTO sold_items (item_id, buyer_id, sold_price, sold_time)
        VALUES (%s, %s, %s, NOW())
        """
        self.cursor.execute(insert_sql, (item_id, buyer_id, sold_price))
        self.conn.commit()
    def get_item_name(self, item_id):
        query = "SELECT item_name FROM auction_items WHERE item_id = %s"
        self.cursor.execute(query, (item_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None



    def close(self):
        self.conn.close()
