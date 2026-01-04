<<<<<<< HEAD
# Movie-reservation-system
=======
# Movie Reservation System

A full-stack web application for booking movie tickets with interactive seat selection, user authentication, and email notifications.

## Features

- Browse movies with posters from OMDb API
- View movie details with ratings, descriptions, and showtimes
- Interactive seat selection with real-time availability
- User registration and login with secure password hashing
- Booking confirmation with email notifications
- Cancel bookings with email confirmation
- Dark-themed responsive Bootstrap 5 UI
- SQLite database for data persistence

## Tech Stack

### Backend
- Python 3.11
- Flask (Web Framework)
- Flask-Mail (Email Notifications)
- SQLite (Database)
- Werkzeug (Password Hashing)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Font Awesome Icons

### External APIs
- OMDb API (Movie Data)

## Project Structure

```
MovieReservationSystem/
├── app.py              # Main Flask application
├── init_db.py          # Database initialization script
├── database.db         # SQLite database (auto-generated)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .env.example        # Environment variables template
│
├── templates/          # HTML templates
│   ├── base.html       # Base template with navbar
│   ├── index.html      # Homepage with movie grid
│   ├── movie.html      # Movie details page
│   ├── seats.html      # Seat selection page
│   ├── login.html      # User login
│   ├── signup.html     # User registration
│   ├── confirmation.html # Booking confirmation
│   ├── cancel.html     # Cancel booking
│   └── my_bookings.html # User's bookings
│
└── static/
    ├── css/
    │   └── style.css   # Custom styles
    ├── js/
    │   └── seats.js    # Seat selection logic
    └── images/         # Static images
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy `.env.example` to `.env`):
   ```bash
   cp .env.example .env
   ```
   
4. Configure the following in `.env`:
   - `SESSION_SECRET`: A secure random string
   - `OMDB_API_KEY`: Your OMDb API key (get one at http://www.omdbapi.com/apikey.aspx)
   - Email configuration (optional, for sending confirmations)

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Open http://localhost:5000 in your browser

## API Routes

### Pages (HTML)
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with movie listings |
| `/movie/<id>` | GET | Movie details page |
| `/seats/<movie_id>/<showtime>` | GET | Seat selection page |
| `/login` | GET, POST | User login |
| `/signup` | GET, POST | User registration |
| `/logout` | GET | User logout |
| `/book` | POST | Process booking |
| `/confirmation/<booking_id>` | GET | Booking confirmation |
| `/cancel` | GET, POST | Cancel booking |
| `/my-bookings` | GET | View user's bookings |

### API Endpoints (JSON)
| Route | Method | Description |
|-------|--------|-------------|
| `/api/movies` | GET | Get all movies |
| `/api/movies/search?q=<query>` | GET | Search movies |
| `/api/booked-seats/<movie_id>/<showtime>` | GET | Get booked seats |

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Movies Table
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imdb_id TEXT UNIQUE,
    title TEXT NOT NULL,
    poster_url TEXT,
    release_year TEXT,
    description TEXT,
    genre TEXT,
    rating TEXT,
    showtimes TEXT DEFAULT '10:00 AM,1:00 PM,4:00 PM,7:00 PM,10:00 PM'
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    seats TEXT NOT NULL,
    showtime TEXT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (movie_id) REFERENCES movies (id)
);
```

### Booked Seats Table
```sql
CREATE TABLE booked_seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    showtime TEXT NOT NULL,
    seat TEXT NOT NULL,
    booking_id TEXT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies (id),
    UNIQUE(movie_id, showtime, seat)
);
```

## Email Configuration

To enable email notifications, configure the following in your `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@moviereservation.com
```

**Note:** For Gmail, you'll need to create an App Password if you have 2-factor authentication enabled.

## License

This project is open source and available under the MIT License.
>>>>>>> ed1d46b (Add comprehensive validation and email feedback for movie bookings)
