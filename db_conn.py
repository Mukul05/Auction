
import mysql.connector

conn = mysql.connector.connect(
    host='144.24.144.192',  # MySQL service name in
    port='3306',
    user='root',
    password='root',
    database='bid_system'
)
cursor = conn.cursor()