import os
import networkx as nx
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from typing import Dict, List, Tuple

from .utils import createJacSparsity, packE, unpackE, createDirectory, saveCameraParameters
from .Camera import Camera


class CameraSystemCalibration:
    """
    A class to represent and calibrate a multi-camera system using detected patterns.
    """
    
    def __init__(self, data: Dict[str, List[str]], patternSize: List[Tuple[int, int]], squareSize: List[float], 
                 minNoPatterns: int = 10, optimizeSingleCalib: bool = False, drawGraph: bool = False) -> None:
        """
        Initializes a CameraSystemCalibration instance.
        
        :param data: Dictionary containing camera names as keys and lists of image paths as values.
        :param patternSize: List of tuples representing the size of the patterns.
        :param squareSize: List of square sizes for the patterns.
        :param minNoPatterns: Minimum number of patterns required for calibration.
        :param optimizeSingleCalib: Flag to optimize single camera calibration.
        :param drawGraph: Flag to draw the graph of camera and pattern connections.
        """
        self.data = data
        self.patternSize = patternSize
        self.squareSize = squareSize
        self.minNoPatterns = minNoPatterns
        self.optimizeSingleCalib = optimizeSingleCalib
        self.drawGraph = drawGraph
        self.cameras = []
        self.extrinsicTable = []
        self.graph = nx.Graph()

        for cameraName in self.data:
            camera = Camera(self.data[cameraName], cameraName, self.patternSize, self.squareSize, self.minNoPatterns, self.optimizeSingleCalib)
            if camera.isCalibrated:
                found = camera.getFound()
                self.cameras.append(camera)
                self.extrinsicTable.append(found)

    def calibrateSystem(self) -> None:
        """
        Calibrates the multi-camera system.
        """
        self.initialize()
        self.optimize(True)
        self.optimize(False)
        self.updatePose()
        print(f'System Calibration Sucessfull for {self.numCameras} cameras and {self.numPatterns} patterns')

    def initialize(self) -> None:
        """
        Initializes the calibration process.
        """
        self.extrinsicTable = np.array(self.extrinsicTable)
        self.extrinsicTable = self.extrinsicTable[:, ~np.all(self.extrinsicTable == 0, axis=0)]
        self.cRefIdx = np.argmax(self.extrinsicTable.sum(axis=1)) # index of camera that saw most patterns.

        self.numCameras = self.extrinsicTable.shape[0]
        self.numPatterns = self.extrinsicTable.shape[1]

        self.points2D = []
        self.points3D = []
        self.cameraIndices = []
        self.patternIndices = []
        
        self.initializeGraph()
        self.initializePoses()

        self.points2D = np.vstack(self.points2D)
        self.points3D = np.vstack(self.points3D)
        self.cameraIndices = np.array(self.cameraIndices)
        self.patternIndices = np.array(self.patternIndices)

    def initializeGraph(self) -> None:
        """
        Initializes the graph of camera and pattern connections.
        """
        for cameraIdx in range(self.numCameras):
            self.graph.add_node(('camera', cameraIdx))

        for patternIdx in range(self.numPatterns):
            self.graph.add_node(('pattern', patternIdx))

        for cameraIdx in range(self.numCameras):
            for patternIdx in range(self.numPatterns):
                if self.extrinsicTable[cameraIdx, patternIdx] == 1:
                    self.graph.add_edge(('camera', cameraIdx), ('pattern', patternIdx))

        if self.drawGraph:
            self.visualizeGraph()

    def visualizeGraph(self) -> None:
        """
        Visualizes the graph of camera and pattern connections.
        """
        pos = nx.spring_layout(self.graph)  # positions for all nodes
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[n for n in self.graph.nodes if n[0] == 'camera'], node_color='r')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=[n for n in self.graph.nodes if n[0] == 'pattern'], node_color='b')
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.show()

    def initializePoses(self) -> None:
        """
        Initializes the poses of the cameras and patterns.
        """
        self.cameraParamsInit = np.zeros((self.numCameras, 15), np.float64)
        self.patternParamsInit = np.zeros((self.numPatterns, 6), np.float64)

        self.cameraParamsInit[self.cRefIdx, :6] = np.array([0] * 6)  # Set reference camera pose to identity
        self.cameraParamsInit[self.cRefIdx, 6] = self.cameras[self.cRefIdx].intrinsic[0, 0]
        self.cameraParamsInit[self.cRefIdx, 7] = self.cameras[self.cRefIdx].intrinsic[1, 1]
        self.cameraParamsInit[self.cRefIdx, 8] = self.cameras[self.cRefIdx].intrinsic[0, 2]
        self.cameraParamsInit[self.cRefIdx, 9] = self.cameras[self.cRefIdx].intrinsic[1, 2]
        self.cameraParamsInit[self.cRefIdx, 10:] = self.cameras[self.cRefIdx].distortion.ravel()

        queue = [self.cRefIdx]
        visited = set(queue)

        while queue:
            cameraIdx = queue.pop(0)
            patterns = self.cameras[cameraIdx].getPatterns()
            for pattern in self.graph.neighbors(('camera', cameraIdx)):
                patternIdx = pattern[1]
                patternIdxRel = np.where(np.nonzero(self.extrinsicTable[cameraIdx, :])[0] == patternIdx)[0][0]
                self.points2D.append(patterns[patternIdxRel].imgPoints.reshape(-1, 2))
                self.points3D.append(patterns[patternIdxRel].objPoints.reshape(-1, 3))
                self.cameraIndices.extend([cameraIdx] * len(patterns[patternIdxRel].objPoints))
                self.patternIndices.extend([patternIdx] * len(patterns[patternIdxRel].objPoints))
                if self.patternParamsInit[patternIdx, :].any() == 0:
                    ECam = packE(self.cameraParamsInit[cameraIdx, :3], self.cameraParamsInit[cameraIdx, 3:6])
                    EPattern = patterns[patternIdxRel].pose
                    EPatternRef = np.linalg.solve(ECam, EPattern) # solves Ax=b, where A = ECam, and B = EPattern
                    rRel, tRel = unpackE(EPatternRef)
                    self.patternParamsInit[patternIdx, :] = np.hstack((rRel.ravel(), tRel.ravel()))
                # Iterate through all cameras that have also seen this pattern
                for neighborCam in self.graph.neighbors(pattern):
                    neighborCameraIdx = neighborCam[1]
                    neighborCamera = self.cameras[neighborCameraIdx]
                    neighborPatternIdxRel = np.where(np.nonzero(self.extrinsicTable[neighborCameraIdx, :])[0] == patternIdx)[0][0]
                    if neighborCameraIdx == cameraIdx or neighborCameraIdx in visited:
                        continue
                    EPattern = neighborCamera.patterns[neighborPatternIdxRel].pose
                    EPatternRef = packE(self.patternParamsInit[patternIdx, :3], self.patternParamsInit[patternIdx, 3:])
                    ECam = EPattern @ np.linalg.inv(EPatternRef)
                    rRel, tRel = unpackE(ECam)
                    self.cameraParamsInit[neighborCameraIdx, :3] = rRel.ravel()
                    self.cameraParamsInit[neighborCameraIdx, 3:6] = tRel.ravel()
                    self.cameraParamsInit[neighborCameraIdx, 6] = neighborCamera.intrinsic[0, 0]
                    self.cameraParamsInit[neighborCameraIdx, 7] = neighborCamera.intrinsic[1, 1]
                    self.cameraParamsInit[neighborCameraIdx, 8] = neighborCamera.intrinsic[0, 2]
                    self.cameraParamsInit[neighborCameraIdx, 9] = neighborCamera.intrinsic[1, 2]
                    self.cameraParamsInit[neighborCameraIdx, 10:] = neighborCamera.distortion.ravel()
                    visited.add(neighborCameraIdx)
                    queue.append(neighborCameraIdx)

    def optimize(self, fixedIntrinsics: bool = False) -> None:
        """
        Optimizes the calibration parameters.
        
        :param fixedIntrinsics: Flag to fix the intrinsic parameters during optimization.
        """
        cameraParamsInit = self.cameraParamsInit[:, :6] if fixedIntrinsics else self.cameraParamsInit
        patternParamsInit = self.patternParamsInit
        paramsInit = np.hstack((cameraParamsInit.ravel(), patternParamsInit.ravel()))

        self.numParams = cameraParamsInit.shape[1]
        jacSparsity = createJacSparsity(self.numParams, self.numCameras, self.numPatterns, self.cameraIndices, self.patternIndices)
        res = least_squares(
            self.reprojectionError,
            paramsInit,
            args=(self.points2D, self.points3D, self.cameraIndices, self.patternIndices),
            x_scale='jac',
            ftol=1e-4,
            method='trf',
            jac_sparsity=jacSparsity,
            verbose=2,
            max_nfev=100
        )

        self.reprojectionSystemError(res)
        optimizedParams = res.x
        optimizedCameraParams = optimizedParams[:self.numCameras * self.numParams].reshape((self.numCameras, self.numParams))
        optimizedPatternParams = optimizedParams[self.numCameras * self.numParams:].reshape((self.numPatterns, 6))

        self.cameraParamsInit[:, :self.numParams] = optimizedCameraParams
        self.patternParamsInit = optimizedPatternParams

    def updatePose(self) -> None:
        """
        Updates the poses of the cameras and patterns after optimization.
        """
        for cIdx, camera in enumerate(self.cameras):
            cameraParams = self.cameraParamsInit[cIdx]
            camera.pose = packE(cameraParams[:3], cameraParams[3:6])
            mtx = np.eye(3)
            mtx[0, 0] = cameraParams[6]
            mtx[1, 1] = cameraParams[7]
            mtx[0, 2] = cameraParams[8]
            mtx[1, 2] = cameraParams[9]
            camera.intrinsic = mtx
            camera.distortion = cameraParams[10:]

            patterns = camera.getPatterns()
            iExist = np.where(self.extrinsicTable[cIdx, :] == 1)[0]
            for idx, i in enumerate(iExist):
                patternParams = self.patternParamsInit[i]
                patterns[idx].pose = packE(patternParams[:3], patternParams[3:])

    def reprojectionError(self, params: np.ndarray, points2D: np.ndarray, points3D: np.ndarray, 
                          cameraIndices: np.ndarray, patternIndices: np.ndarray) -> np.ndarray:
        """
        Computes the reprojection error for the optimization process.
        """
        cameraParams = params[:self.numCameras * self.numParams].reshape((self.numCameras, self.numParams))
        patternParams = params[self.numCameras * self.numParams:].reshape((self.numPatterns, 6))
        cameraParams[self.cRefIdx, :6] = np.array([0] * 6)
        points2DProj = []
        for i in range(len(points3D)):
            cameraIndex = cameraIndices[i]
            patternIndex = patternIndices[i]

            cam = self.cameraParamsInit[cameraIndex]
            cam[:self.numParams] = cameraParams[cameraIndex]
            pattern = patternParams[patternIndex]

            ECam = packE(cam[:3], cam[3:6])
            EPattern = packE(pattern[:3], pattern[3:])
            mtx = np.eye(3)
            mtx[0, 0] = cam[6]
            mtx[1, 1] = cam[7]
            mtx[0, 2] = cam[8]
            mtx[1, 2] = cam[9]
            dist = cam[10:]

            ERel = ECam @ EPattern
            rRel, tRel = unpackE(ERel)
        
            X = points3D[i]
            x, _ = cv2.projectPoints(X, rRel, tRel, mtx, dist)
            points2DProj.append(x.reshape(2,))
    
        points2DProj = np.array(points2DProj)
        return (points2D - points2DProj).ravel()
    
    def reprojectionSystemError(self, res: least_squares) -> None:
        """
        Prints the system reprojection error after optimization.
        """
        meanError = np.sqrt(np.mean(res.fun ** 2))
        print(f"Calibration System Reprojection Error: {meanError:.2f} pixels")

    def reprojectPoints(self, path: str) -> None:
        """
        Reprojects points and saves the images with the projected points.
        
        :param path: Path to save the reprojected images.
        """
        reprojectionPath = os.path.join(path, 'reprojections')
        for camera in self.cameras:
            cameraPath = os.path.join(reprojectionPath, camera.cameraName)
            createDirectory(cameraPath)
            camera.reprojectPoints(cameraPath)

    def getCameras(self) -> List[Camera]:
        """
        Returns the list of calibrated cameras.
        """
        return self.cameras
    
    def exportCameraParameters(self, savePath: str = 'parameters.yaml') -> None:
        """
        Exports the camera parameters to a YAML file.
        
        :param savePath: Path to save the parameters file.
        """
        params = {}
        for camera in self.cameras:
            params[camera.cameraName] = {
                'image_size': list(camera.imageShape[::-1]),
                'intrinsics': np.asarray(camera.intrinsic).tolist(),
                'distortion_coeff': np.asarray(camera.distortion).tolist(),
                'extrinsics': np.asarray(camera.pose).tolist()
            }
        saveCameraParameters(params, savePath)