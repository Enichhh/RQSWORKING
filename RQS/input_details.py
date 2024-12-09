from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from backend import QueueSystem  # Import the QueueSystem class
from queue_number import show_queue_number

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\input_detailsAssets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_input_details_window(queue_type):
    window = Tk()
    window.title("Registrar Queueing System RQS")
    # Get the screen width and height
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

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=800,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Background images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(640.0, 400.0, image=image_image_1, anchor="center")

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(113.0, 75.0, image=image_image_2)

    # Input Details
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(644.0, 289.5, image=entry_image_1)
    entry_name = Entry(
        bd=2,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        highlightcolor="#2C3167",
        highlightbackground="#808080",
        font=("Times New Roman", 16),
        relief="solid"
    )
    entry_name.place(x=218.0, y=267.0, width=852.0, height=53.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(642.0, 418.5, image=entry_image_2)
    entry_student_id = Entry(
        bd=2,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        highlightcolor="#2C3167",
        highlightbackground="#808080",
        font=("Times New Roman", 16),
        relief="solid"
    )
    entry_student_id.place(x=216.0, y=396.0, width=852.0, height=53.0)

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    canvas.create_image(642.0, 546.5, image=entry_image_3)
    entry_concern = Entry(
        bd=2,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        highlightcolor="#2C3167",
        highlightbackground="#808080",
        font=("Times New Roman", 16),
        relief="solid"
    )
    entry_concern.place(x=216.0, y=524.0, width=852.0, height=53.0)

    # Shadow text
    canvas.create_text(
        640,
        168.0,
        anchor="center",
        text="Please Enter the Required Details",
        fill="#CCCCCC",
        font=("Fredoka One", 35 * -1,)
    )

    # Main text
    canvas.create_text(
        640,
        165.0,
        anchor="center",
        text="Please Enter the Required Details",
        fill="#000000",
        font=("Fredoka One", 35 * -1,) 
    )

    # Student Name with shadow
    canvas.create_text(
        217.0,
        234.0,
        anchor="nw",
        text="Student Surname:",
        fill="#C0C0C0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        216.0,
        233.0,
        anchor="nw",
        text="Student Surname:",
        fill="#A0A0A0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        215.0,
        232.0,
        anchor="nw",
        text="Student Surname:",
        fill="#2C3167",
        font=("Times New Roman", 32 * -1)
    )

    # Student No with shadow
    canvas.create_text(
        217.0,
        361.0,
        anchor="nw",
        text="Student No:",
        fill="#C0C0C0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        216.0,
        360.0,
        anchor="nw",
        text="Student No:",
        fill="#A0A0A0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        215.0,
        359.0,
        anchor="nw",
        text="Student No:",
        fill="#2C3167",
        font=("Times New Roman", 32 * -1)
    )

    # List of Concerns with shadow
    canvas.create_text(
        217.0,
        491.0,
        anchor="nw",
        text="Concern/s",
        fill="#C0C0C0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        216.0,
        490.0,
        anchor="nw",
        text="Concern/s",
        fill="#A0A0A0",
        font=("Times New Roman", 32 * -1)
    )
    canvas.create_text(
        215.0,
        489.0,
        anchor="nw",
        text="Concern/s",
        fill="#2C3167",
        font=("Times New Roman", 32 * -1)
    )

    # STI College Text 
    canvas.create_text(
        638,
        84.0,
        anchor="center",
        text="STI College Global City",
        fill="#606060",
        font=("Fredoka One", 55 * -1)
    )
    canvas.create_text(
        637,
        82.0,
        anchor="center",
        text="STI College Global City",
        fill="#404040",
        font=("Fredoka One", 55 * -1)
    )
    canvas.create_text(
        636,
        82.0,
        anchor="center",
        text="STI College Global City",
        fill="#2C3167",
        font=("Fredoka One", 55 * -1)
    )

    # Submit Button
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: submit_user_details(entry_name.get(), entry_student_id.get(), entry_concern.get(), queue_type, window),
        relief="flat"
    )
    button_1.place(
        x=835.5,
        y=642.0,
        width=247.0,
        height=112.0
    )

    button_image_hover_1 = PhotoImage(
        file=relative_to_assets("button_hover_1.png")
    )

    def button_1_hover(e):
        button_1.config(
            image=button_image_hover_1
        )

    def button_1_leave(e):
        button_1.config(
            image=button_image_1
        )

    button_1.bind('<Enter>', button_1_hover)
    button_1.bind('<Leave>', button_1_leave)

    window.resizable(False, False)
    window.mainloop()

def submit_user_details(name, student_id, concern, queue_type, window):
    # Create an instance of QueueSystem
    queue_system = QueueSystem()

    try:
        # Validate user input
        is_valid, message = queue_system.validate_user_input(name, student_id, concern)
        if not is_valid:
            messagebox.showerror("Input Error", message)
            return  # Stop further processing if validation fails

        # Save user details to the database
        user_data = queue_system.save_user_details(name, student_id, concern, queue_type)

        # Close the current input details window
        window.destroy()  # This will close the current window
        show_queue_number(user_data['queue_number'])
    finally:
        queue_system.close()  # Ensure the connection is ⬤
