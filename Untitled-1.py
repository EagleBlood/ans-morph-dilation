from PIL import Image, ImageTk
import numpy as np
import cv2
from tkinter import SINGLE, Button, Listbox, Tk, Canvas

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

    tab = np.zeros((3,3), np.uint8)
    tab[0,1] = 1
    
    for y in range(0,img.shape[0]-2):
        for x in range(0,img.shape[1]-2):
            masked1 = np.array(imgA[y:y+3,x:x+3])
            masked2 = np.array(masked1)
            masked3 = np.array(masked1)
            masked4 = np.array(masked1)

            masked1 *= tab
            tab = np.rot90(tab)
            masked4 *= tab
            tab = np.rot90(tab)
            masked3 *= tab
            tab = np.rot90(tab)
            masked2 *= tab
            tab = np.rot90(tab)

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
    canvas.create_image(x, y, image=photo_list[-1], anchor='nw')


#global variables
margin_size = 70
white_color = (255, 255, 255)
font = cv2.FONT_HERSHEY_SIMPLEX
photo_list = []


# load the input image
img = cv2.imread(r'ertka.bmp', 0)

# apply the morphological dilation
dilation, step1, step2, step3, step4 = thick(img)

# create a window and canvas to display the images
root = Tk()
root.title('Morphological Dilation Steps')
canvas = Canvas(root, width=3*img.shape[1] + 4*margin_size, height=2*img.shape[0] + 3*margin_size)
canvas.pack()

# set the images and labels
canvas.create_text(margin_size+img.shape[1]/2, margin_size-40, text='Input Image', font=font)
setPhotoOnCanvas(canvas, img, margin_size, margin_size-20, photo_list)

#Buttons
update_button = Button(root, text='Update Images')
load_button = Button(root, text='Load Image')
mask_list = Listbox(root, selectmode=SINGLE, height=3)
mask_list.insert(1, 'Mask 1')
mask_list.insert(2, 'Mask 2')
mask_list.insert(3, 'Mask 3')
mask_list.insert(4, 'Mask 4')
save_button = Button(root, text='Save Image')


# Place the buttons to the right of the input image
update_button.place(x=margin_size+img.shape[1]+20, y=margin_size)
load_button.place(x=margin_size+img.shape[1]+20, y=margin_size+40)
mask_list.place(x=margin_size+img.shape[1]+20, y=margin_size+80)


# create a table to display the morphological dilation steps
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

# add result image next to the table
canvas.create_text(margin_size*2 + table_size[0]*2 + margin_size//2, margin_size*2+img.shape[0]-10, text='Result', font=font)
setPhotoOnCanvas(canvas, dilation, margin_size*2 + table_size[0]*2, margin_size*2+img.shape[0], photo_list)

save_button.place(x=margin_size*2 + table_size[0]*2, y=margin_size*2+img.shape[0]+table_margin_size+table_size[1]+30)


root.mainloop()