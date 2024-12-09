from datetime import datetime
import time
from tkinter import *
from tkinter import ttk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from backend import QueueSystem
from report import generate_report  
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\Admin_Assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Admin")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Set the window dimensions
window_width = 1280
window_height = 800
# Calculate x and y coordinates to center the window
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
window.configure(bg="#FFFFFF")
queue_system = QueueSystem()

def show_full_concern(event):
    """Show the full concern in a new window when the concern is clicked."""
    # Get the clicked item and its column
    region = tree.identify_region(event.x, event.y)
    if region == "cell":
        # Get the item and column index
        row_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)

        # Check if the clicked column is the "Concern" column
        if column_id == "#4":  
            concern = tree.item(row_id)['values'][3]  # Get the concern text
            print(f"Concern retrieved: {concern}")  # Debugging line
            
            # Create a new window to display the full concern
            concern_window = Toplevel(window)
            concern_window.title("Concern")
            concern_window.geometry("400x200")  # Set the size of the window
            
            # Add a label to display the concern
            concern_label = Label(concern_window, text=concern, wraplength=380, justify="left")
            concern_label.pack(pady=20, padx=20)  # Add some padding
            
            # Add a button to close the window
            close_button = Button(concern_window, text="Close", command=concern_window.destroy)
            close_button.pack(pady=10)

def copy_student_id(event):
    """Copy the selected student's ID to the clipboard."""
    # Get the clicked item and its column
    region = tree.identify_region(event.x, event.y)
    if region == "cell":
        # Get the item
        selected_item = tree.selection()
        if selected_item:
            # Get the student ID value (index 1 because it's the second column)
            student_id = tree.item(selected_item[0])['values'][1]
            # Clear clipboard and copy new value
            window.clipboard_clear()
            window.clipboard_append(student_id)
            
            # Optional: Show a small popup message
            popup = Toplevel(window)
            popup.geometry("300x50")
            popup.title("")
            
            # Position popup near mouse click
            popup.geometry(f"+{event.x_root}+{event.y_root}")
            
            # Add message
            Label(popup, text=f"Student ID {student_id} copied!").pack(pady=10)
            popup.after(1000, popup.destroy)

def mark_user_completed():
    """Mark the currently selected user as completed."""
    selected_item = tree.selection()  # Get the selected item in the Treeview
    if selected_item:
        # Debugging: Print the selected item
        print(f"Selected item: {selected_item}")  # Debugging line
        
        # Get the student ID from the selected item
        student_id = tree.item(selected_item[0])['values'][1]  # Assuming student_id is in the second column
        print(f"Student ID retrieved: {student_id}")  # Debugging line
        
        # Update the user status to 'completed'
        queue_system.update_user_status(student_id, 'Completed')
        print(f"User  with Student ID {student_id} marked as Completed.")  # Confirm update
        
        # Refresh the queue to show the latest state
        refresh_queue()  # Call refresh_queue to update the GUI
    else:
        messagebox.showwarning("No Selection", "Please select a user to mark as completed.")

def reset_queue():
    """Reset the queue by clearing the users table and reinitializing the QueueSystem."""
    global queue_system  # Ensure we are modifying the global variable
    print("Attempting to reset the queue...")

    # Clear the contents of the users table
    if clear_users_table():
        # Close the existing database connection
        queue_system.close()
        
        clear_table()
        
        # Reinitialize the QueueSystem to create a new database connection
        queue_system = QueueSystem()  # This should open a new database connection
        print("New queue_system initialized.")
    else:
        print("Failed to reset the queue. Users table could not be cleared.")

    # Refresh the queue to show the latest state
    refresh_queue()  # Call refresh_queue to update the GUI

def clear_users_table():
    """Clear the users table in the database."""
    try:
        # Use the database connection to execute the delete command
        queue_system.db.cursor.execute("DELETE FROM users")  # Clear the users table
        queue_system.db.connection.commit()  # Commit the changes
        print("Users table cleared.")
        return True
    except Exception as e:
        print(f"Error clearing users table: {e}")
        return False  # Indicate failure

