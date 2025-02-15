# There are two ways to connect to MySQL database using Python:

# 1. Using mysql-connector-python

    # This is the official MySQL library



import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mysql"
    )
    if connection.is_connected():
        print("Connected to MySQL database")

    # Perform any database operations here

except mysql.connector.Error as e:
    print("Error connecting to MySQL database:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL database connection closed")



# 2. Using PyMySQL

    # This is a pure python method 



import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="mysql"
    )
    if connection.open:
        print("Connected to MySQL database")

    # Perform  any database operations here

except pymysql.Error as e:
    print("Error connecting to MySQL database:", e)

finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("MySQL database connection closed")
