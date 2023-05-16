import numpy as np

def defaultMask():
    mask1 = np.array([[2, 255, 2],
                     [0, 0, 0],
                     [0, 0, 0]], dtype=np.uint8)
    
    mask2 = np.array([[0, 0, 2],
                     [0, 0, 255],
                     [0, 0, 2]], dtype=np.uint8)
    
    mask3 = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [2, 255, 2]], dtype=np.uint8)
    
    mask4 = np.array([[2, 0, 0],
                     [255, 0, 0],
                     [2, 0, 0]], dtype=np.uint8)
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8),mask3.astype(np.uint8),mask4.astype(np.uint8)



def golayC():
    mask1 = np.array([[255, 2, 2],
                     [255, 0, 2],
                     [255, 255, 2]], dtype=np.uint8)
    mask2 = np.array([[2, 255, 2],
                     [255, 0, 2],
                     [2, 255, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayD():
    mask1 = np.array([[2, 0, 2],
                     [0, 255, 255],
                     [2, 0, 2]], dtype=np.uint8)
    mask2 = np.array([[0, 2, 2],
                     [0, 0, 255],
                     [0, 0, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayE():
    mask1 = np.array([[0, 0, 0],
                     [0, 255, 0],
                     [0, 2, 2]], dtype=np.uint8)
    mask2 = np.array([[0, 0, 0],
                     [0, 255, 0],
                     [2, 0, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayL():
    mask1 = np.array([[255, 255, 255],
                     [2, 255, 2],
                     [0, 0, 0]], dtype=np.uint8)
    mask2 = np.array([[255, 2, 255],
                     [2, 255, 2],
                     [0, 0, 0]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayM():
    mask1 = np.array([[255, 255, 2],
                     [255, 255, 0],
                     [255, 255, 2]], dtype=np.uint8)
    
    
    
    return mask1.astype(np.uint8)

def golayR():
    mask1 = np.array([[2, 2, 2],
                     [2, 255, 0],
                     [2, 2, 2]], dtype=np.uint8)
    
    
    
    return mask1.astype(np.uint8)

def skiz():
    mask1 = np.array([[2, 255, 2],
                     [2, 0, 2],
                     [0, 0, 0]], dtype=np.uint8)
    mask2 = np.array([[0, 2, 2],
                     [0, 0, 255],
                     [0, 2, 2]], dtype=np.uint8)
    mask3 = np.array([[0, 0, 0],
                     [2, 0, 2],
                     [2, 255, 2]], dtype=np.uint8)
    mask4 = np.array([[2, 2, 0],
                     [255, 0, 0],
                     [2, 2, 0]], dtype=np.uint8)
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8),mask3.astype(np.uint8),mask4.astype(np.uint8)

def canvas():
    mask1 = np.array([[255, 2, 2],
                     [255, 2, 255],
                     [255, 255, 2]], dtype=np.uint8)
    mask2 = np.array([[2, 255, 2],
                     [255, 2, 0],
                     [2, 255, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)