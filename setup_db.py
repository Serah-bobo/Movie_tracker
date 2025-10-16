import sqlite3
#connect db with connect()
#cursor acts as a pen to database to read/write the db
#we use with to close connection automatically
#data types in sqlite is int,text,real(decimals) and blob
#primary key is a unique identifier of a row in a table paired with autoincrement
#not null means a column can't be empty
#check creates a custom rule for a column
#unique prevents duplicates
#foreign key links a column to another table's primary key
#use CREATE_TABLE to create a table
#we've users,movies,genres and reviews tables
#genre(id and name)
#IF NOT EXISTS creates table if it doesn't exist and prevents execution failure

movies_tables = [
    """CREATE TABLE genres(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
       );""",

    """CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
       );""",

    """CREATE TABLE movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_year INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        FOREIGN KEY (genre_id) REFERENCES genres(id)
       );""",

    """CREATE TABLE reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        rating REAL CHECK(rating >= 0 AND rating <= 10),
        comment TEXT,
        date TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
       );"""
]

try:
    with sqlite3.connect('movies.db') as conn:
        cursor = conn.cursor()
        # loop
        for table_sql in movies_tables:
            cursor.execute(table_sql)
        print('Tables created successfully!')
except sqlite3.OperationalError as e:
    print("Error while connecting to SQLite:", e)
