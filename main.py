from PIL import Image, ImageTk
import numpy as np
import cv2
from tkinter import SINGLE, Button, OptionMenu, Scale, StringVar, Tk, Canvas, HORIZONTAL, Frame, Label, LEFT, filedialog
import os
import masks as msk

#Global variables
program_dir = os.path.dirname(os.path.abspath(__file__))

margin_size = 70
background_color = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
photo_list = []
mask_filenames = {
    "Default Mask": "mask/Default.png",
    "Golay Mask C ": "mask/maskC.png",
    "Golay Mask E": "mask/maskE.png",
    "Golay Mask D": "mask/maskD.png",
}
mask_names = list(mask_filenames.keys())


#Mask functions
def thick(img):
    imgA = np.array(img)
    
    img1 = np.array(imgA,np.uint8)
    img2 = np.array(imgA,np.uint8)
    img3 = np.array(imgA,np.uint8)
    img4 = np.array(imgA,np.uint8)

    masked1 = np.zeros((3,3), np.uint8)
    masked2 = np.zeros((3,3), np.uint8)
    masked3 = np.zeros((3,3), np.uint8)
    masked4 = np.zeros((3,3), np.uint8)

    mask = msk.defaultMask()
    
    for y in range(0,img.shape[0]-2):
        for x in range(0,img.shape[1]-2):
            masked1 = np.array(imgA[y:y+3,x:x+3])
            masked2 = np.array(masked1)
            masked3 = np.array(masked1)
            masked4 = np.array(masked1)

            masked1 *= mask
            mask = np.rot90(mask)
            masked4 *= mask
            mask = np.rot90(mask)
            masked3 *= mask
            mask = np.rot90(mask)
            masked2 *= mask
            mask = np.rot90(mask)

            if(masked1[0,0]==masked1[0,1]):
                img1[y,x] = 255
            if(masked1[0,0]==masked1[0,1]):
                img1[y,x+2] = 255

            if(masked2[0,2]==masked2[1,2]):
                img2[y,x+2] = 255
            if(masked2[2,2]==masked2[1,2]):
                img2[y+2,x+2] = 255

            if(masked3[2,2]==masked3[2,1]):
                img3[y+2,x+2] = 255
            if(masked3[2,0]==masked3[2,1]):
                img3[y+2,x] = 255

            if(masked4[0,0]==masked4[1,0]):
                img4[y,x] = 255
            if(masked4[2,0]==masked4[1,0]):
                img4[y+2,x] = 255
    
    for y in range(0,img.shape[0]):
        for x in range(0,img.shape[1]):
            if (img1[y,x]==0):
                img1[y,x] = 255
            else:
                img1[y,x]  = 0
            if img2[y,x] == 0:
                img2[y,x] = 255
            else:
                img2[y,x] = 0
            if img3[y,x] == 0:
                img3[y,x] = 255
            else:
                img3[y,x]  = 0
            if img4[y,x] == 0:
                img4[y,x] = 255
            else:
                img4[y,x]  = 0

    imgA += img1 + img2 + img3 + img4

    return imgA, img1, img2, img3, img4

def loadImg(path):
    img = cv2.imread(path, 0)
    return img

def setPhotoOnCanvas(canvas, img, x, y, photo_list):
    img_pil = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(img_pil)
    photo_list.append(img_tk)
    img_del = canvas.create_image(x, y, image=photo_list[-1], anchor='nw')

def update_mask_image(*args):
    mask_name = selected_mask_var.get()
    mask_img = loadImg(os.path.join(program_dir, mask_filenames[mask_name]))
    setPhotoOnCanvas(canvas, mask_img, margin_size*4 + img.shape[0] + 50, margin_size-20, photo_list)

def update_main_image():
    update_image = loadImg(selected_file_path)
    update_image = cv2.resize(update_image, (228, 164))
    setPhotoOnCanvas(canvas, update_image, margin_size, margin_size-30, photo_list)

