from PIL import Image, ImageTk
import numpy as np
import cv2
from tkinter import Tk, Canvas

margin_size = 70
white_color = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX

# load the input image
img = cv2.imread(r'ertka.bmp', 0)

# create a window and canvas to display the images
root = Tk()
root.title('Morphological Dilation Steps')
canvas = Canvas(root, width=3*img.shape[1] + 4*margin_size, height=2*img.shape[0] + 3*margin_size)
canvas.pack()

# set the images and labels
canvas.create_text(margin_size+10, margin_size-10, text='Input Image', font=font, anchor='nw')
img_pil = Image.fromarray(img)
img_tk = ImageTk.PhotoImage(img_pil)
canvas.img_tk = img_tk  # Store a reference to the PhotoImage object
canvas.create_image(margin_size, margin_size, image=img_tk, anchor='nw')

# ... repeat for other images ...

root.mainloop()