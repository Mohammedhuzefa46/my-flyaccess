import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
import os

# Initialize Flask app
app = Flask(__name__)  # Corrected here

# Database setup (SQLite) - stores email addresses
def create_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Store email in database
def store_email(email):
    try:
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False

# Send email to customer using Gmail SMTP
def send_email_to_customer(customer_email):
    sender_email = os.getenv('GMAIL_USER')  # Use environment variable for Gmail user
    password = os.getenv('GMAIL_PASSWORD')  # Use environment variable for Gmail password
    receiver_email = customer_email
    subject = "Thank You for Your Subscription!"
    body = "Hello, thank you for subscribing. We are excited to have you!"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# API route to handle storing email, sending email and responding to the user
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Step 1: Store email in database
    if store_email(email):
        # Step 2: Send email to customer
        if send_email_to_customer(email):
            # Step 3: Respond to user
            return jsonify({"message": "Subscription successful! An email has been sent to you."}), 200
        else:
            return jsonify({"error": "There was an error sending the email."}), 500
    else:
        return jsonify({"error": "This email is already subscribed."}), 400

if __name__ == '__main__':  # Corrected here
    create_db()  # Create database table if it doesn't exist
    app.run(debug=True)
