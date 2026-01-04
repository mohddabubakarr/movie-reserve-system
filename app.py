"""
Movie Reservation System - Main Flask Application
Full-stack web application for movie ticket booking
"""

import os
import re
import sqlite3
import uuid
from functools import wraps
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

VALID_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
VALID_COLS = list(range(1, 11))
SEAT_PATTERN = re.compile(r'^[A-H]([1-9]|10)$')

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@moviereservation.com')

mail = Mail(app)

DATABASE = 'database.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def validate_seat(seat):
    """Validate seat format (e.g., A1, B10, H5)"""
    return bool(SEAT_PATTERN.match(seat.upper()))

def validate_showtime(showtime, movie_showtimes):
    """Validate that showtime exists for the movie"""
    valid_times = [s.strip() for s in movie_showtimes.split(',')]
    return showtime.strip() in valid_times

def send_booking_email(user_email, user_name, booking_details, is_cancellation=False):
    """Send booking confirmation or cancellation email"""
    try:
        if not app.config['MAIL_USERNAME']:
            print("Email not configured. Skipping email send.")
            return False
        
        if is_cancellation:
            subject = f"Booking Cancelled - {booking_details['movie_title']}"
            template = f"""
Dear {user_name},

Your booking has been successfully cancelled.

Booking Details:
- Booking ID: {booking_details['booking_id']}
- Movie: {booking_details['movie_title']}
- Showtime: {booking_details['showtime']}
- Seats: {booking_details['seats']}

If you did not request this cancellation, please contact us immediately.

Thank you for using Movie Reservation System!

Best regards,
Movie Reservation Team
            """
        else:
            subject = f"Booking Confirmed - {booking_details['movie_title']}"
            template = f"""
Dear {user_name},

Your booking has been confirmed!

Booking Details:
- Booking ID: {booking_details['booking_id']}
- Movie: {booking_details['movie_title']}
- Showtime: {booking_details['showtime']}
- Seats: {booking_details['seats']}
- Booking Date: {booking_details['booking_date']}

Please arrive at least 15 minutes before the showtime.

Thank you for choosing Movie Reservation System!

Best regards,
Movie Reservation Team
            """
        
        msg = Message(subject, recipients=[user_email])
        msg.body = template
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def index():
    """Homepage - Display all movies"""
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY title').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/api/movies')
def api_movies():
    """API endpoint to get all movies"""
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies ORDER BY title').fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

@app.route('/api/movies/search')
def api_search_movies():
    """API endpoint to search movies"""
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    movies = conn.execute(
        'SELECT * FROM movies WHERE LOWER(title) LIKE ? OR LOWER(genre) LIKE ?',
        (f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    """Movie details page"""
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('index'))
    
    showtimes = movie['showtimes'].split(',') if movie['showtimes'] else []
    return render_template('movie.html', movie=movie, showtimes=showtimes)

@app.route('/seats/<int:movie_id>/<showtime>')
def seat_selection(movie_id, showtime):
    """Seat selection page"""
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('index'))
    
    booked_seats = conn.execute(
        'SELECT seat FROM booked_seats WHERE movie_id = ? AND showtime = ?',
        (movie_id, showtime)
    ).fetchall()
    conn.close()
    
    booked_seat_list = [seat['seat'] for seat in booked_seats]
    
    return render_template('seats.html', movie=movie, showtime=showtime, booked_seats=booked_seat_list)

