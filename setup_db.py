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
    """CREATE TABLE IF NOT EXISTS genres(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT NOT NULL unique 
       );""",

    """CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
       );""",

    """CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_year INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        FOREIGN KEY (genre_id) REFERENCES genres(id)
       );""",

    """CREATE TABLE  IF NOT EXISTS reviews(
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
#insering data to the tables
#a placeholder ? is an empty space,safe way to put values without directly writing them in sql commands
#important in preventing sql injection
#commit() save changes permanently
#rollback() unsave
#lastrowid adds id of the new inserted row
def add_genre(conn, genre_name):
    #error handling
    if  not genre_name :
        print("genre cannot be empty")
        return None
    # Check if the genre already exists
    cur = conn.cursor()
    cur.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
    existing = cur.fetchone()

    if existing:
        print(f"Genre '{genre_name}' already exists with id {existing[0]}")
        return existing[0]
    #insert
    sql="INSERT INTO genres(name) VALUES (?)"
    #create cursor
    #execute insert
    cur.execute(sql,(genre_name,))
    #commit
    conn.commit()
    #get id of last inserted row
    return cur.lastrowid


#users
def add_user(conn,first_name,last_name,email ):
    #error handling
    if not first_name or not last_name or not email:
        print("User cannot be empty")
        return
    #check if user exists by email
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=?", (email,))
    existing = cur.fetchone()
    if existing:
        print(f"User with email '{email}' already exists with id {existing[0]}")
        return existing[0]
    #insert
    sql="INSERT INTO users(first_name,last_name,email) VALUES (?,?,?)"
    cur.execute(sql,(first_name,last_name,email))
    conn.commit()
    return cur.lastrowid


def main():
    try:
        with sqlite3.connect('movies.db') as conn:
            cursor = conn.cursor()
            # loop
            for table_sql in movies_tables:
                cursor.execute(table_sql)
            print('Tables created successfully!')
            #adding genres value
            genres_to_add=["Action", "Comedy","Drama",  "Horror","Thriller","Romance","Sci-Fi","Animation","Documentary"]
            for genre_name in genres_to_add:
                genre_id=add_genre(conn, genre_name)
                print(f"added {genre_name} with id {genre_id}")


            #adding users
            users_to_add = [
                ("Serah", "Ndungu", "ndunguserahwambui@gmail.com"),
                ("Daniel", "Githumbi", "danielgithumbi1998@gmail.com")
            ]

            for first_name, last_name, email in users_to_add:
                user_id = add_user(conn, first_name, last_name, email)
                print(f"Added user '{first_name} {last_name}' with ID {user_id}")

    except sqlite3.OperationalError as e:
        print("Error while connecting to SQLite:", e)
# This line ensures that main() runs only when this file is executed directly,
# not when it is imported into another file.
if __name__ == "__main__":
    main()