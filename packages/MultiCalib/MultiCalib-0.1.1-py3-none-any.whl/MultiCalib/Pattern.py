from typing import Tuple
import numpy as np
from .utils import getObjectPoints

class Pattern:
    """
    A class to represent a detected pattern in an image for camera calibration.
    """
    
    def __init__(self, imagePath: str, imgPoints: np.ndarray, patternSize: Tuple[int, int], squareSize: float) -> None:
        """
        Initializes a Pattern instance.
        
        :param imagePath: Path to the image containing the pattern.
        :param imgPoints: Image points detected in the pattern.
        :param patternSize: Size of the pattern (number of inner corners per chessboard row and column).
        :param squareSize: Size of a square in the pattern.
        """
        self.path = imagePath
        self.imgPoints = imgPoints
        self.objPoints = getObjectPoints(patternSize, squareSize)
        self.pose = None

    def setPose(self, E: np.ndarray) -> None:
        """
        Sets the pose of the pattern.
        
        :param E: The pose matrix (extrinsic parameters) of the pattern.
        """
        self.pose = E
