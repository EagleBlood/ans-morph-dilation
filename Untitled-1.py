import cv2
import numpy as np


def thick(img):
    imgA = np.array(img)
    
    img1 = np.array(imgA,np.uint8)
    img2 = np.array(imgA,np.uint8)
    img3 = np.array(imgA,np.uint8)
    img4 = np.array(imgA,np.uint8)

    tab = np.zeros((3,3), np.uint8)
    tab[0,1] = 1
  

    masked1 = np.zeros((3,3), np.uint8)
    masked2 = np.zeros((3,3), np.uint8)
    masked3 = np.zeros((3,3), np.uint8)
    masked4 = np.zeros((3,3), np.uint8)
    
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

   



# load the input image
img = cv2.imread(r'ertka.bmp', 0)

# apply the morphological dilation
dilation, step1, step2, step3, step4 = thick(img)

# create a 2x3 table for displaying the images with margins and a gray background
margin_size = 70
white_color = (123, 123, 127)
table = np.ones((2*img.shape[0] + 3*margin_size, 3*img.shape[1] + 4*margin_size), dtype=np.uint8) * white_color[0]
table[margin_size:-margin_size, margin_size:-margin_size] = white_color[0]

# set the first image to be the input image with margins and a label
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(table, 'Input Image', (margin_size+10, margin_size-10), font, 1, (0, 0, 0), 2)
table[margin_size:img.shape[0]+margin_size, margin_size:img.shape[1]+margin_size] = img

# set the intermediate images in the remaining cells of the first row with margins and labels
cv2.putText(table, 'Step 1', (img.shape[1]+2*margin_size+10, margin_size-10), font, 1, (0, 0, 0), 2)
table[margin_size:img.shape[0]+margin_size, img.shape[1]+2*margin_size:2*img.shape[1]+2*margin_size] = step1

cv2.putText(table, 'Step 2', (2*img.shape[1]+3*margin_size+10, margin_size-10), font, 1, (0, 0, 0), 2)
table[margin_size:img.shape[0]+margin_size, 2*img.shape[1]+3*margin_size:3*img.shape[1]+3*margin_size] = step2

# set the intermediate images in the remaining cells of the second row with margins and labels
cv2.putText(table, 'Step 3', (margin_size+10, img.shape[0]+2*margin_size-10), font, 1, (0, 0, 0), 2)
table[img.shape[0]+2*margin_size:2*img.shape[0]+2*margin_size, margin_size:img.shape[1]+margin_size] = step3

cv2.putText(table, 'Step 4', (img.shape[1]+2*margin_size+10, img.shape[0]+2*margin_size-10), font, 1, (0, 0, 0), 2)
table[img.shape[0]+2*margin_size:2*img.shape[0]+2*margin_size, img.shape[1]+2*margin_size:2*img.shape[1]+2*margin_size] = step4

cv2.putText(table, 'Result', (2*img.shape[1]+3*margin_size+10, img.shape[0]+2*margin_size-10), font, 1, (0, 0, 0), 2)
table[img.shape[0]+2*margin_size:2*img.shape[0]+2*margin_size, 2*img.shape[1]+3*margin_size:3*img.shape[1]+3*margin_size] = dilation


# display the table of images
cv2.imshow('Morphological Dilation Steps', table)
cv2.waitKey(0)
cv2.destroyAllWindows()