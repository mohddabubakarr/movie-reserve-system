<h1 align="center">Movie Reservation System</h1>
<p align="center">
  A full-stack Flask web application to browse movies, view details, reserve seats, and cancel bookings.
</p>

<hr />

<h2>Overview</h2>
<p>
  The Movie Reservation System is a full-stack web application developed for a university web development project.
  It allows users to browse available movies, view movie details, and make or cancel reservations through a web browser.
  Movie information (e.g., posters and metadata) is loaded via the backend using the OMDb API (with a sample-data fallback).
</p>

<hr />

<h2>Key Features</h2>
<ul>
  <li>Browse available movies</li>
  <li>Movie detail page (poster + metadata)</li>
  <li>Seat selection and booking confirmation</li>
  <li>Booking cancellation</li>
  <li>Seat availability enforcement (already-booked seats are disabled)</li>
  <li>Responsive layout for different viewport sizes</li>
</ul>

<hr />

<h2>Tech Stack</h2>
<h3>Frontend</h3>
<ul>
  <li>HTML / CSS</li>
  <li>JavaScript</li>
  <li>Bootstrap</li>
  <li>Jinja2 Templates</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Python</li>
  <li>Flask</li>
</ul>

<h3>Database</h3>
<ul>
  <li>SQLite</li>
</ul>

<h3>External API</h3>
<ul>
  <li>OMDb API (movie data)</li>
</ul>

<hr />

<h2>Project Structure</h2>
<pre><code>Movie-Reserve-Platform/
├── app.py
├── init_db.py
├── requirements.txt
├── README.md
├── database.db              (generated locally)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── movie_details.html
│   └── ...
└── static/
    ├── css/
    ├── js/
    └── images/
</code></pre>

<hr />

<h2>Setup & Run</h2>

<h3>1) Clone the repository</h3>
<pre><code>git clone https://github.com/mohddabubakarr/movie-reserve-system.git
cd movie-reserve-system
</code></pre>

<h3>2) Create and activate a virtual environment</h3>
<p><b>macOS / Linux</b></p>
<pre><code>python3 -m venv venv
source venv/bin/activate
</code></pre>

<p><b>Windows (PowerShell)</b></p>
<pre><code>python -m venv venv
venv\Scripts\activate
</code></pre>

<h3>3) Install dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>4) Initialize the database</h3>
<pre><code>python3 init_db.py
</code></pre>

<h3>5) Run the application</h3>
<pre><code>python3 app.py
</code></pre>

<h3>6) Open in your browser</h3>
<p>
  The terminal will display the running address. Commonly:
</p>
<pre><code>http://127.0.0.1:8000
</code></pre>

<hr />


<p><b>Notes:</b></p>
<ul>
  <li>Do not commit <code>.env</code> (keep it in <code>.gitignore</code>).</li>
  <li>If the API is unavailable, the project can fall back to sample movie data during database initialization.</li>
</ul>

<hr />

<h2>Testing</h2>

<h3>Test Data</h3>
<ul>
  <li>SQLite database initialized with sample movies via <code>init_db.py</code></li>
  <li>Seat layout available per movie screening</li>
  <li>Test bookings created and cancelled to validate flows</li>
</ul>

<h3>Test Cases (Action → Expected Result)</h3>
<ul>
  <li>
    <b>Booking confirmation:</b><br />
    Action: Select available seats and click the booking confirm button<br />
    Expected: Confirmation message is shown and the booking is saved in the database
  </li>
  <li>
    <b>Booking cancellation:</b><br />
    Action: Cancel an existing booking via the cancellation option<br />
    Expected: Cancellation confirmation is shown and the booking is removed/updated in the database
  </li>
</ul>

<hr />

<h2>Notes / Limitations</h2>
<ul>
  <li>This is a university project and focuses on delivering a functioning web application with clear installation instructions.</li>
</ul>

<hr />

<h2>Author</h2>
<p>
  Muhammad Abubakar
</p>

<hr />

<p align="center">
  <i>University project (academic submission).</i>
</p>

