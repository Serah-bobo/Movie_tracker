import sqlite3
from datetime import datetime

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
#a placeholder ? is an empty space,safe way to put values without directly writing them in SQL commands
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
    cur.execute("SELECT id FROM genres WHERE genre_name = ?", (genre_name,))
    existing = cur.fetchone()

    if existing:
        print(f"Genre '{genre_name}' already exists with id {existing[0]}")
        return existing[0]
    #insert
    sql="INSERT INTO genres(genre_name) VALUES (?)"
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

#movies
def add_movies(conn, title, release_year, genre_id):
    # Error handling
    if not title or not release_year or not genre_id:
        print("Movie cannot be empty")
        return None

    cur = conn.cursor()

    # Check if genre exists
    cur.execute("SELECT id FROM genres WHERE id=?", (genre_id,))
    genre = cur.fetchone()
    if not genre:
        print(f"Genre with ID {genre_id} does not exist. Add the genre first.")
        return None  # stop here

    # Check if movies already exists
    cur.execute("SELECT id FROM movies WHERE title=? AND release_year=?",
                (title, release_year))
    existing = cur.fetchone()
    if existing:
        print(f"Movie '{title}' already exists with ID {existing[0]}")
        return existing[0]

    # Insert movie
    cur.execute("INSERT INTO movies(title, release_year, genre_id) VALUES (?, ?, ?)",
                (title, release_year, genre_id))
    conn.commit()
    return cur.lastrowid

#add reviews

def add_review(conn, movie_title, user_email, rating, comment):
    # Error handling
    if not movie_title or not user_email or rating is None:
        print("Review fields cannot be empty")
        return

    cur = conn.cursor()

    # Validate rating
    if rating < 0 or rating > 10:
        print("Rating must be between 0 and 10")
        return

    # Find movie_id by title
    cur.execute("SELECT id FROM movies WHERE title = ?", (movie_title,))
    movie = cur.fetchone()
    if not movie:
        print(f"Movie '{movie_title}' not found.")
        return
    movie_id = movie[0]

    # Find user_id by email
    cur.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user = cur.fetchone()
    if not user:
        print(f"User with email '{user_email}' not found.")
        return
    user_id = user[0]

    # Current date
    review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert review
    sql = """INSERT INTO reviews (movie_id, user_id, rating, comment, date)
                 VALUES (?, ?, ?, ?, ?)"""
    cur.execute(sql, (movie_id, user_id, rating, comment, review_date))
    conn.commit()

    print(f"✅ Review added for '{movie_title}' by {user_email} on {review_date}")
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


            #adding movies
            movies_to_add = [
                ("Inception", 2010, "Action"),
                ("The Dark Knight", 2008, "Action"),
                ("Forrest Gump", 1994, "Drama"),
                ("The Hangover", 2009, "Comedy"),
                ("Get Out", 2017, "Horror"),
                ("Titanic", 1997, "Romance"),
                ("Interstellar", 2014, "Sci-Fi"),
                ("Toy Story", 1995, "Animation"),
                ("The Social Dilemma", 2020, "Documentary"),
                ("Se7en", 1995, "Thriller")
            ]
            for title, release_year, genre_name in movies_to_add:
                cursor.execute("SELECT id FROM genres WHERE genre_name=?", (genre_name,))
                genre_row=cursor.fetchone()
                if not genre_row:
                    print(f"Genre '{genre_name}' not found. Add it first!")
                    continue  # skip this movie

                genre_id = genre_row[0]  # now we have the actual genre ID

                movie_id = add_movies(conn, title, release_year, genre_id)
                if movie_id:
                    print(f"Added movie '{title}' ({release_year}) with genre '{genre_name}' and ID {movie_id}")

            # Add some reviews
            reviews_to_add = [
                ("Inception", "ndunguserahwambui@gmail.com", 9.5, "Mind-blowing sci-fi!"),
                ("Titanic", "danielgithumbi1998@gmail.com", 8.8, "Emotional and timeless."),
                ("The Dark Knight", "ndunguserahwambui@gmail.com", 9.7, "Best superhero movie ever!")
            ]

            for movie_title, user_email, rating, comment in reviews_to_add:
                add_review(conn, movie_title, user_email, rating, comment)


    except sqlite3.OperationalError as e:
        print("Error while connecting to SQLite:", e)
# This line ensures that main() runs only when this file is executed directly.
# not when it is imported into another file.
if __name__ == "__main__":
    main()

#join putting rows of multiple tables together
#inner join returns rows that exist in both tables