def refresh_queue():
    """Refresh the Treeview to show the latest queue data."""
    global queue_system  # Declare it as global to use the modified instance
    print(f"Refreshing queue with current queue_system: {queue_system}")  # Debugging line
    clear_table()
    users = queue_system.get_all_users()  # Fetch users from the database
    
    if not users: 
        messagebox.showinfo("Queue Status", "The queue is currently empty.")  
    else:
        load_users_into_treeview(users) 

def clear_table():
    for item in tree.get_children():
        tree.delete(item)

def load_users_into_treeview(users):
    """Load users from the database into the Treeview."""
    clear_table()
    for user in users:
        # Assuming user is a tuple like (id, name, student_id, concern, queue_number, queue_type)
        tree.insert("", "end", values=(user[1], user[2], user[5], user[3], user[4], user[6]))  # Ensure user[5] is valid view columns

        
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

# Frame for table
table_frame = Frame(window)
table_frame.place(x=50, y=150, width=900, height=400)

# Style for Table
style = ttk.Style()
style.configure("Treeview.Heading", 
    font=('Arial Bold', 12, 'bold'),  
    foreground='black',
    background='#2C3167'
)
style.configure("Treeview", 
    font=('Arial', 11),  
    rowheight=30  
)

# Create Treeview
tree = ttk.Treeview(table_frame, 
    columns=("Name", "Student ID", "PO/RO", "Concern", "Queue Number", "Status"),  
    show="headings",
    style="Treeview"
)

# Column headings
tree.heading("Name", text="Surname")
tree.heading("Student ID", text="Student ID")
tree.heading("PO/RO", text="PO/RO")
tree.heading("Concern", text="Concern")
tree.heading("Queue Number", text="Queue Number")
tree.heading("Status", text="Status")  

# Column widths
tree.column("Name", width=100, anchor="center")
tree.column("Student ID", width=150, anchor="center")
tree.column("PO/RO", width=100, anchor="center")
tree.column("Concern", width=120, anchor="center")
tree.column("Queue Number", width=200, anchor="center")
tree.column("Status", width=100, anchor="center") 

tree.pack(expand=True, fill=BOTH)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    640.0,
    400.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    89.0,
    95.0,
    image=image_image_2
)


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: reset_queue(),
    relief="flat"
)
button_1.place(x=950.0, y=271.0, width=330.0, height=146.0)

button_image_hover_1 = PhotoImage(file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(image=button_image_hover_1)
def button_1_leave(e):
    button_1.config(image=button_image_1)

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: refresh_queue(),
    relief="flat"
)
button_2.place(x=950.0, y=151.0, width=330.0, height=139.0)

button_image_hover_2 = PhotoImage(file=relative_to_assets("button_hover_2.png"))

def button_2_hover(e):
    button_2.config(image=button_image_hover_2)
def button_2_leave(e):
    button_2.config(image=button_image_2)

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)



button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: generate_report(queue_system),
    relief="flat"
)
button_4.place(x=950.0, y=412.0, width=330.0, height=126.0)

button_image_hover_4 = PhotoImage(file=relative_to_assets("button_hover_4.png"))

def button_4_hover(e):
    button_4.config(image=button_image_hover_4)
def button_4_leave(e):
    button_4.config(image=button_image_4)

button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: mark_user_completed(),
    relief="flat"
)
button_5.place(x=950.0, y=538.0, width=330.0, height=125.0)

button_image_hover_5 = PhotoImage(file=relative_to_assets("button_hover_5.png"))

def button_5_hover(e):
    button_5.config(image=button_image_hover_5)
def button_5_leave(e):
    button_5.config(image=button_image_5)

button_5.bind('<Enter>', button_5_hover)
button_5.bind('<Leave>', button_5_leave)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [window.destroy(), print("Window Destroyed")],
    relief="flat"
)
button_6.place(x=950.0, y=658.0, width=330.0, height=142.0)

