from PIL import Image, ImageTk
import numpy as np
import cv2
from tkinter import SINGLE, Button, OptionMenu, Scale, StringVar, Tk, Canvas, HORIZONTAL, Frame, Label, LEFT, filedialog
import os
import masks as msk

#Global variables
program_dir = os.path.dirname(os.path.abspath(__file__))
global img, dylation
margin_size = 70
background_color = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
photo_list = []
selected_file_path = ""

#Image processing variables
threshold_value = 127
max_value = 255

mask_filenames = {
    "Default Mask": "mask/Default.png",
    "Golay Mask C": "mask/maskC.png",    
    "Golay Mask D": "mask/maskD.png",
    "Golay Mask E": "mask/maskE.png",
    "Golay Mask L": "mask/maskL.png",
    "Golay Mask M": "mask/maskM.png",
    "Golay Mask R": "mask/maskR.png",
    "Golay Mask Skiz": "mask/goleySkiz.png",
    "Skiz": "mask/skiz.png",
    "Mask Canv": "mask/maskCanv.png",
}

dictionary = {
    "Input Image": "Obraz wejściowy",
    "Step 1": "Krok 1",
    "Step 2": "Krok 2",
    "Step 3": "Krok 3",
    "Step 4": "Krok 4",
    "Result Image": "Obraz Wynikowy",
    "Execute thickening": "Wykonaj pogrubienie",
    "Load Image": "Wczytaj obraz",
    "Save Image": "Zapisz obraz",
    "PL": "EN",
    "Load result to Input Image": "Wczytaj do obrazu wejściowego",
}

mask_names = list(mask_filenames.keys())

#Garbage collector prevention
image_ref = None
mask_ref = None
img_res_ref = None
img_step1_ref = None
img_step2_ref = None
img_step3_ref = None
img_step4_ref = None
lang = "en"
text_1, text_2, text_3, text_4, text_5, text_6 = None, None, None, None, None, None
selected_mask = msk.defaultMask()


#Mask functions
def defaultThickening(img,iter):
    
    global selected_mask
    for y in range(0,img.shape[0]-2):
        for x in range(0,img.shape[1]-2):
            if img[y][x] != 0:
                img[y][x] = 255



    imgA = np.array(img,np.uint8)

    

    
    if len(selected_mask) != 3:
        
        for a in range(iter):
            imgTmp = np.array(imgA,np.uint8)
            for se in selected_mask:           
                for y in range(0,img.shape[0]-2):
                    for x in range(0,img.shape[1]-2):
                        masked = imgA[y:y+3,x:x+3]
                        changeImg = True
                        for i in range(3):
                            for j in range(3):
                                if  (se[i][j] == 0 and masked[i][j] != 0) or (se[i][j] == 255 and  masked[i][j] == 0) :
                                    changeImg = False
                        if changeImg == True:
                            imgTmp[y+1][x+1] = 255
            imgA = imgTmp        
    else:
        se = selected_mask
        for a in range(iter):
            imgTmp = np.array(imgA,np.uint8)
            for y in range(0,img.shape[0]-2):
                for x in range(0,img.shape[1]-2):
                    masked = imgA[y:y+3,x:x+3]
                    changeImg = True
                    for i in range(3):
                        for j in range(3):
                            if  (se[i][j] == 0 and masked[i][j] != 0) or (se[i][j] == 255 and  masked[i][j] == 0) :
                                changeImg = False
                    if changeImg == True:
                        imgTmp[y+1][x+1] = 255
            imgA = imgTmp 
            
    
    imgDiff = np.subtract(imgA, img)        
            

    
    return imgA, imgDiff, imgDiff, imgDiff, imgDiff


# GUI functions
def setPhotoOnCanvas(canvas, img, x, y, photo_list):
    # Żeby można było się dostać do modyfikacji obrazu trzeba podać jako argument id obrazu które zwraca funkcja
    img_pil = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(img_pil)
    photo_list.append(img_tk)
    img_return = canvas.create_image(x, y, image=photo_list[-1], anchor='nw')
    return img_return

def replace_image_with_color(image_path):
    img = Image.open(image_path)
    width, height = img.size
    data = img.load()
    for x in range(width):
        for y in range(height):
            data[x, y] = (255, 255, 255)  # replace the pixel with F0F0F0 color
    img.save(image_path)
    

