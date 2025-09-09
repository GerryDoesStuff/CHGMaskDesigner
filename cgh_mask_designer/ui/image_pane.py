from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from ..core.image_utils import to_qimage
import numpy as np

class ImagePane(QtWidgets.QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(320, 320)
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setWordWrap(True)

    def set_array(self, arr: np.ndarray):
        q = to_qimage(arr)
        pm = QtGui.QPixmap.fromImage(q)
        self.setPixmap(pm.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, e):
        if self.pixmap():
            self.setPixmap(self.pixmap().scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        super().resizeEvent(e)
