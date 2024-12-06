import os
import re  # Import regular expressions for validation
import heapq  # Import heapq for priority queue functionality
import time
from database import Database

LOCK_FILE = "queue_lock.lock"

def acquire_lock():
    """Acquire a lock by creating a lock file."""
    while os.path.exists(LOCK_FILE):
        time.sleep(0.1)  # Wait until the lock is released
    open(LOCK_FILE, 'w').close()  # Create the lock file

def release_lock():
    """Release the lock by deleting the lock file."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

class QueueSystem:
    def __init__(self):
        """Initialize the QueueSystem and the Database."""
        print("Initializing QueueSystem...")
        self.db = Database()
        self.queue_number = self.db.get_last_queue_number() + 1  # Start from the last queue number in the database
        print(f"Starting queue_number: {self.queue_number}")  # Debugging line
        self.priority_queue = []

    def clear_queue(self):
        """Clear the priority queue."""
        self.priority_queue = []

    def generate_queue_number(self):
        """Generate a new queue number."""
        self.queue_number += 1
        return self.queue_number

    def save_user_details(self, name, student_id, concern, queue_type):
        """Save user details to the database and return user data."""
        current_queue_number = self.queue_number
        self.db.insert_user(name, student_id, concern, current_queue_number, queue_type)
        self.add_to_queue(queue_type, name, student_id, concern)
        self.queue_number += 1  # Increment for the next user
        return {
            'queue_number': current_queue_number
        }

    def add_to_queue(self, queue_type, name, student_id, concern):
        """Add a user to the priority queue based on their queue type."""
        priority = 1 if queue_type == "PO" else 2
        user_info = (name, student_id, concern)
        heapq.heappush(self.priority_queue, (priority, user_info))

    def process_queue(self):
        """Process the queue and return users in order of priority."""
        # Sort the priority queue to ensure "PO" is processed first
        self.priority_queue.sort(key=lambda x: (x[0], x[1][0] != "PO"))  # Sort by priority, then by type
        while self.priority_queue:
            priority, user_info = heapq.heappop(self.priority_queue)
            print(f"Processing {user_info} with priority {priority}")
    
    def get_all_completed_users(self):
        """Retrieve all completed users from the database."""
        print("Fetching all completed users from the QueueSystem...")  # Debugging line
        completed_users = self.db.get_all_completed_users()  # Call the database method
        print(f"Completed users fetched: {completed_users}")  # Debugging line
        return completed_users

    def get_all_users(self):
        """Retrieve all user data from the database."""
        print("Fetching all users from the database...")  # Debugging line
        users = self.db.get_all_users()
        print(f"Users fetched: {users}")  # Debugging line
        return users

    def close(self):
        """Close the database connection."""
        print("Closing database connection...") 
        self.db.close()

    @staticmethod
    def validate_user_input(name, student_id, concern):
        """Validate user input for name, student ID, and concern."""
        if not student_id.isdigit():
            return False, "Student ID must be numbers only."
        if not re.match(r'^[A-Za-z\s]+$', name):
            return False, "Name must contain only letters and spaces."
        if not concern.strip():
            return False, "Concern cannot be empty."
        return True, "Valid input."

    def insert_user(self, name, student_id, concern, queue_number, queue_type):
        """Insert a new user into the users table."""
        acquire_lock()  # Acquire the lock before modifying the database
        try:
            print(f"Inserting user: {name}, Student ID: {student_id}, Concern: {concern}, Queue Number: {queue_number}, Queue Type: {queue_type}")  # Debugging line
            self.db.insert_user(name, student_id, concern, queue_number, queue_type)
            print("User  inserted successfully.")  # Debugging line
        except Exception as e:
            print(f"An error occurred while inserting user: {e}")  # Debugging line
        finally:
            release_lock()  # Ensure the lock is released

    def update_user_status(self, student_id, new_status):
        """Update the status of a user in the database."""
        acquire_lock()  # Acquire the lock before modifying the database
        try:
            print(f"Updating user status: Student ID: {student_id}, New Status: {new_status}")
            # Debugging line
            self.db.update_user_status(student_id, new_status)  # Call the database method to update status
            print(f"User  {student_id} status updated to {new_status}.")
        except Exception as e:
            print(f"An error occurred while updating user status: {e}")  # Debugging line
        finally:
            release_lock()  # Ensure the lock is released
    