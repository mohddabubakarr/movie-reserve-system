Project Description

The Movie Reservation System is a full-stack web application developed for a university web development project.
It allows users to browse movies, view details, and reserve or cancel movie tickets through a web browser.

The project focuses on delivering a functioning application with a responsive frontend, a custom backend, and a database for data storage.

Technologies Used

Frontend

HTML

CSS

JavaScript

Bootstrap

Jinja2 Templates

Backend

Python

Flask

Database

SQLite

External API

OMDb API (movie data)

Installation & Setup

All source code and required installation files are included in this folder.
This folder can be zipped and uploaded directly for Phase 3 submission.

Steps

Clone or extract the project folder

git clone https://github.com/your-username/movie-reserve-system.git
cd movie-reserve-system


Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Initialize the database

python init_db.py


Run the application

python app.py


Open the application in a browser

http://localhost:8000

Project Structure

app.py – Main Flask application

init_db.py – Database setup script

templates/ – HTML templates (Jinja2)

static/ – CSS, JavaScript, images

requirements.txt – Python dependencies