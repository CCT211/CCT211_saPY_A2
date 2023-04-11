import sqlite3

# create a connection to the database
conn = sqlite3.connect('user_date_saPY.db')

# create a cursor object to execute SQL queries
cur = conn.cursor()

# create the usernames table
cur.execute('''CREATE TABLE usernames
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE)''')

# create the passwords table
cur.execute('''CREATE TABLE passwords
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT)''')

# create the reviews table
cur.execute('''CREATE TABLE reviews
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                review TEXT)''')

# create the friends_list table
cur.execute('''CREATE TABLE friends_list
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                friend TEXT,
                FOREIGN KEY (username) REFERENCES usernames(username))''')

# commit the changes to the database
conn.commit()

# close the connection to the database
conn.close()