@app.route('/api/booked-seats/<int:movie_id>/<showtime>')
def api_booked_seats(movie_id, showtime):
    """API endpoint to get booked seats for a movie and showtime"""
    conn = get_db_connection()
    booked_seats = conn.execute(
        'SELECT seat FROM booked_seats WHERE movie_id = ? AND showtime = ?',
        (movie_id, showtime)
    ).fetchall()
    conn.close()
    return jsonify([seat['seat'] for seat in booked_seats])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['user_email'] = user['email']
            flash('Login successful!', 'success')
            
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not all([first_name, last_name, email, password, confirm_password]):
            flash('Please fill in all fields.', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('signup.html')
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            conn.close()
            flash('Email already registered. Please login.', 'error')
            return render_template('signup.html')
        
        password_hash = generate_password_hash(password)
        
        try:
            conn.execute(
                'INSERT INTO users (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)',
                (first_name, last_name, email, password_hash)
            )
            conn.commit()
            
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            conn.close()
            
            session['user_id'] = user['id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            session['user_email'] = user['email']
            
            flash('Account created successfully!', 'success')
            
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))
        except Exception as e:
            conn.close()
            flash('An error occurred. Please try again.', 'error')
            print(f"Signup error: {e}")
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/book', methods=['POST'])
@login_required
def book_tickets():
    """Process ticket booking"""
    movie_id = request.form.get('movie_id')
    showtime = request.form.get('showtime')
    seats = request.form.get('seats', '')
    
    if not all([movie_id, showtime, seats]):
        flash('Please select seats before booking.', 'error')
        return redirect(url_for('index'))
    
    seat_list = [s.strip().upper() for s in seats.split(',') if s.strip()]
    
    if not seat_list:
        flash('Please select at least one seat.', 'error')
        return redirect(url_for('seat_selection', movie_id=movie_id, showtime=showtime))
    
    for seat in seat_list:
        if not validate_seat(seat):
            flash(f'Invalid seat format: {seat}. Seats must be A1-H10.', 'error')
            return redirect(url_for('seat_selection', movie_id=movie_id, showtime=showtime))
    
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    
    if not movie:
        conn.close()
        flash('Movie not found.', 'error')
        return redirect(url_for('index'))
    
    if not validate_showtime(showtime, movie['showtimes'] or ''):
        conn.close()
        flash('Invalid showtime selected.', 'error')
        return redirect(url_for('movie_details', movie_id=movie_id))
    
    existing_seats = conn.execute(
        'SELECT seat FROM booked_seats WHERE movie_id = ? AND showtime = ? AND seat IN ({})'.format(
            ','.join('?' * len(seat_list))
        ),
        [movie_id, showtime] + seat_list
    ).fetchall()
    
    if existing_seats:
        conn.close()
        flash('Some selected seats are already booked. Please try again.', 'error')
        return redirect(url_for('seat_selection', movie_id=movie_id, showtime=showtime))
    
    booking_id = f"BK{uuid.uuid4().hex[:8].upper()}"
    
    try:
        conn.execute(
            'INSERT INTO bookings (booking_id, user_id, movie_id, seats, showtime) VALUES (?, ?, ?, ?, ?)',
            (booking_id, session['user_id'], movie_id, seats, showtime)
        )
        
        for seat in seat_list:
            conn.execute(
                'INSERT INTO booked_seats (movie_id, showtime, seat, booking_id) VALUES (?, ?, ?, ?)',
                (movie_id, showtime, seat, booking_id)
            )
        
        conn.commit()
        
        booking_details = {
            'booking_id': booking_id,
            'movie_title': movie['title'],
            'showtime': showtime,
            'seats': seats,
            'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        email_sent = send_booking_email(
            session['user_email'],
            session['user_name'],
            booking_details,
            is_cancellation=False
        )
        
        conn.close()
        
        if not email_sent:
            flash('Booking confirmed! Note: Confirmation email could not be sent.', 'warning')
        
        return redirect(url_for('confirmation', booking_id=booking_id))
    
    except Exception as e:
        conn.rollback()
        conn.close()
        flash('An error occurred while booking. Please try again.', 'error')
        print(f"Booking error: {e}")
        return redirect(url_for('seat_selection', movie_id=movie_id, showtime=showtime))

@app.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    """Booking confirmation page"""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, m.title, m.poster_url, m.release_year, u.first_name, u.last_name, u.email
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
        JOIN users u ON b.user_id = u.id
        WHERE b.booking_id = ?
    ''', (booking_id,)).fetchone()
    conn.close()
    
    if not booking:
        flash('Booking not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('confirmation.html', booking=booking)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel_booking():
    """Cancel booking page"""
    if request.method == 'POST':
        booking_id = request.form.get('booking_id', '').strip().upper()
        email = request.form.get('email', '').strip()
        
        if not booking_id or not email:
            flash('Please fill in all fields.', 'error')
            return render_template('cancel.html')
        
        conn = get_db_connection()
        booking = conn.execute('''
            SELECT b.*, m.title, u.first_name, u.last_name, u.email
            FROM bookings b
            JOIN movies m ON b.movie_id = m.id
            JOIN users u ON b.user_id = u.id
            WHERE b.booking_id = ? AND u.email = ?
        ''', (booking_id, email)).fetchone()
        
        if not booking:
            conn.close()
            flash('Booking not found. Please check your booking ID and email.', 'error')
            return render_template('cancel.html')
        
        try:
            conn.execute('DELETE FROM booked_seats WHERE booking_id = ?', (booking_id,))
            conn.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
            conn.commit()
            
            booking_details = {
                'booking_id': booking_id,
                'movie_title': booking['title'],
                'showtime': booking['showtime'],
                'seats': booking['seats']
            }
            
            send_booking_email(
                booking['email'],
                f"{booking['first_name']} {booking['last_name']}",
                booking_details,
                is_cancellation=True
            )
            
            conn.close()
            flash(f'Booking {booking_id} has been successfully cancelled.', 'success')
            return render_template('cancel.html', cancelled=True, booking_id=booking_id)
        
        except Exception as e:
            conn.rollback()
            conn.close()
            flash('An error occurred. Please try again.', 'error')
            print(f"Cancel error: {e}")
    
    return render_template('cancel.html')

@app.route('/my-bookings')
@login_required
def my_bookings():
    """View user's bookings"""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, m.title, m.poster_url
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
        WHERE b.user_id = ?
        ORDER BY b.booking_date DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('my_bookings.html', bookings=bookings)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print("Database not found. Please run 'python init_db.py' first.")
    app.run(host='0.0.0.0', port=5000, debug=True)
