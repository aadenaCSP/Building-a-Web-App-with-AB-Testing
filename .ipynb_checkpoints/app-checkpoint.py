import random
import datetime
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

# Function to initialize the SQLite database and create the table if not exists
def init_db():
    with sqlite3.connect('interactions.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT,
                        timestamp TEXT,
                        ip TEXT
                    )''')
        conn.commit()

# Call this function to initialize the database when the app starts
init_db()

@app.route('/')
def home():
    """ Static homepage with description """
    return render_template('home.html')

@app.route('/home')
def home_page():
    """ Randomly assign a user to either Version A or Version B """
    version = random.choice(['A', 'B'])
    
    # Store the version in the session to ensure stickiness across visits
    session['version'] = version
    print(f"Assigned version: {version}")  # Debugging line
    
    if version == 'A':
        return redirect(url_for('home_a'))
    else:
        return redirect(url_for('home_b'))

@app.route('/home/a')
def home_a():
    """ Version A user page """
    # Retrieve interaction data from the session to display it on the page
    interaction_data = session.get('interaction_data', [])
    return render_template('home_a.html', interaction_data=interaction_data)

@app.route('/home/b')
def home_b():
    """ Version B user page """
    # Retrieve interaction data from the session to display it on the page
    interaction_data = session.get('interaction_data', [])
    return render_template('home_b.html', interaction_data=interaction_data)

@app.route('/track', methods=['POST'])
def track_interaction():
    """ Track interaction, log to file, and session """
    version = session.get('version', 'unknown')  # Retrieve version from session
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr
    
    # Log the interaction data to the session
    interaction_info = f"{timestamp} - IP: {ip_address} - Version: {version} - Interaction tracked"
    
    # Retrieve existing interaction data, or create an empty list if none exist
    interaction_data = session.get('interaction_data', [])
    interaction_data.append(interaction_info)
    
    # Store the updated interaction data back in the session
    session['interaction_data'] = interaction_data
    
    # Log the interaction data to the console (optional)
    print(f"Logged Interaction - IP: {ip_address}, Version: {version}, Timestamp: {timestamp}")
    
    # Append the interaction data to the log file (optional)
    with open('interaction_log.txt', 'a') as log_file:
        log_file.write(f"{interaction_info}\n")
    
    # Insert the interaction into the SQLite database
    with sqlite3.connect('interactions.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO interactions (version, timestamp, ip) VALUES (?, ?, ?)', 
                  (version, timestamp, ip_address))
        conn.commit()
    
    # Return the interaction info as a response (this is what will be shown on the page)
    return interaction_info

@app.route('/go_back')
def go_back():
    """ Go back to the original homepage """
    session.pop('version', None)  # Remove the current version from session
    session.pop('interaction_data', None)  # Optional: Remove interaction data from session if you want to reset
    return redirect(url_for('home'))  # Redirect to the static homepage

if __name__ == '__main__':
    app.run(debug=True)
