from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
from backend import QueueSystem  # Import the QueueSystem class
import winsound
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\viewing_MonitorAssets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize the window
window = Tk()
window.title("Viewing Monitor")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window dimensions
window_width = 1280
window_height = 800
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create the canvas
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=800,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# Load images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(640.0, 400.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(113.0, 75.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(639.0, 415.0, image=image_image_3)

# Create text placeholders for time and date
time_text_shadow2 = canvas.create_text(89.0, 687.0, anchor="nw", text="", fill="#C0C0C0", font=("Times New Roman", 49 * -1))
time_text_shadow1 = canvas.create_text(86.0, 686.0, anchor="nw", text="", fill="#A0A0A0", font=("Times New Roman", 49 * -1))
time_text = canvas.create_text(87.0, 685.0, anchor="nw", text="", fill="#000000", font=("Times New Roman", 49 * -1))

day_text_shadow2 = canvas.create_text(799.0, 687.0, anchor="nw", text="", fill="#C0C0C0", font=("Times New Roman", 49 * -1))
day_text_shadow1 = canvas.create_text(798.0, 686.0, anchor="nw", text="", fill="#A0A0A0", font=("Times New Roman", 49 * -1))
day_text = canvas.create_text(800.0, 685.0, anchor="nw", text="", fill="#000000", font=("Times New Roman", 49 * -1))

date_text_shadow2 = canvas.create_text(1042.0, 731.5, anchor="nw", text="", fill="#C0C0C0", font=("Times New Roman", 22 * -1))
date_text_shadow1 = canvas.create_text(1041.0, 731.0, anchor="nw", text="", fill="#A0A0A0", font=("Times New Roman", 22 * -1))
date_text = canvas.create_text(1040.0, 730.0, anchor="nw", text="", fill="#000000", font=("Times New Roman", 22 * -1))

# Create placeholders for queue information
window_1 = canvas.create_text(255.0, 280.0, anchor="center", text="", fill="#2C3167", font=("Times New Roman", 36))
window_2 = canvas.create_text(650.0, 280.0, anchor="center", text="", fill="#2C3167", font=("Times New Roman", 36))
window_3 = canvas.create_text(1000.0, 280.0, anchor="center", text="", fill="#2C3167", font=("Times New Roman", 36))

overviewwindow_1 = canvas.create_text(255.0, 500.0, anchor="center", text="", fill="#2C3167", font=(" Times New Roman", 36))
overviewwindow_2 = canvas.create_text(650.0, 500.0, anchor="center", text="", fill="#2C3167", font=("Times New Roman", 36))
overviewwindow_3 = canvas.create_text(1000.0, 500.0, anchor="center", text="", fill="#2C3167", font=("Times New Roman", 36))

# Initialize the QueueSystem
queue_system = QueueSystem()  # Create an instance of the QueueSystem class

