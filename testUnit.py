import tkinter as tk
import cv2
from PIL import ImageTk, Image

# Load the images for each dilation step
step1 = cv2.imread('step1.png')
step2 = cv2.imread('step2.png')
step3 = cv2.imread('step3.png')
step4 = cv2.imread('step4.png')

# Initialize Tkinter
root = tk.Tk()

# Load the original image
img = cv2.imread('original.png')

# Calculate the canvas size
canvas_width = img.shape[1] + 2 * 20
canvas_height = img.shape[0] + 4 * 20 + 40

# Create a canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Create a table to display the morphological dilation steps
table_size = (img.shape[1]//1.3, img.shape[0]//1.3)
table_margin_size = 20
table_start_x = 20
table_start_y = 3 * table_margin_size + 40

for i in range(4):
    row = i // 2
    col = i % 2
    step_img = [step1, step2, step3, step4][i]
    table_x = table_start_x + col * (table_size[0] + table_margin_size)
    table_y = table_start_y + row * (table_size[1] + table_margin_size)

    # Add a label with the step number
    canvas.create_text(table_x + table_size[0] / 2, table_y - 10, text=f'Step {i + 1}', font=('Arial', 12))

    # Convert the image to a format that Tkinter can display
    img_tk = ImageTk.PhotoImage(Image.fromarray(step_img))

    # Add the image to the canvas with the specified offset
    canvas.create_image(table_x, table_y, image=img_tk, anchor='nw')

# Convert the original image to a format that Tkinter can display
img_tk = ImageTk.PhotoImage(Image.fromarray(img))

# Add the image to the canvas with the specified offset
canvas.create_image(20, 20, image=img_tk, anchor='nw')

# Start the Tkinter event loop
root.mainloop()