from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, font
import subprocess
import threading 
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\queue_numberAssets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_text_with_outline(canvas, x, y, text, font, fill, outline, outline_offset=2):
    # Draw the outline by creating the text multiple times with the outline color
    for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset),
                   (-outline_offset, -outline_offset), (-outline_offset, outline_offset),
                   (outline_offset, -outline_offset), (outline_offset, outline_offset)]:
        canvas.create_text(x + dx, y + dy, anchor="nw", text=text, fill=outline, font=font)
    # Draw the main text
    canvas.create_text(x, y, anchor="nw", text=text, fill=fill, font=font)

def run_start_script():
    """Function to run start.py in a separate thread."""
    subprocess.run(["python", "start.py"])

def countdown(seconds, window):
    if seconds > 0:
        # Call countdown again after 1000 milliseconds (1 second)
        window.after(1000, countdown, seconds - 1, window)
    else:
        window.destroy()
        # Start a new thread to run start.py
        threading.Thread(target=run_start_script).start()

def show_queue_number(queue_number):
    """Display the queue number on the screen."""
    
    window = Tk()
    window.title("Registrar Queueing System RQS")

    # Load the icon image and keep a reference to it
    icon_path = relative_to_assets("image_2.png")
    icon = PhotoImage(file=icon_path)  # Load the icon image
    window.iconphoto(True, icon)  # Set the window icon

    window.configure(bg="#FFFFFF")
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

    # Load and keep references for images used in canvas
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(640.0, 400.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(113.0, 75.0, image=image_image_2)

    canvas.create_rectangle(
        377.0,
        221.0,
        902.0,
        747.2867431640625,
        fill="#FFFFFF",
        outline=""
    )
    setting_font = font.Font(family="Fredoka One", size=35, weight="bold")

    # Main title
    create_text_with_outline(
        canvas,
        438,
        50.0,
        text="STI College Global City",
        font=("Fredoka One", 48 * -1),
        fill="#2C3167",
        outline="#606060",  # Outline color
        outline_offset=2  # Outline thickness
    )

    # Display the queue number
    create_text_with_outline(
        canvas,
        250.0,  # X-Axis
        125.0,  # Y-Axis
        text="YOUR QUEUE NUMBER:",
        font=setting_font,
        fill="#000000",  # Main text color
        outline="#FFD700",  # Outline color
        outline_offset=0  # Outline thickness
    )
    canvas.create_text(
        500.0,  # X-Axis
        485.375,  # Y-Axis
        text=" No.",
        font=setting_font,
        fill="#2C3167",  # Main text color
    )

    # Display the actual queue number
    canvas.create_text(
        700,
        485.375,
        anchor="center",
        text=str(queue_number),  # Display the queue number here
        fill="#2C3167",
        font=("Fredoka One", 100)
    )

    # Start the countdown from 10 seconds without displaying it
    countdown(10, window)

    window.resizable(False, False)
    window.mainloop()