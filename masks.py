import numpy as np

def defaultMask():
    mask1 = np.array([[2, 1, 2],
                     [0, 0, 0],
                     [0, 0, 0]], dtype=np.uint8)
    mask2 = np.array([[0, 0, 2],
                     [0, 0, 1],
                     [0, 0, 2]], dtype=np.uint8)
    mask3 = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [2, 1, 2]], dtype=np.uint8)
    mask4 = np.array([[2, 0, 0],
                     [1, 0, 0],
                     [2, 0, 0]], dtype=np.uint8)
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8),mask3.astype(np.uint8),mask4.astype(np.uint8)



def golayC():
    mask1 = np.array([[1, 2, 2],
                     [1, 0, 2],
                     [1, 1, 2]], dtype=np.uint8)
    mask2 = np.array([[2, 1, 2],
                     [1, 0, 2],
                     [2, 1, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayD():
    mask1 = np.array([[2, 0, 2],
                     [0, 1, 1],
                     [2, 0, 2]], dtype=np.uint8)
    mask2 = np.array([[0, 2, 2],
                     [0, 0, 1],
                     [0, 0, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayE():
    mask1 = np.array([[0, 0, 0],
                     [0, 1, 0],
                     [0, 2, 2]], dtype=np.uint8)
    mask2 = np.array([[0, 0, 0],
                     [0, 1, 0],
                     [2, 0, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayL():
    mask1 = np.array([[1, 1, 1],
                     [2, 1, 2],
                     [0, 0, 0]], dtype=np.uint8)
    mask2 = np.array([[1, 2, 1],
                     [2, 1, 2],
                     [0, 0, 0]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)

def golayM():
    mask1 = np.array([[1, 1, 2],
                     [1, 1, 0],
                     [1, 1, 2]], dtype=np.uint8)
    
    
    
    return mask1.astype(np.uint8)

def golayR():
    mask1 = np.array([[2, 2, 2],
                     [2, 1, 0],
                     [2, 2, 2]], dtype=np.uint8)
    
    
    
    return mask1.astype(np.uint8)

def skiz():
    mask1 = np.array([[2, 1, 2],
                     [2, 0, 2],
                     [0, 0, 0]], dtype=np.uint8)
    mask2 = np.array([[0, 2, 2],
                     [0, 0, 1],
                     [0, 2, 2]], dtype=np.uint8)
    mask3 = np.array([[0, 0, 0],
                     [2, 0, 2],
                     [2, 1, 2]], dtype=np.uint8)
    mask4 = np.array([[2, 2, 0],
                     [1, 0, 0],
                     [2, 2, 0]], dtype=np.uint8)
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8),mask3.astype(np.uint8),mask4.astype(np.uint8)

def convex():
    mask1 = np.array([[1, 2, 2],
                     [1, 2, 1],
                     [1, 1, 2]], dtype=np.uint8)
    mask2 = np.array([[2, 1, 2],
                     [1, 2, 0],
                     [2, 1, 2]], dtype=np.uint8)
    
    
    return mask1.astype(np.uint8),mask2.astype(np.uint8)