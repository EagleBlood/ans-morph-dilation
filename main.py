import PIL.Image as Image
import PIL.ImageTk as ImageTk
import numpy as np
import cv2
from tkinter import ttk, SINGLE, Button, OptionMenu, Scale, StringVar, Tk, Canvas, HORIZONTAL, Frame, Label, LEFT, filedialog
import os
import masks as msk

#Global variables
program_dir = os.path.dirname(os.path.abspath(__file__))
img = None
margin_size = 70
background_color = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
photo_list = []
selected_file_path = ""
dilation, difference = None, None
selected_mask = None
mask_value = "Choose a mask"

# #Image processing variables
threshold_value = 127
max_value = 255

mask_filenames = {
    "Default Mask": "mask/Default.png", #1 / pogrubianie
    "Skiz": "mask/skiz.png",# 2 
    "Convex hull": "mask/maskCanv.png",# 3
    "Golay Mask C": "mask/maskC.png",# 4
    "Golay Mask D": "mask/maskD.png",# 5
    "Golay Mask E": "mask/maskE.png",# 6
    "Golay Mask L": "mask/maskL.png",# 7
    "Golay Mask M": "mask/maskM.png",# 8
    "Golay Mask R": "mask/maskR.png",# 9
    "Golay SKIZ": "mask/golaySkiz.png",# 10
}

mask_names = [
    "Default Mask",
    "Skiz", 
    "Convex hull",
    "Golay Mask C",
    "Golay Mask D",
    "Golay Mask E",
    "Golay Mask L",
    "Golay Mask M",
    "Golay Mask R",
    "Golay SKIZ"
]

