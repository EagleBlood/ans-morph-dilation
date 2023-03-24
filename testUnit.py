import tkinter as tk
from PIL import Image, ImageTk
import os

# function to update the displayed mask image
def update_mask_image(*args):
    mask_name = selected_mask_var.get()
    mask_filename = mask_filenames[mask_name]
    mask_path = os.path.join(program_dir, mask_filename)
    mask_image = Image.open(mask_path)
    mask_image_tk = ImageTk.PhotoImage(mask_image)
    mask_canvas.itemconfig(mask_canvas_image, image=mask_image_tk)
    mask_canvas.image = mask_image_tk  # store a reference to the image to prevent garbage collection

window = tk.Tk()
window.title("Mask Viewer")

program_dir = os.path.dirname(os.path.abspath(__file__))

# dictionary mapping mask names to their file paths
mask_filenames = {
    "Golay Mask C ": "mask/maskC.png",
    "Golay Mask D": "mask/maskD.png",
    "Golay Mask E": "mask/maskE.png",
}

# create a list of mask names
mask_names = list(mask_filenames.keys())

# create a canvas for displaying the mask image
mask_canvas = tk.Canvas(window, width=400, height=400)
mask_canvas.pack()

# create a placeholder image
placeholder_image = Image.new("RGB", (400, 400), "black")
placeholder_image_tk = ImageTk.PhotoImage(placeholder_image)

# create an image item on the canvas for the placeholder image
mask_canvas_image = mask_canvas.create_image(0, 0, anchor="nw", image=placeholder_image_tk)

# create a dropdown menu for selecting the mask
selected_mask_var = tk.StringVar()
selected_mask_var.set(mask_names[0])  # set the default mask to the first in the list
mask_dropdown = tk.OptionMenu(window, selected_mask_var, *mask_names)
mask_dropdown.pack()

# bind the update_mask_image function to the StringVar's trace method
selected_mask_var.trace("w", update_mask_image)

# call the update_mask_image function initially to display the default mask image
update_mask_image()

window.mainloop()