def update_main_image(canvas, input_img_var, selected_file_path):
    global image_ref # To prevent garbage collection
    global img

    

    update_image = load_img(selected_file_path)
    update_image = cv2.resize(update_image, (228, 164))

    for y in range(0,update_image.shape[0]-2):
        for x in range(0,update_image.shape[1]-2):
            if update_image[y][x] != 0:
                update_image[y][x] = 255


    img = update_image
    update_image = Image.fromarray(update_image)
    update_image = ImageTk.PhotoImage(update_image)

    canvas.itemconfig(input_img_var, image=update_image)
    image_ref = update_image
    
    return update_image

def update_main_image_from_dilation(canvas, input_img_var, result_image):
    global image_ref # To prevent garbage collection
    global img

    update_image = result_image

    img = update_image
    update_image = Image.fromarray(update_image)
    update_image = ImageTk.PhotoImage(update_image)

    canvas.itemconfig(input_img_var, image=update_image)
    image_ref = update_image
    
    return update_image

def update_result_images(canvas, img_result_var, img):
    global img_res_ref # To prevent garbage collection

    resized_img = cv2.resize(img, (228, 164))
    img_pil = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.itemconfig(img_result_var, image=img_tk)
    img_res_ref = img_tk
    canvas.itemconfigure(img_result_var, state="normal")

def update_step1_image(canvas, img_result_var, img):
    global img_step1_ref # To prevent garbage collection

    resized_img = cv2.resize(img, (table_size[0], table_size[1]))
    img_pil = Image.fromarray(resized_img)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.itemconfig(img_result_var, image=img_tk)
    img_step1_ref = img_tk
    canvas.itemconfigure(img_result_var, state="normal")

def update_step2_image(canvas, img_result_var, img):
    global img_step2_ref # To prevent garbage collection

    resized_img = cv2.resize(img, (table_size[0], table_size[1]))
    img_pil = Image.fromarray(resized_img)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.itemconfig(img_result_var, image=img_tk)
    img_step2_ref = img_tk
    canvas.itemconfigure(img_result_var, state="normal")

def update_step3_image(canvas, img_result_var, img):
    global img_step3_ref # To prevent garbage collection

    resized_img = cv2.resize(img, (table_size[0], table_size[1]))
    img_pil = Image.fromarray(resized_img)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.itemconfig(img_result_var, image=img_tk)
    img_step3_ref = img_tk
    canvas.itemconfigure(img_result_var, state="normal")

def update_step4_image(canvas, img_result_var, img):
    global img_step4_ref # To prevent garbage collection

    resized_img = cv2.resize(img, (table_size[0], table_size[1]))
    img_pil = Image.fromarray(resized_img)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.itemconfig(img_result_var, image=img_tk)
    img_step4_ref = img_tk
    canvas.itemconfigure(img_result_var, state="normal")

def on_slider_move(value):
    print(f"Slider value: {value}")
    return value

def update_mask_image(*args):
    global mask_ref # To prevent garbage collection

    mask_name = selected_mask_var.get()
    mask_img = load_img(os.path.join(program_dir, mask_filenames[mask_name]))
    mask_img = Image.fromarray(mask_img)
    mask_img = mask_img.resize((300, 150), Image.LANCZOS)

    mask_img = ImageTk.PhotoImage(mask_img)

    mask_img_var = canvas.create_image(margin_size*4 + img.shape[0] + 50, margin_size-20, image=mask_img, anchor='nw')
    mask_ref = mask_img

def create_slider(parent):
    slider_frame = Frame(parent)
    slider_frame.pack()
    
    slider = Scale(slider_frame, from_=1, to=10, length=200, orient=HORIZONTAL, label="Iter", command=on_slider_move)
    slider.pack(side=LEFT)
    
    return slider, slider_frame