button_image_hover_6 = PhotoImage(file=relative_to_assets("button_hover_6.png"))

def button_6_hover(e):
    button_6.config(image=button_image_hover_6)
def button_6_leave(e):
    button_6.config(image=button_image_6)

button_6.bind('<Enter>', button_6_hover)
button_6.bind('<Leave>', button_6_leave)

# Time with shadow
time_text_shadow2 = canvas.create_text(
    59.0,
    672.0,
    anchor="nw",
    text="",
    fill="#C0C0C0",
    font=("Times New Roman", 49 * -1)
)
time_text_shadow1 = canvas.create_text(
    58.0,
    671.0,
    anchor="nw",
    text="",
    fill="#A0A0A0",
    font=("Times New Roman", 49 * -1)  
)
time_text = canvas.create_text(
    57.0,
    670.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Times New Roman", 49 * -1)
)

# Day with shadow
day_text_shadow2 = canvas.create_text(
    499.0,
    672.0,
    anchor="nw",
    text="",
    fill="#C0C0C0",
    font=("Times New Roman", 49 * -1)  
)
day_text_shadow1 = canvas.create_text(
    498.0,
    671.0,
    anchor="nw",
    text="",
    fill="#A0A0A0",
    font=("Times New Roman", 49 * -1)
)
day_text = canvas.create_text(
    497.0,
    670.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Times New Roman", 49 * -1)
)

# Date with shadow
date_text_shadow2 = canvas.create_text(
    747.552734375,
    724.0,  
    anchor="nw",
    text="",
    fill="#C0C0C0",
    font=("Times New Roman", 22 * -1) 
)
date_text_shadow1 = canvas.create_text(
    746.552734375,
    723.0,  
    anchor="nw",
    text="",
    fill="#A0A0A0",
    font=("Times New Roman", 22 * -1)
)
date_text = canvas.create_text(
    745.552734375,
    722.0,  
    anchor="nw",
    text="",
    fill="#000000",
    font=("Times New Roman", 22 * -1)
)

def update_datetime():
    # Get current date and time
    current = datetime.now()
    
    # Update time (24-hour format)
    time_string = f"TIME: {current.strftime('%H:%M:%S')}"
    canvas.itemconfig(time_text_shadow2, text=time_string)
    canvas.itemconfig(time_text_shadow1, text=time_string)
    canvas.itemconfig(time_text, text=time_string)
    
    # Update day
    day_string = f"DATE: {current.strftime('%A').upper()}"
    canvas.itemconfig(day_text_shadow2, text=day_string)
    canvas.itemconfig(day_text_shadow1, text=day_string)
    canvas.itemconfig(day_text, text=day_string)
    
    # Update date
    date_string = current.strftime('%m/%d/%Y')
    canvas.itemconfig(date_text_shadow2, text=date_string)
    canvas.itemconfig(date_text_shadow1, text=date_string)
    canvas.itemconfig(date_text, text=date_string)
    
    # Schedule the next update
    window.after(1000, update_datetime)

update_datetime()

# STI College text with shadow
canvas.create_text(
    582.0,
    95.0,
    anchor="center",
    text="STI College Global City",
    fill="#C0C0C0",
    font=("Fredoka One", 55 * -1)
)
canvas.create_text(
    581.0,
    97.0,
    anchor="center",
    text="STI College Global City",
    fill="#A0A0A0",
    font=("Fredoka One", 55 * -1)
)
canvas.create_text( #main
    580.0,
    95.0,
    anchor="center",
    text="STI College Global City",
    fill="#2C3167",
    font=("Fredoka One", 55 * -1)
)


tree.bind('<Button-1>', show_full_concern)  # Show full concern on click
tree.bind('<Double-1>', copy_student_id)  # Copy student ID on double click
window.resizable(False, False)
window.mainloop()
