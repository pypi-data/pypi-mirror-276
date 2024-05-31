import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from typing import List, Tuple

from .utils import resizeImage, createJacSparsity, packE, unpackE
from .Pattern import Pattern


class Camera:
    """
    A class to represent a camera and perform calibration using chessboard patterns.
    """

    def __init__(self, imagePaths: List[str], cameraName: str, patternSize: List[Tuple[int, int]], 
                 squareSize: List[float], minNoPatterns: int = 10, optimizeSingleCalib: bool = False) -> None:
        self.found = []
        self.cameraName = cameraName
        self.patterns = []
        self.patternSize = patternSize
        self.squareSize = squareSize
        self.minNoPatterns = minNoPatterns
        self.optimizeSingleCalib = optimizeSingleCalib
        self.imageShape = None
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        self.isCalibrated = False
        self.intrinsic = None
        self.distortion = None
        self.numCameraParams = 9
        self.pose = np.eye(4)

        self.getPatternPoints(imagePaths)
        self.calibrate()

    def getPatternPoints(self, imagePaths: List[str], flag: bool = False) -> None:
        """
        Detects chessboard pattern points in the provided images.
        """
        for imagePath in imagePaths:
            img = cv2.imread(imagePath)
            is_found = False
            for i in range(4, 1, -1):
                ratio = 1/(2 ** i)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                self.imageShape = gray.shape[::-1]
                gray_resized = resizeImage(gray, ratio)
                chessBoardFlags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE if flag else None
                pattern_idx = 0
                for idx, size in enumerate(self.patternSize):
                    ret, corners = cv2.findChessboardCorners(gray_resized, size, chessBoardFlags)
                    if ret:
                        pattern_idx = idx
                        break
                if ret:
                    corners = corners / ratio
                    corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), self.criteria)
                    self.patterns.append(Pattern(imagePath, corners2, self.patternSize[pattern_idx], self.squareSize[pattern_idx]))
                    self.found.append(1)
                    is_found = True
                    break
            if not is_found:
                self.found.append(0)
            is_found = False

        print(f"Number of images with detected pattern points for {self.cameraName}: ", sum(self.found))

    def calibrate(self) -> None:
        """
        Calibrates the camera using the detected pattern points.
        """
        if sum(self.found) >= self.minNoPatterns:
            objPoints = [pattern.objPoints for pattern in self.patterns]
            imgPoints = [pattern.imgPoints for pattern in self.patterns]
            _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, self.imageShape, None, None)
            self.reprojectionInitialError(objPoints, imgPoints, mtx, dist, rvecs, tvecs)
            
            if self.optimizeSingleCalib:
                self.optimize(imgPoints, objPoints, mtx, dist, rvecs, tvecs)
            else:
                self.intrinsic = mtx
                self.distortion = dist
                for idx, pattern in enumerate(self.patterns):
                    pattern.setPose(packE(rvecs[idx], tvecs[idx]))
                self.isCalibrated = True
        else:
            self.isCalibrated = False

    def optimize(self, imgPoints: List[np.ndarray], objPoints: List[np.ndarray], mtx: np.ndarray, 
                 dist: np.ndarray, rvecs: List[np.ndarray], tvecs: List[np.ndarray]) -> None:
        """
        Optimizes the calibration parameters using non-linear least squares.
        """
        numPatterns = len(self.patterns)
        points2D = np.vstack([imgPoint.reshape(-1, 2) for imgPoint in imgPoints])
        points3D = np.vstack([objPoint.reshape(-1, 3) for objPoint in objPoints])
        cameraIndices = np.array([[i for points in objPoints for i in [0] * len(points)]])
        patternIndices = np.array([i for idx, points in enumerate(objPoints) for i in [idx] * len(points)])

        cameraParams = np.zeros((self.numCameraParams), np.float64)
        cameraParams[0] = mtx[0, 0]
        cameraParams[1] = mtx[1, 1]
        cameraParams[2] = mtx[0, 2]
        cameraParams[3] = mtx[1, 2]
        cameraParams[4:] = dist.ravel()

        patternParams = np.zeros((numPatterns, 6), np.float64)
        for i in range(numPatterns):
            patternParams[i, :] = np.hstack((rvecs[i].ravel(), tvecs[i].ravel()))

        paramsInit = np.hstack((cameraParams.ravel(), patternParams.ravel()))
        jacSparsity = createJacSparsity(self.numCameraParams, 1, numPatterns, cameraIndices, patternIndices)

        res = least_squares(
            self.reprojectionError,
            paramsInit,
            args=(points2D, points3D, patternIndices),
            x_scale='jac',
            ftol=1e-4,
            method='trf',
            jac_sparsity=jacSparsity,
            verbose=2,
            max_nfev=100
        )

        self.reprojectionOptimizedError(res)
        optimizedParams = res.x
        optimizedCameraParams = optimizedParams[:self.numCameraParams]
        optimizedPatternParams = optimizedParams[self.numCameraParams:].reshape((numPatterns, 6))
        
        mtx = np.eye(3)
        mtx[0, 0] = optimizedCameraParams[0]
        mtx[1, 1] = optimizedCameraParams[1]
        mtx[0, 2] = optimizedCameraParams[2]
        mtx[1, 2] = optimizedCameraParams[3]
        self.intrinsic = mtx
        self.distortion = optimizedCameraParams[4:]

        for idx, pattern in enumerate(self.patterns):
            patternParams = optimizedPatternParams[idx, :]
            pattern.setPose(packE(patternParams[:3], patternParams[3:]))

        self.isCalibrated = True

    def reprojectionError(self, params: np.ndarray, points2D: np.ndarray, points3D: np.ndarray, 
                          patternIndices: np.ndarray) -> np.ndarray:
        """
        Computes the reprojection error.
        """
        numPatterns = patternIndices.max() + 1
        cameraParams = params[:self.numCameraParams]
        patternParams = params[self.numCameraParams:].reshape((numPatterns, 6))
        points2DProj = []

        for i in range(len(points3D)):
            patternIndex = patternIndices[i]
            pattern = patternParams[patternIndex]
            mtx = np.eye(3)
            mtx[0, 0] = cameraParams[0]
            mtx[1, 1] = cameraParams[1]
            mtx[0, 2] = cameraParams[2]
            mtx[1, 2] = cameraParams[3]
            dist = cameraParams[4:]
            rvec = pattern[:3]
            tvec = pattern[3:]
            X = points3D[i]
            x, _ = cv2.projectPoints(X, rvec, tvec, mtx, dist)
            points2DProj.append(x.reshape(2,))

        points2DProj = np.array(points2DProj)
        return (points2D - points2DProj).ravel()

    def reprojectionInitialError(self, objPoints: List[np.ndarray], imgPoints: List[np.ndarray], 
                                 mtx: np.ndarray, dist: np.ndarray, rvecs: List[np.ndarray], 
                                 tvecs: List[np.ndarray]) -> None:
        """
        Computes the initial reprojection error.
        """
        mean_error = 0
        for i in range(len(objPoints)):
            imgPoints2, _ = cv2.projectPoints(objPoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgPoints[i], imgPoints2, cv2.NORM_L2)/len(imgPoints2)
            mean_error += error
        print("Initial Reprojection Error: {}".format(mean_error/len(objPoints)))

    def reprojectionOptimizedError(self, res: least_squares) -> None:
        """
        Prints the optimized reprojection error.
        """
        mean_error = np.sqrt(np.mean(res.fun ** 2))
        print(f"Optimized Reprojection Error: {mean_error:.2f} pixels")

    def reprojectPoints(self, savePath: str) -> None:
        """
        Reprojects points and saves the images with the projected points.
        """
        for idx, pattern in enumerate(self.patterns):
            H1 = self.pose
            H2 = pattern.pose
            E = H1 @ H2
            r, t = unpackE(E)
            x, _ = cv2.projectPoints(pattern.objPoints, r, t, self.intrinsic, self.distortion)
            x = np.int0(x.reshape(-1, 2))
            img = cv2.imread(pattern.path)
            for point in x:
                try:
                    img = cv2.circle(img, (point[0], point[1]), (img.shape[1]*20)//8192, (255, 0, 0), (img.shape[1]*10)//8192)
                except:
                    continue
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            plt.imsave(f'{savePath}/{idx}.png', img)

    def getFound(self) -> List[int]:
        """
        Returns the list indicating which images had detected pattern points.
        """
        return self.found
    
    def getPatterns(self) -> List[Pattern]:
        """
        Returns the list of detected patterns.
        """
        return self.patterns