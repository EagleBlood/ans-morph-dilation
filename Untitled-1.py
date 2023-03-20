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

    return imgA

   





# wczytanie obrazu
img = cv2.imread(r'ertka.bmp', 0)

dimensions = img.shape
height, width = img.shape[:2]

# konwersja trybu kolorów na 3 kanały


# określenie kernela
kernel = np.ones((3, 3), np.uint8)

# zastosowanie filtru maksymalnego z wykorzystaniem kernela
#dilation = cv2.dilate(img, kernel, iterations=1)
dilation = thick(img)
# dodanie marginesów między obrazami
img = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=0)


# utworzenie obrazu szarego jako tła okna
background = np.zeros((height*2, width*3), dtype=np.uint8)
background[:] = (128)

# dodanie opisu na górze obrazów
cv2.putText(background, "Image 1", (80, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
cv2.putText(background, "Image 2", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)

# umieszczenie obrazów na tle
background[50:height+50, 50:width+50] = img
background[50:height+50, 150+width:150+(2*width)] = dilation

# wyświetlenie obrazów przed i po dylatacji
cv2.imshow('Result', background)
cv2.waitKey(0)
cv2.destroyAllWindows()