# File functions
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        initialdir=os.path.join(os.getcwd(), "img"),
        title="Select a file",
        filetypes=(("Image files", "*.bmp;*.jpg;*.png"), ("All files", "*.*")),
    )
    global selected_file_path
    selected_file_path = file_path

    if file_path:
        update_main_image(canvas, input_img_var, selected_file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".jpg", filetypes=[(".jpg", "*.jpg"), ("All Files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, dilation)

def load_img(path):
    binary_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    ret, binary_img = cv2.threshold(binary_img, threshold_value, max_value, cv2.THRESH_BINARY)

    img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

    canvas.itemconfigure(step1_img_var, state="hidden")
    canvas.itemconfigure(step2_img_var, state="hidden")
    canvas.itemconfigure(step3_img_var, state="hidden")
    canvas.itemconfigure(step4_img_var, state="hidden")
    canvas.itemconfigure(img_result_var, state="hidden")

    for y in range(0,img.shape[0]-2):
        for x in range(0,img.shape[1]-2):
            if binary_img[y][x] != 0:
                binary_img[y][x] = 255

    return binary_img

# Morphological functions
def thic_iter(fun, iter, img):
    imgTab = fun(img)
    for a in range(iter-1):
        imgTab = fun(imgTab[0])
    return imgTab

def execute_dilation():
    global dilation
    dilation, step_iter_1, step_iter_2, step_iter_3, step_iter_4 = defaultThickening(img, slider.get())
    update_step1_image(canvas, step1_img_var, step_iter_1)
    update_step2_image(canvas, step2_img_var, step_iter_2)
    update_step3_image(canvas, step3_img_var, step_iter_3)
    update_step4_image(canvas, step4_img_var, step_iter_4)
    update_result_images(canvas, img_result_var, dilation)

def load_to_input():
    if img_result_var is not "hidden":
        update_main_image_from_dilation(canvas, input_img_var, dilation)

        canvas.itemconfigure(step1_img_var, state="hidden")
        canvas.itemconfigure(step2_img_var, state="hidden")
        canvas.itemconfigure(step3_img_var, state="hidden")
        canvas.itemconfigure(step4_img_var, state="hidden")
        canvas.itemconfigure(img_result_var, state="hidden")

# Language functions
def translate_text(text, lang):
    if lang == "en":
        return text
    elif lang == "pl":
        if text in dictionary:
            return dictionary[text]
        else:
            return text
    else:
        return text
    
def change_language():
    global lang
    if lang == "en":
        lang = "pl"
    else:
        lang = "en"
    update_text()
    update_button_text(update_button, "Execute thickening")
    update_button_text(load_button, "Load Image")
    update_button_text(save_button, "Save Image")
    update_button_text(change_lang_button, "PL")
    update_button_text(result_to_input_button, "Load result to Input Image")

def update_button_text(button, button_text):
    if button_text in dictionary:
        translated_text = translate_text(button_text, lang)
        button.config(text=translated_text)
    else:
        button.config(text=button_text)

def update_text():
    global text_1, text_2, text_3, text_4, text_5, text_6

    canvas.delete(text_1, text_2, text_3, text_4, text_5, text_6)
    text_1 = canvas.create_text(margin_size+img.shape[1]/2, margin_size-40, text=translate_text("Input Image", lang), font=font)
    text_2 = canvas.create_text(step1_pos[0] + table_size[0]/2, step1_pos[1]-10, text=translate_text("Step 1", lang), font=font)
    text_3 = canvas.create_text(step2_pos[0] + table_size[0]/2, step2_pos[1]-10, text=translate_text("Step 2", lang), font=font)
    text_4 = canvas.create_text(step3_pos[0] + table_size[0]/2, step3_pos[1]-10, text=translate_text("Step 3", lang), font=font)
    text_5 = canvas.create_text(step4_pos[0] + table_size[0]/2, step4_pos[1]-10, text=translate_text("Step 4", lang), font=font)
    text_6 = canvas.create_text(margin_size*2 + table_size[0]*2 +  img.shape[1]/2, margin_size*2+img.shape[0]-10, text=translate_text("Result Image", lang), font=font)


def on_select(*args):

    global selected_mask

    if selected_mask_var.get() == "Default Mask":
        selected_mask = msk.defaultMask()
    elif selected_mask_var.get() == "Golay Mask C":
        selected_mask = msk.golayC()
    elif selected_mask_var.get() == "Golay Mask D":
        selected_mask = msk.golayD()
    elif selected_mask_var.get() == "Golay Mask E":
        selected_mask = msk.golayE()
    elif selected_mask_var.get() == "Golay Mask L":
        selected_mask = msk.golayL()
    elif selected_mask_var.get() == "Golay Mask M":
        selected_mask = msk.golayM()
    elif selected_mask_var.get() == "Golay Mask R":
        selected_mask = msk.golayR()

# Load the input image
# img = cv2.imread(r'img/ertka.bmp', 0)


# Load the binary image
binary_img = cv2.imread(r'img/ertka.bmp', cv2.IMREAD_GRAYSCALE)
ret, binary_img = cv2.threshold(binary_img, threshold_value, max_value, cv2.THRESH_BINARY)

#img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
#img = cv2.resize(img, (228, 164))
img  = cv2.resize(binary_img, (228, 164))

for y in range(0,img.shape[0]-2):
        for x in range(0,img.shape[1]-2):
            if img[y][x] != 0:
                img[y][x] = 255
# Apply the morphological dilation
dilation, step1, step2, step3, step4 = defaultThickening(img,1)


# Create a window and canvas to display the images
root = Tk()
root.title('Morphological Dilation Steps')
canvas = Canvas(root, width=3*img.shape[1] + 4*margin_size, height=2*img.shape[0] + 3*margin_size)
canvas.pack()


# Add the mask images
selected_mask_var = StringVar()
selected_mask_var.set(mask_names[0])  # set the default mask to the first in the list
selected_mask_var.trace("w", update_mask_image)


# Add the images on cavas
input_img_var = setPhotoOnCanvas(canvas, img, margin_size, margin_size-20, photo_list)

# Set position valaues
table_size = (int(img.shape[1]//1.3), int(img.shape[0]//1.3))
table_margin_size = 1
table_start_x = margin_size
table_start_y = margin_size*3+40

# Define positions of each step image
step1_pos = (margin_size, margin_size*3+40)
step2_pos = (margin_size+table_size[0] - table_margin_size + 40, margin_size*3+40)
step3_pos = (margin_size, margin_size*3+60+table_size[1] - table_margin_size)
step4_pos = (margin_size+table_size[0] - table_margin_size + 40, margin_size*3+60+table_size[1] - table_margin_size)

# Add the images on cavas
step1_img_var = setPhotoOnCanvas(canvas, cv2.resize(step1, (table_size[0], table_size[1])), step1_pos[0], step1_pos[1], photo_list)
step2_img_var = setPhotoOnCanvas(canvas, cv2.resize(step2, (table_size[0], table_size[1])), step2_pos[0], step2_pos[1], photo_list)
step3_img_var = setPhotoOnCanvas(canvas, cv2.resize(step3, (table_size[0], table_size[1])), step3_pos[0], step3_pos[1], photo_list)
step4_img_var = setPhotoOnCanvas(canvas, cv2.resize(step4, (table_size[0], table_size[1])), step4_pos[0], step4_pos[1], photo_list)

img_result_var = setPhotoOnCanvas(canvas, dilation, margin_size*2 + table_size[0]*2, margin_size*2+img.shape[0], photo_list)

canvas.itemconfigure(step1_img_var, state="hidden")
canvas.itemconfigure(step2_img_var, state="hidden")
canvas.itemconfigure(step3_img_var, state="hidden")
canvas.itemconfigure(step4_img_var, state="hidden")
canvas.itemconfigure(img_result_var, state="hidden")


#Buttons
update_button = Button(root, text='Execute thickening', command=execute_dilation)
load_button = Button(root, text='Load Image', command=open_file_dialog)
mask_dropdown = OptionMenu(root, selected_mask_var, *mask_names, command=on_select)
save_button = Button(root, text='Save Image', command=save_file)
change_lang_button = Button(root, text='PL', command=change_language)
result_to_input_button = Button(root, text='Load result to Input Image', command=load_to_input)
slider, slider_frame = create_slider(root)


# Place the buttons on canvas
update_button_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size, window=update_button)
load_button_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+40, window=load_button)
mask_dropdown_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+80, window=mask_dropdown)
change_lang_window = canvas.create_window(margin_size*2 + img.shape[1] + 25, margin_size+120, window=change_lang_button)
save_button_window = canvas.create_window(margin_size*2 + table_size[0]*2 +  img.shape[1]/2, margin_size*2+img.shape[0]+table_margin_size+table_size[1]+52, window=save_button)
result_to_input_window = canvas.create_window(margin_size*2 + table_size[0]*2 +  img.shape[1]/2, margin_size*2+img.shape[0]+table_margin_size+table_size[1]+80, window=result_to_input_button)
slider_window = canvas.create_window(margin_size*2 + img.shape[1]*2, margin_size+160, window=slider_frame)


# Set default mask image
update_text()
update_mask_image()


root.mainloop()