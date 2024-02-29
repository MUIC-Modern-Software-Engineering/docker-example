from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


@app.route('/')
def index():
    # Retrieve messages from the database
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages")
    messages = [row[0] for row in cur.fetchall()]
    cur.close()
    return render_template('index.html', messages=messages)


@app.route('/post_message', methods=['POST'])
def post_message():
    message = request.form['message']
    # Save the message to the database
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
