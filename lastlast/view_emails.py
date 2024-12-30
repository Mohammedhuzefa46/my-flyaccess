import sqlite3

def view_emails():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    
    # Query all emails from the database
    c.execute('SELECT * FROM users')
    
    # Fetch all rows from the result of the query
    rows = c.fetchall()
    
    # Print the emails
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}")
    
    conn.close()

# Call the function to view emails
view_emails()
