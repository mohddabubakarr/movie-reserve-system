<!-- README (paste into GitHub README.md) -->

<h1 align="center">🎬 Movie Reservation System</h1>

<p align="center">
  A full-stack web application built for a university web development project.<br/>
  Browse movies, view details, and reserve or cancel tickets directly in the browser.
</p>

<hr/>

<h2>📌 Project Description</h2>
<p>
  The <strong>Movie Reservation System</strong> is a full-stack web application that allows users to:
</p>
<ul>
  <li>Browse movies</li>
  <li>View movie details</li>
  <li>Reserve movie tickets</li>
  <li>Cancel existing reservations</li>
</ul>

<p>
  The project focuses on delivering a functioning application with a <strong>responsive frontend</strong>,
  a <strong>custom backend</strong>, and a <strong>database</strong> for persistent storage.
</p>

<hr/>

<h2>✨ Key Features</h2>
<ul>
  <li>Responsive UI (mobile-friendly)</li>
  <li>Movie browsing + detail pages</li>
  <li>Ticket reservation and cancellation workflow</li>
  <li>Persistent data storage using SQLite</li>
  <li>Movie data fetched via the OMDb API</li>
</ul>

<hr/>

<h2>🧰 Technologies Used</h2>

<h3>Frontend</h3>
<ul>
  <li>HTML</li>
  <li>CSS</li>
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

<hr/>

<h2>⚙️ Installation &amp; Setup</h2>

<p>
  All source code and required installation files are included in this folder.
  This folder can be zipped and uploaded directly for <strong>Phase 3 submission</strong>.
</p>

<h3>1) Clone or extract the project folder</h3>
<pre><code>git clone https://github.com/your-username/movie-reserve-system.git
cd movie-reserve-system</code></pre>

<h3>2) Create and activate a virtual environment</h3>
<pre><code>python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate</code></pre>

<h3>3) Install dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>4) Initialize the database</h3>
<pre><code>python init_db.py</code></pre>

<h3>5) Run the application</h3>
<pre><code>python app.py</code></pre>

<h3>6) Open in your browser</h3>
<pre><code>http://localhost:8000</code></pre>

<hr/>

<h2>🗂️ Project Structure</h2>
<pre><code>movie-reserve-system/
├── app.py                # Main Flask application
├── init_db.py            # Database setup script
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates (Jinja2)
└── static/               # CSS, JavaScript, images</code></pre>

<hr/>

<h2>🔑 Configuration Notes (OMDb API)</h2>
<p>
  This project uses the <strong>OMDb API</strong> to fetch movie data.
  If your app requires an API key, make sure it is configured as expected by your codebase
  (e.g., environment variable, config file, or directly in the Flask app).
</p>

<ul>
  <li><strong>Tip:</strong> If you use an environment variable, you can export it before running:</li>
</ul>

<pre><code># macOS/Linux
export OMDB_API_KEY="your_key_here"

# Windows (PowerShell)
$env:OMDB_API_KEY="your_key_here"</code></pre>

<hr/>

<h2>🖼️ Screenshots</h2>
<p>
  Add at least 3 responsive screenshots here (desktop / tablet / mobile) to match submission requirements.
</p>

<!-- Replace the placeholders with your real image paths, e.g. ./screenshots/home-desktop.png -->
<ul>
  <li><strong>Home (Desktop)</strong><br/><img src="screenshots/home-desktop.png" alt="Home Desktop" width="700"/></li>
  <li><strong>Movie Details (Tablet)</strong><br/><img src="screenshots/details-tablet.png" alt="Details Tablet" width="500"/></li>
  <li><strong>Reservation (Mobile)</strong><br/><img src="screenshots/reservation-mobile.png" alt="Reservation Mobile" width="300"/></li>
</ul>

<hr/>

<h2>✅ Test Cases (Examples)</h2>
<p>Write your test cases as <strong>actions</strong> and <strong>expected results</strong>:</p>

<ul>
  <li>
    <strong>Test Case 1: Reserve a ticket</strong>
    <ul>
      <li>Action: Open a movie details page and click <em>Reserve</em></li>
      <li>Expected: A confirmation message is shown and reservation is stored in the database</li>
    </ul>
  </li>

  <li>
    <strong>Test Case 2: Cancel a reservation</strong>
    <ul>
      <li>Action: Go to reservations and click <em>Cancel</em> for an existing booking</li>
      <li>Expected: Reservation is removed and the UI updates accordingly</li>
    </ul>
  </li>

  <li>
    <strong>Test Case 3: Movie search/browse</strong>
    <ul>
      <li>Action: Load the homepage and browse/search for a movie</li>
      <li>Expected: Results are displayed and clicking a movie opens its details page</li>
    </ul>
  </li>
</ul>

<hr/>

<h2>📄 License</h2>
<p>
  This project was created for a university course submission. Add a license here if required.
</p>

<hr/>

<h2>🙏 Acknowledgements</h2>
<ul>
  <li>OMDb API for providing movie metadata</li>
  <li>Flask + Bootstrap for rapid full-stack development</li>
</ul>

<!-- End of README -->