dictionary = {
    "Input Image": "Obraz wejściowy",
    "Output Image": "Obraz wynikowy",
    "Load Image": "Wczytaj obraz",
    "Save Image": "Zapisz obraz",
    "PL": "EN",
    "Swap output/input": "Zamień obraz",
    "Mask/Masks":"Maska/Maski)",
    "Choose a mask":"Wybierz maskę",
    "Differential image":"Różnica obrazu",
    "Loaded Image":"Wczytany Obraz",
    "No operations":"Liczba Iiteracji",
    "Morphological thickening operations":"Morfologiczne operacje pogrubiania",
    "MENU Settings":"Ustawienia programu",
    "Result Image MENU":"Operacje na obrazie wyjściowym",
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
selected_mask = None


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
            

    
    return imgA, imgDiff


def update_main_image(canvas, selected_file_path):
    global image_ref # To prevent garbage collection
    global img
    
    update_image = load_img(selected_file_path)
    update_image = cv2.resize(update_image, (228, 228))
    
    for y in range(0,update_image.shape[0]-2):
        for x in range(0,update_image.shape[1]-2):
            if update_image[y][x] != 0:
                update_image[y][x] = 255


    img = update_image
    update_image = ImageTk.PhotoImage(Image.fromarray(update_image))

    canvas.create_image(0, 0, anchor='nw', image=update_image)
    canvas.image = update_image
    image_ref = update_image
    
    return update_image

def update_image(canvas, image):
    global img_res_ref

    img_pil = Image.fromarray(image)
    img_tk = ImageTk.PhotoImage(img_pil)
    
    canvas.create_image(0, 0, anchor='nw', image=img_tk)
    canvas.image = img_tk
    img_res_ref = img_tk

def on_slider_move(value):

    difference_image_var.delete("all")
    result_image_var.delete("all")

    save_button.config(state="disabled")
    rti_button.config(state="disabled")

    return value

def update_mask_image(*args):
    global mask_ref # To prevent garbage collection
    
    mask_name = selected_mask_var.get()
    if mask_name != mask_value:
        mask_img = load_img(os.path.join(program_dir, mask_filenames[mask_name]))
        mask_img = Image.fromarray(mask_img)
        mask_img = mask_img.resize((228, 228), Image.LANCZOS)

        mask_img = ImageTk.PhotoImage(mask_img)

        mask_image_var.create_image(0, 0, anchor='nw', image=mask_img)
        mask_ref = mask_img
    
        difference_image_var.delete("all")
        result_image_var.delete("all")

        save_button.config(state="disabled")
        rti_button.config(state="disabled")

def clear_all():
    global img, dilation, selected_mask_var, slider, selected_mask

    img = None
    selected_mask = None
    dilation = None

    selected_mask_var.set(mask_value)
    slider.set(1)
    input_image_var.delete("all")
    mask_image_var.delete("all")
    difference_image_var.delete("all")
    result_image_var.delete("all")

    save_button.config(state="disabled")
    rti_button.config(state="disabled")
    update_button.config(state="normal")


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
        result_image_var.delete("all")
        difference_image_var.delete("all")

        update_main_image(input_image_var, selected_file_path)
        save_button.config(state="disabled")
        rti_button.config(state="disabled")

def save_file():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".jpg", filetypes=[(".jpg", "*.jpg"), ("All Files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, dilation)

def load_img(path):
    binary_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    ret, binary_img = cv2.threshold(binary_img, threshold_value, max_value, cv2.THRESH_BINARY)

    img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

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
    global dilation, difference, selected_mask    

    if img is not None and selected_mask is not None:
        dilation, difference = defaultThickening(img, slider.get())

        update_image(difference_image_var, difference)
        update_image(result_image_var, dilation)

        save_button.config(state="normal")
        rti_button.config(state="normal")
        
def load_to_input():

    global img, dilation

    tmp_img = dilation
    clear_all()
    img = tmp_img    
    update_image(input_image_var, img)
    update_button.config(state="normal")    

    

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
    update_button_text(update_button, "START")
    update_button_text(load_button, "Load Image")
    update_button_text(save_button, "Save Image")
    update_button_text(change_lang_button, "PL")
    update_button_text(rti_button, "Swap output/input")

def update_button_text(button, button_text):
    if button_text in dictionary:
        translated_text = translate_text(button_text, lang)
        button.config(text=translated_text)
    else:
        button.config(text=button_text)

def update_text():
    global mask_value

    label_input_image.config(text=translate_text("Input Image", lang))
    label_difference.config(text=translate_text("Difference", lang))
    label_mask_image.config(text=translate_text("Mask", lang))
    label_result.config(text=translate_text("Result Image", lang))
    label_iterations.config(text=translate_text("Iterations", lang))
    label_mask_image.config(text=translate_text("Mask", lang))
    appName.config(text=translate_text("Morphological thickening operations", lang))
    text_menu.config(text=translate_text("Settings MENU", lang))
    text_result_op.config(text=translate_text("Result Image MENU", lang))
    mask_value = translate_text("Choose a mask", lang)
    selected_mask_var.set(mask_value)

def on_select(event):
    global selected_mask
    selected_mask_var = event.widget.get()
    if selected_mask_var == "Default Mask":
        selected_mask = msk.defaultMask()
    elif selected_mask_var == "Skiz":
        selected_mask = msk.skiz()
    elif selected_mask_var == "Convex hull":
        selected_mask = msk.canvas()
    elif selected_mask_var == "Golay Mask C":
        selected_mask = msk.golayC()
    elif selected_mask_var == "Golay Mask D":
        selected_mask = msk.golayD()
    elif selected_mask_var == "Golay Mask E":
        selected_mask = msk.golayE()
    elif selected_mask_var == "Golay Mask L":
        selected_mask = msk.golayL()
    elif selected_mask_var == "Golay Mask M":
        selected_mask = msk.golayM()
    elif selected_mask_var == "Golay Mask R":
        selected_mask = msk.golayR()
    elif selected_mask_var == "Golay SKIZ":
        selected_mask = msk.goleySkiz()

# Create a window and grid to display the images
root = Tk()
root.title('Morphological Thickening Operations')

# frames
mainFrame = Frame(root)
mainFrame.grid(row=0, column=0, padx=20, pady=20)

frame1 = Frame(mainFrame)
frame1.grid(row=1, column=0, padx=10, pady=10)

frame2 = Frame(mainFrame)
frame2.grid(row=1, column=2, padx=10, pady=10, sticky="n")

# Add the mask images
selected_mask_var = StringVar()
selected_mask_var.set(mask_value)
selected_mask_var.trace("w", update_mask_image)


# buttons
update_button = Button(frame1, text='START', command=execute_dilation, font=("Lato", 10, "bold"))
load_button = Button(frame1, text='Load Image', command=open_file_dialog)
mask_dropdown = OptionMenu(frame1, selected_mask_var, *mask_names, command=on_select)
save_button = Button(frame1, text='Save Image', state="disabled", command=save_file)
change_lang_button = Button(frame1, text='PL', command=change_language)
rti_button = Button(frame1, text='Swap output/input', state="disabled", command=load_to_input)
clear_button = Button(frame1, text='Reset', command=clear_all)

# slider
slider = Scale(frame1, from_=1, to=10, orient=HORIZONTAL, command=on_slider_move)
mask_dropdown = ttk.Combobox(frame1, textvariable=selected_mask_var, values=mask_names, state='readonly')
mask_dropdown.bind("<<ComboboxSelected>>", on_select)

# images 
input_image_var = Canvas(frame2, width=227, height=227, bg="light blue")
mask_image_var = Canvas(frame2, width=227, height=227,bg="light blue")
difference_image_var = Canvas(frame2, width=227, height=227, bg="light blue")
result_image_var = Canvas(frame2, width=227, height=227, bg="light blue")

# separators
separator1 = ttk.Separator(frame1, orient="horizontal")
separator2 = ttk.Separator(frame1, orient="horizontal")
separator3 = ttk.Separator(mainFrame, orient="vertical")

# labels
appName = Label(mainFrame, text="Morphological thickening operations", font=('Lato', 25, 'bold'))
text_menu= Label(frame1, text="Settings MENU", font=("Lato", 11, "bold"))
label_choose_mask = Label(frame1, text="Choose a mask")
label_iterations = Label(frame1, text="Iterations")
text_result_op = Label(frame1, text="Result Image MENU", font=("Lato", 11, "bold"))
label_input_image = Label(frame2, text="Input Image")
label_mask_image = Label(frame2, text="Mask")
label_difference = Label(frame2, text="Difference")
label_result = Label(frame2, text="Result Image")

# ----mainFrame----
appName.grid(row=0, column=0, columnspan=3, pady=(0, 10))

# ----frame1----
text_menu.grid(row=0, column=0, columnspan=2, padx=5, pady=0)
separator1.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
load_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
change_lang_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
mask_dropdown.grid(row=3, column=0, columnspan=2, padx=5, pady=(10,0), sticky="ew")
label_iterations.grid(row=4, column=0, columnspan=2, padx=5, pady=(5,0), sticky="w")
slider.grid(row=5, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")
clear_button.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
update_button.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
text_result_op.grid(row=7, column=0, columnspan=2, padx=5, pady=(15, 0))
separator2.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")
save_button.grid(row=9, column=0, columnspan=2,  padx=5, pady=5, sticky="ew")
rti_button.grid(row=10, column=0, columnspan=2,  padx=5, pady=5, sticky="ew")

# --------------

separator3.grid(row=1, column=1, padx=5 ,pady=5, sticky="ns")

# ----frame2----
input_image_var.grid(row=0, column=0, padx=10, pady=10)
label_input_image.grid(row=1, column=0, padx=10, pady=0)
result_image_var.grid(row=0, column=1, padx=10, pady=10)
label_result.grid(row=1, column=1, padx=10, pady=0)
mask_image_var.grid(row=2, column=0, padx=10, pady=10)
label_mask_image.grid(row=3, column=0, padx=10, pady=0)
difference_image_var.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
label_difference.grid(row=3, column=1, columnspan=2, padx=10, pady=0)



update_text()
update_mask_image()

root.mainloop()