def create_slider(parent):
    slider_frame = Frame(parent)
    slider_frame.pack()
    
    slider = Scale(slider_frame, from_=1, to=10, length=200, orient=HORIZONTAL, label="Iterations", command=on_slider_move)
    slider.pack(side=LEFT)
    
    return slider, slider_frame

def on_slider_move(value):
    dilation, step1, step2, step3, step4 = thicIter(thick, value, img)
    print(f"Slider value: {value}")
    return value

def thicIter(fun, iter, img):
    imgTab = fun(img)
    for a in range(iter-1):
        imgTab = fun(imgTab[0])
    return imgTab

def open_file_dialog():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select a file",
        filetypes=(("Image files", "*.bmp;*.jpg;*.png"), ("All files", "*.*")),
    )
    global selected_file_path
    selected_file_path = file_path

    update_main_image()

def save_file():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".jpg", filetypes=[(".jpg", "*.jpg"), ("All Files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, dilation)


# Load the input image
img = cv2.imread(r'ertka.bmp', 0)
img = cv2.resize(img, (228, 164))


# Apply the morphological dilation
dilation, step1, step2, step3, step4 = thick(img)


# Create a window and canvas to display the images
root = Tk()
root.title('Morphological Dilation Steps')
canvas = Canvas(root, width=3*img.shape[1] + 4*margin_size, height=2*img.shape[0] + 3*margin_size)
canvas.pack()


# Add the mask images
selected_mask_var = StringVar()
selected_mask_var.set(mask_names[0])  # set the default mask to the first in the list
selected_mask_var.trace("w", update_mask_image)


canvas.create_text(margin_size+img.shape[1]/2, margin_size-40, text='Input Image', font=font)
setPhotoOnCanvas(canvas, img, margin_size, margin_size-20, photo_list)

# Create a table to display the morphological dilation steps
table_size = (img.shape[1]//1.3, img.shape[0]//1.3)
table_margin_size = 20
table_start_x = margin_size
table_start_y = margin_size*3+40
for i in range(4):
    row = i // 2
    col = i % 2
    step_img = [step1, step2, step3, step4][i]
    table_x = table_start_x + col * (table_size[0] + table_margin_size) 
    table_y = table_start_y + row * (table_size[1] + table_margin_size)
    canvas.create_text(table_x + table_size[0]/2, table_y-10, text=f'Step {i+1}', font=font)
    setPhotoOnCanvas(canvas, cv2.resize(step_img, (int(table_size[0]), int(table_size[1]))), table_x, table_y, photo_list)

# Add result image next to the table
canvas.create_text(margin_size*2 + table_size[0]*2 +  img.shape[1]/2, margin_size*2+img.shape[0]-10, text='Result', font=font)
setPhotoOnCanvas(canvas, dilation, margin_size*2 + table_size[0]*2, margin_size*2+img.shape[0], photo_list)

# Upade the main images
selected_file_path = ""
selected_image_var = StringVar()
selected_image_var.set(selected_file_path)
selected_image_var.trace("w", update_main_image)

#Buttons
update_button = Button(root, text='Update Images')
load_button = Button(root, text='Load Image', command=open_file_dialog)
mask_dropdown = OptionMenu(root, selected_mask_var, *mask_names)
save_button = Button(root, text='Save Image', command=save_file)
change_lang_button = Button(root, text='Change language')
slider, slider_frame = create_slider(root)


# Place the buttons on canvas
update_button_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size, window=update_button)
load_button_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+40, window=load_button)
mask_dropdown_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+80, window=mask_dropdown)
change_lang_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+120, window=change_lang_button)
save_button_window = canvas.create_window(margin_size*2 + table_size[0]*2 +  img.shape[1]/2, margin_size*2+img.shape[0]+table_margin_size+table_size[1]+50, window=save_button)
slider_window = canvas.create_window(margin_size*2 + img.shape[1]*2, margin_size+160, window=slider_frame)



# Display default mask image
update_mask_image()
#update_main_image()


root.mainloop()
