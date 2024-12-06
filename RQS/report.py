from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from backend import QueueSystem
from datetime import datetime  
from tkinter import messagebox, Tk

def generate_report(queue_system):
    """Generate a PDF report of completed users in the queue."""
    
    # Fetch all users from the database
    # Fetch all completed users from the QueueSystem
    completed_users = queue_system.get_all_completed_users()  # Use the new method

    # Debugging: Print completed users to the console
    print("Completed Users:")
    for user in completed_users:
        print(f"Name: {user[1]}, Student ID: {user[2]}, Concern: {user[3]}, Queue Number: {user[4]}")
    # Check if there are no completed users in the database
    if not completed_users:
        # Create a hidden Tkinter root window to use messagebox
        root = Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("No Data", "No completed user data found in the database. Report generation error.")
        root.destroy()  # Close the hidden window
        return  # Exit the function if there are no completed users

    # Create a PDF file
    report_filename = "completed_users_report.pdf"
    c = canvas.Canvas(report_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 40, "Completed Users Report")
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 60, "Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Column headers
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, height - 100, "Name")
    c.drawString(200, height - 100, "Student ID")
    c.drawString(350, height - 100, "Concern")
    c.drawString(500, height - 100, "Queue Number")

    # Draw a line under the headers
    c.line(30, height - 105, width - 30, height - 105)

    # Add completed user data
    y = height - 120
    for user in completed_users:
        c.setFont("Helvetica", 12)
        c.drawString(30, y, user[1])  # Name
        c.drawString(200, y, str(user[2]))  # Student ID
        c.drawString(350, y, user[3])  # Concern
        c.drawString(500, y, str(user[4]))  # Queue Number
        y -= 20  # Move down for the next line

    # Save the PDF
    c.save()
    print(f"Report generated: {report_filename}")

# Main execution
if __name__ == "__main__":
    queue_system = QueueSystem()  # Create an instance of QueueSystem
    generate_report(queue_system)  # Pass the instance to the function