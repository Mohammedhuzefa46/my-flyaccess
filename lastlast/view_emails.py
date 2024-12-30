import sqlite3

def view_emails():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        
        # Query all emails from the database
        c.execute('SELECT * FROM users')
        
        # Fetch all rows from the result of the query
        rows = c.fetchall()
        
        # Check if there are any emails to display
        if rows:
            print("Emails in the database:")
            print("-" * 30)
            for row in rows:
                print(f"ID: {row[0]}, Email: {row[1]}")
        else:
            print("No emails found in the database.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Call the function to view emails
if __name__ == "__main__":
    view_emails()
