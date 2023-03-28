from tkinter import *
from PIL import Image, ImageTk

def on_slider_move(value):
    print(f"Slider value: {value}")

def setPhotoOnCanvas(canvas, img, x, y, photo_list):
    photo = ImageTk.PhotoImage(img)
    photo_list.append(photo)
    canvas.create_image(x, y, image=photo, anchor=NW)
    
def create_slider(parent):
    slider_frame = Frame(parent)
    slider_frame.pack()
    
    slider_label = Label(slider_frame, text="Slider")
    slider_label.pack(side=LEFT)
    
    slider = Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, command=on_slider_move)
    slider.pack(side=LEFT)
    
    return slider, slider_frame

root = Tk()
root.geometry("800x600")
root.title("Slider Demo")

img = Image.open("ertka.bmp")
mask_img = Image.open("ertka.bmp").convert("L")
photo_list = []

canvas = Canvas(root, width=800, height=600)
canvas.pack()

margin_size = 70

setPhotoOnCanvas(canvas, img, margin_size, margin_size, photo_list)

slider, slider_frame = create_slider(root)
slider_window = canvas.create_window(margin_size, margin_size + img.height + margin_size//2, anchor=NW, window=slider_frame)

root.mainloop()