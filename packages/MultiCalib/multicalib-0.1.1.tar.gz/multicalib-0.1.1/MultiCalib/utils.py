import os
import cv2
import numpy as np
import yaml

from scipy.sparse import lil_matrix

def createDirectory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def resizeImage(img, ratio):
    return cv2.resize(img, None, fx= ratio, fy= ratio, interpolation = cv2.INTER_NEAREST)

def unpackE(E):
    R = E[:3, :3]
    t = E[:3, 3].reshape(-1, 1)
    return cv2.Rodrigues(R)[0], t

def packE(r, t):
    E = np.eye(4)
    E[:3, :3] = cv2.Rodrigues(r)[0]
    E[:3, 3] = t.ravel()
    return E

def getObjectPoints(patternSize, squareSize):
    objp = np.zeros((patternSize[0] * patternSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:patternSize[0], 0:patternSize[1]].T.reshape(-1, 2) * squareSize
    return objp

def createJacSparsity(nParams, nCameras, nPatterns, cameraIndices, patternIndices):
    m = cameraIndices.size * 2
    n = nCameras * nParams + nPatterns * 6
    A = lil_matrix((m, n), dtype=int)

    i = np.arange(cameraIndices.size)
    for s in range(nParams):
        A[2 * i, cameraIndices * nParams + s] = 1
        A[2 * i + 1, cameraIndices * nParams + s] = 1

    for s in range(6):
        A[2 * i, nCameras * nParams + patternIndices * 6 + s] = 1
        A[2 * i + 1, nCameras * nParams + patternIndices * 6 + s] = 1

    return A

def saveCameraParameters(data, savePath):
    try:
        with open(savePath, "w") as f:
            yaml.dump(data, f)
        print("Calibration parameters saved successfully")
    except:
        print("Error: Could not save Calibration parameters")