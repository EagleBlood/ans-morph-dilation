import numpy as np

def defaultMask():
    mask = np.zeros((3,3), dtype=np.uint8)
    mask[0, 0] = 1
    mask[0, 1] = 1
    mask[0, 2] = 1
    return mask.astype(np.uint8)

def noBordering():
    mask = np.zeros((3,3), dtype=np.uint8)
    mask[0, 0] = 1
    mask[0, 1] = 1
    mask[0, 2] = 1
    mask[1, 0] = 1
    mask[1, 2] = 1

def golayC():
    mask = np.zeros((3,3), dtype=np.uint8)
    mask[0, 0] = 1
    mask[1, 0] = 1
    mask[2, 0] = 1
    mask[2, 1] = 1
    return mask.astype(np.uint8)

def golayD():
    mask = np.zeros((3,3), dtype=np.uint8)
    mask[1, 1] = 1
    mask[1, 2] = 1
    return mask.astype(np.uint8)

def golayE():
    mask = np.zeros((3,3), dtype=np.uint8)
    mask[1, 1] = 1
    return mask.astype(np.uint8)