from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, font
from input_details import open_input_details_window  # Import the function to open input details window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\queue_typeAssets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_queue_type_window():
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
    canvas.place(x=0, y=0)

    # Load and display images
    try:
        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        canvas.create_image(640.0, 400.0, image=image_image_1)
    except Exception as e:
        print(f"Error loading image_1.png: {e}")

    try:
        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(113.0, 75.0, image=image_image_2)
    except Exception as e:
        print(f"Error loading image_2.png: {e}")

    # Setting the font for the buttons
    button_font = font.Font(family="Fredoka One", size=20)

    # Function to handle Priority selection
    def select_priority():
        queue_type = "PO"  # Set queue type as Priority
        print(f"Selected queue type: {queue_type}")  # Debugging output
        window.destroy()  # Close the queue type window
        open_input_details_window(queue_type)

    # Function to handle Non-Priority selection
    def select_non_priority():
        queue_type = "RO"  # Set queue type as Non-Priority
        print(f"Selected queue type: {queue_type}")  # Debugging output
        window.destroy()  # Close the queue type window
        open_input_details_window(queue_type)
    
    def select_returnee():
        queue_type = "RE"  # Set queue type as Returnee
        print(f"Selected queue type: {queue_type}")  # Debugging output
        window.destroy()
        open_input_details_window(queue_type)

    # Button for Priority
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=select_non_priority,  # Updated command
        relief="flat",
        font=button_font  # Set font for the button
    )
    button_1.place(
        x=207.0,
        y=496.0,
        width=863.0,
        height=135.0
    )

    # Button for Non-Priority
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=select_priority,  # Updated command
        relief="flat",
        font=button_font  # Set font for the button
    )
    button_2.place(
        x=207.0,
        y=231.0,
        width=863.0,
        height=150.0
    )

    # Title text
    title_font = font.Font(family="Fredoka One", size=40, weight="bold")
    canvas.create_text(
        640,  # X position
        100,  # Y position
        text="Select Queue Type",
        fill="#2C3167",  # Text color
        font=title_font,  # Title font
        anchor="center"  # Center the text
    )

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    open_queue_type_window()