def update_viewing_monitor_display():
    """Update the display with the current queue information and overview."""
    users = queue_system.get_all_users()  # Fetch all users from the QueueSystem

    ro_users = [(user[5], user[4], user[2]) for user in users if user[5] == "RO"]  # (queue_type, queue_number, student_id)
    po_users = [(user[5], user[4], user[2]) for user in users if user[5] == "PO"]  # (queue_type, queue_number, student_id)

    # Update window text for RO users
    window_1_text = ro_users[0][1] if len(ro_users) > 0 else " "  # Queue number for first RO
    window_2_text = ro_users[1][1] if len(ro_users) > 1 else " "  # Queue number for second RO
    window_3_text = po_users[0][1] if po_users else " "  # Queue number for first PO

    canvas.itemconfig(window_1, text=f"RO - {window_1_text}" if window_1_text != " " else " ")
    canvas.itemconfig(window_2, text=f"RO - {window_2_text}" if window_2_text != " " else " ")
    canvas.itemconfig(window_3, text=f"PO - {window_3_text}" if window_3_text != " " else " ")

    # Automatically mark users in the window as "Serving" if they are currently "Waiting"

    # For the first RO user
    student_id_1 = None  # Initialize the variable
    if window_1_text != " " and len(ro_users) > 0:
        student_id_1 = ro_users[0][2]  # Get student ID for the first RO user

    if student_id_1 is not None:  # Check if student_id_1 has been assigned
        print(f"Checking status for first RO user: Student ID = {student_id_1}")  # Debugging line
        try:
            current_status_1 = next(user[6] for user in users if user[2] == student_id_1)  # Corrected index
            print(f"Current status for Student ID {student_id_1}: {current_status_1}")  # Debugging line
            if current_status_1 == 'Waiting':
                print(f"Updating status for Student ID {student_id_1} to 'Serving'")  # Debugging line
                queue_system.update_user_status(student_id_1, 'Serving')  # Update status to 'Serving'
                winsound.PlaySound("C:/Users/Enoch Gabriel Astor/Desktop/RQS/assets/pingping.wav", winsound.SND_FILENAME)
            else:
                print(f"Student ID {student_id_1} is not 'Waiting', current status: {current_status_1}")  # Debugging line
        except StopIteration:
            print(f"Student ID {student_id_1} not found in users list.")
    else:
        print("No valid first RO user to check.")  # Handle case where there is no user

    # For the second RO user
    student_id_2 = None  # Initialize the variable
    if window_2_text != " " and len(ro_users) > 1:
        student_id_2 = ro_users[1][2]  # Get student ID for the second RO user

    if student_id_2 is not None:  # Check if student_id_2 has been assigned
        print(f"Checking status for second RO user: Student ID = {student_id_2}")  # Debugging line
        try:
            current_status_2 = next(user[6] for user in users if user[2] == student_id_2)  # Corrected index
            print(f"Current status for Student ID {student_id_2}: {current_status_2}")  # Debugging line
            if current_status_2 == 'Waiting':
                print(f"Updating status for Student ID {student_id_2} to 'Serving'")  # Debugging line
                queue_system.update_user_status(student_id_2, 'Serving')  # Update status to 'Serving'
                winsound.PlaySound("C:/Users/Enoch Gabriel Astor/Desktop/RQS/assets/pingping.wav", winsound.SND_FILENAME)
            else:
                print(f"Student ID {student_id_2} is not 'Waiting', current status: {current_status_2}")  # Debugging line
        except StopIteration:
            print(f"Student ID {student_id_2} not found in users list.")
    else:
        print("No valid second RO user to check.")  # Handle case where there is no user

    # For the first PO user
    student_id_3 = None  # Initialize the variable
    if window_3_text != " " and len(po_users) > 0:
        student_id_3 = po_users[0][2]  # Get student ID for the first PO user

    if student_id_3 is not None:  # Check if student_id_3 has been assigned
        print(f"Checking status for first PO user: Student ID = {student_id_3}")  # Debugging line
        try:
            current_status_3 = next(user[6] for user in users if user[2] == student_id_3)  # Corrected index
            print(f"Current status for Student ID {student_id_3}: {current_status_3}")  # Debugging line
            if current_status_3 == 'Waiting':
                print(f"Updating status for Student ID {student_id_3} to 'Serving'")  # Debugging line
                queue_system.update_user_status(student_id_3, 'Serving')  # Update status to 'Serving'
                winsound.PlaySound("C:/Users/Enoch Gabriel Astor/Desktop/RQS/assets/pingping.wav", winsound.SND_FILENAME)
            else:
                print(f"Student ID {student_id_3} is not 'Waiting', current status: {current_status_3}")  # Debugging line
        except StopIteration:
            print(f"Student ID {student_id_3} not found in users list.")
    else:
        print("No valid first PO user to check.")  # Handle case where there is no user

    # Prepare overview text
    overview_1_text = ro_users[2][1] if len(ro_users) > 2 else ""  # Next RO user after window 1 and 2
    overview_2_text = ro_users[3][1] if len(ro_users) > 3 else ""  # Next RO user after overview 1
    overview_3_text = po_users[1][1] if len(po_users) > 1 else ""  # Next PO user after window 3

    # Update the overview windows
    canvas.itemconfig(overviewwindow_1, text=f"RO - {overview_1_text}" if overview_1_text else " ")
    canvas.itemconfig(overviewwindow_2, text=f"RO - {overview_2_text}" if overview_2_text else " ")
    canvas.itemconfig(overviewwindow_3, text=f"PO - {overview_3_text}" if overview_3_text else " ")

    window.after(10000, update_viewing_monitor_display)  # Schedule the next update
    
def update_datetime():
    """Update the date and time display."""
    current = datetime.now()
    
    # Update time (24-hour format)
    time_string = f"TIME: {current.strftime('%H:%M:%S')}"
    canvas.itemconfig(time_text_shadow2, text=time_string)
    canvas.itemconfig(time_text_shadow1, text=time_string)
    canvas.itemconfig(time_text, text=time_string)
    
    # Update day
    day_string = f"DATE: {current.strftime('%A').upper()}"  # Get the current day
    canvas.itemconfig(day_text_shadow2, text=day_string)
    canvas.itemconfig(day_text_shadow1, text=day_string)
    canvas.itemconfig(day_text, text=day_string)  # Update the main text layer
    
    # Update date
    date_string = current.strftime('%m/%d/%Y')
    canvas.itemconfig(date_text_shadow2, text=date_string)
    canvas.itemconfig(date_text_shadow1, text=date_string)
    canvas.itemconfig(date_text, text=date_string)
    
    # Schedule the next update
    window.after(1000, update_datetime)

update_viewing_monitor_display()
update_datetime()

# STI College title with shadow effects
canvas.create_text(
    652.0,
    78.0,
    anchor="center",
    text="STI College Global City",
    fill="#C0C0C0",
    font=("Fredoka One", 55 * -1)
)
canvas.create_text(
    651.0,
    80.0,
    anchor="center",
    text="STI College Global City",
    fill="#A0A0A0",
    font=("Fredoka One", 55 * -1)
)
canvas.create_text( #main
    650.0,
    78.0,
    anchor="center",
    text="STI College Global City",
    fill="#2C3167",
    font=("Fredoka One", 55 * -1)
)

# Finalize the window settings
window.resizable(False, False)
window.mainloop()
