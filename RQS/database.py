import sqlite3

class Database:
    def __init__(self, db_name="queue_system.db"):
        """Initialize the database connection and create the table if it doesn't exist."""
        print(f"Connecting to database: {db_name}")  # Debugging line
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the users table in the database."""
        print("Creating users table if it doesn't exist...")  # Debugging line
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id INTEGER NOT NULL,
            concern TEXT NOT NULL,
            queue_number INTEGER NOT NULL,
            queue_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Waiting'  -- New status column
        )
        """)
        self.connection.commit()

    def insert_user(self, name, student_id, concern, queue_number, queue_type):
        """Insert a new user into the users table."""
        print(f"Inserting user: {name}, Student ID: {student_id}, Concern: {concern}, Queue Number: {queue_number}, Queue Type: {queue_type}")  # Debugging line
        try:
            self.cursor.execute("""
            INSERT INTO users (name, student_id, concern, queue_number, queue_type, status) VALUES (?, ?, ?, ?, ?, 'Waiting')
            """, (name, student_id, concern, queue_number, queue_type))
            self.connection.commit()
            print("User  inserted successfully.")  # Debugging line
        except sqlite3.Error as e:
            print(f"An error occurred while inserting user: {e}")  # Debugging line

    def get_last_queue_number(self):
        """Retrieve the last queue number from the users table."""
        print("Retrieving last queue number...")  # Debugging line
        self.cursor.execute("SELECT MAX(queue_number) FROM users")
        result = self.cursor.fetchone()
        last_queue_number = result[0] if result[0] is not None else 0  # Return 0 if no records exist
        print(f"Last queue number retrieved: {last_queue_number}")  # Debugging line
        return last_queue_number

    def get_all_users(self):
        """Retrieve all users from the users table."""
        print("Retrieving all users from the database...")  # Debugging line
        self.cursor.execute("SELECT * FROM users WHERE status IN ('Waiting', 'Serving')")  # Only get waiting and serving users
        users = self.cursor.fetchall()
        print(f"All users retrieved: {users}")  # Debugging line
        return users
    

    def update_user_status(self, student_id, new_status):
        """Update the status of a user in the database."""
        try:
            self.cursor.execute("""
            UPDATE users SET status = ? WHERE student_id = ?
            """, (new_status, student_id))
            self.connection.commit()
            print(f"User  {student_id} status updated to {new_status}.")
        except sqlite3.Error as e:
            print(f"An error occurred while updating user status: {e}")

    def close(self):
        """Close the database connection."""
        print("Closing database connection...")  # Debugging line
        self.connection.close()
    
    def get_all_completed_users(self):
        """Retrieve all completed users from the users table."""
        print("Retrieving all completed users from the database...")  # Debugging line
        self.cursor.execute("SELECT * FROM users WHERE status = 'Completed'")  # Only get completed users
        completed_users = self.cursor.fetchall()
        print(f"Completed users retrieved: {completed_users}")  # Debugging line
        return completed_users