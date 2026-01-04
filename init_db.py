"""
Database Initialization Script for Movie Reservation System
Creates SQLite database with Users, Movies, and Bookings tables
Also fetches initial movie data from OMDb API
"""

import sqlite3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DATABASE = 'database.db'
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'demo')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create all required database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imdb_id TEXT UNIQUE,
            title TEXT NOT NULL,
            poster_url TEXT,
            release_year TEXT,
            description TEXT,
            genre TEXT,
            rating TEXT,
            showtimes TEXT DEFAULT '10:00 AM,1:00 PM,4:00 PM,7:00 PM,10:00 PM'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            seats TEXT NOT NULL,
            showtime TEXT NOT NULL,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (movie_id) REFERENCES movies (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booked_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            showtime TEXT NOT NULL,
            seat TEXT NOT NULL,
            booking_id TEXT NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            UNIQUE(movie_id, showtime, seat)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

def fetch_movies_from_omdb():
    """Fetch movies from OMDb API and save to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_terms = ['batman', 'avengers', 'spider', 'star wars', 'matrix', 'inception']
    
    for term in search_terms:
        try:
            url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={term}&type=movie"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('Response') == 'True' and 'Search' in data:
                for movie in data['Search'][:3]:
                    detail_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={movie['imdbID']}&plot=short"
                    detail_response = requests.get(detail_url, timeout=10)
                    detail_data = detail_response.json()
                    
                    if detail_data.get('Response') == 'True':
                        try:
                            cursor.execute('''
                                INSERT OR IGNORE INTO movies (imdb_id, title, poster_url, release_year, description, genre, rating)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                detail_data.get('imdbID'),
                                detail_data.get('Title'),
                                detail_data.get('Poster') if detail_data.get('Poster') != 'N/A' else '/static/images/no-poster.png',
                                detail_data.get('Year'),
                                detail_data.get('Plot') if detail_data.get('Plot') != 'N/A' else 'No description available.',
                                detail_data.get('Genre') if detail_data.get('Genre') != 'N/A' else 'Unknown',
                                detail_data.get('imdbRating') if detail_data.get('imdbRating') != 'N/A' else 'N/A'
                            ))
                            print(f"Added: {detail_data.get('Title')}")
                        except sqlite3.IntegrityError:
                            pass
        except Exception as e:
            print(f"Error fetching movies for '{term}': {e}")
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("No movies fetched from API. Adding sample movies...")
        sample_movies = [
            ('tt0468569', 'The Dark Knight', 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg', '2008', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'Action, Crime, Drama', '9.0'),
            ('tt0848228', 'The Avengers', 'https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg', '2012', 'Earth\'s mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.', 'Action, Sci-Fi', '8.0'),
            ('tt0816692', 'Interstellar', 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg', '2014', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', 'Adventure, Drama, Sci-Fi', '8.7'),
            ('tt0133093', 'The Matrix', 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg', '1999', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 'Action, Sci-Fi', '8.7'),
            ('tt1375666', 'Inception', 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg', '2010', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Action, Adventure, Sci-Fi', '8.8'),
            ('tt0076759', 'Star Wars: Episode IV - A New Hope', 'https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_SX300.jpg', '1977', 'Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire\'s world-destroying battle station.', 'Action, Adventure, Fantasy', '8.6'),
        ]
        
        for movie in sample_movies:
            cursor.execute('''
                INSERT OR IGNORE INTO movies (imdb_id, title, poster_url, release_year, description, genre, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', movie)
        
        conn.commit()
        print("Sample movies added successfully!")
    
    conn.close()
    print(f"Total movies in database: {count if count > 0 else len(sample_movies)}")

if __name__ == '__main__':
    print("Initializing Movie Reservation System Database...")
    create_tables()
    fetch_movies_from_omdb()
    print("Database initialization complete!")
