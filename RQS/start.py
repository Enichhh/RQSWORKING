from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, font
from queue_type import open_queue_type_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\RQS\assets\startAssets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
window.configure(bg="#FAF304")

canvas = Canvas(
    window,
    bg="#FAF304",
    height=800,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(640.0, 400.0, image=image_image_1)# x, y axis

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(625.0, 150.0, image=image_image_2) # X, Y 

setting_font = font.Font(family="Fredoka One", size=40, weight="normal")  # Font setting variable

def create_text_with_outline(canvas, x, y, text, font, fill, outline, outline_offset=2):
    for dx, dy in [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset),
                   (-outline_offset, -outline_offset), (-outline_offset, outline_offset),
                   (outline_offset, -outline_offset), (outline_offset, outline_offset)]:
        canvas.create_text(x + dx, y + dy, anchor="nw", text=text, fill=outline, font=font)
    canvas.create_text(x, y, anchor="nw", text=text, fill=fill, font=font)

# Generate text with outline
create_text_with_outline(
    canvas,
    398.0,  # X-Axis
    275.0,  # Y-Axis
    text="Welcome to",
    font=setting_font,
    fill="#FFD700",  # Main text color
    outline="#000000",  # Outline color
    outline_offset=2  # Outline thickness
)

create_text_with_outline(
    canvas,
    215.0,  # X-Axis
    400.0,  # Y-Axis
    text="STI College Global City",
    font=setting_font,
    fill="#FFD700",  # Main text color
    outline="#000000",  # Outline color
    outline_offset=2  # Outline thickness
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [window.destroy(), open_queue_type_window()],  # Close current window and open the next
    relief="flat"
)
button_1.place(
    x=0.0,
    y=556.0,
    width=1280.0,
    height=172.0
)

window.resizable(False, False)
window.mainloop()