
# A/B Testing Web Application

## Overview

This is a simple A/B testing web application built using Flask. The application randomly assigns users to one of two versions (A or B) of a user page and tracks interactions. It also logs these interactions in a database and a text file for further analysis.

## Features

- **Homepage**: A static homepage introducing the web app.
- **Version A and Version B**: Users are randomly assigned to either version A or B of the user page.
- **Interaction Tracking**: Users can interact with the page, and their interactions (including IP address, timestamp, and version) are logged in both a text file and a SQLite database.
- **Session Stickiness**: Once a user is assigned to a version, they will consistently see the same version throughout their session.
- **Log File**: Interaction details are stored in an `interaction_log.txt` file.
- **Database**: Interaction details are also stored in a SQLite database `interactions.db`.

## Folder Structure

```
A/B Testing Web Application/
│
├── app.py                # Main Python file to run the Flask app
├── interaction_log.txt   # Log file where interaction data is stored
├── interactions.db       # SQLite database where interaction data is stored
├── templates/            # Folder containing HTML files
│   ├── home.html         # Homepage (initial landing page)
│   ├── home_a.html       # Version A of the user page
│   └── home_b.html       # Version B of the user page
├── static/               # Folder containing static files like CSS and images
│   └── style.css         # CSS file for styling the pages
└── README.md             # Project README (this file)
```

## Database Setup

### SQLite Database (`interactions.db`)

The application uses an SQLite database (`interactions.db`) to store interaction data. The database is created automatically the first time the application runs. It contains a single table `interactions` with the following columns:

- `id`: The unique identifier for each interaction (auto-incremented).
- `version`: The version (either 'A' or 'B') of the user page the user interacted with.
- `timestamp`: The timestamp when the interaction occurred.
- `ip`: The IP address of the user who interacted with the page.

### Creating the Database

When the app is run for the first time, the `interactions.db` SQLite database is created automatically with the following SQL schema:

```sql
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    ip TEXT NOT NULL
);
```

### Logging Interactions to the Database

Each time a user interacts with the page (by clicking a button), the following data is stored in both the `interaction_log.txt` file and the `interactions.db` database:

- **IP address** of the user
- **Timestamp** of the interaction
- **Version** of the page (A or B)

The interaction is inserted into the database using the following SQL query:

```python
cursor.execute("INSERT INTO interactions (version, timestamp, ip) VALUES (?, ?, ?)", (version, timestamp, ip_address))
conn.commit()
```

This ensures that all interaction data is stored persistently in the database for later analysis.

### Viewing Interactions in the Database

To view the interactions stored in the database, you can open the SQLite database in a terminal or any SQLite browser. Use the following commands:

1. Open the database:

```bash
sqlite3 interactions.db
```

2. List the tables:

```sql
.tables
```

3. View the interaction data:

```sql
SELECT * FROM interactions;
```

## How to Run the Application

### Prerequisites

- Python 3.x
- Flask
- SQLite (which is included with Python)

### Installation

1. Clone the repository:

```bash
git clone <repo_url>
cd <project_folder>
```

2. Install Flask:

```bash
pip install flask
```

### Running the Application

To start the Flask development server, run the following command:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`.

### Interacting with the App

1. Visit the homepage.
2. Click the button to navigate to either Version A or Version B.
3. Interact with the page (e.g., click a button) to log the interaction data.
4. The interaction data will be stored in both the `interaction_log.txt` file and the `interactions.db` database.
