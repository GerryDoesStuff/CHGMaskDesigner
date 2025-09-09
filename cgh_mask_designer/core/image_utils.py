from PyQt6 import QtGui
import numpy as np

def normalize01(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.float32)
    mn, mx = float(a.min()), float(a.max())
    if mx - mn < 1e-12:
        return np.zeros_like(a, dtype=np.float32)
    return (a - mn) / (mx - mn)

def to_qimage(img: np.ndarray) -> QtGui.QImage:
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 1)
        img = (img * 255.0).astype(np.uint8)
    h, w = img.shape[:2]
    if img.ndim == 2:
        q = QtGui.QImage(img.data, w, h, w, QtGui.QImage.Format.Format_Grayscale8)
        q.ndarray = img
        return q
    elif img.ndim == 3 and img.shape[2] == 3:
        q = QtGui.QImage(img.data, w, h, 3*w, QtGui.QImage.Format.Format_RGB888)
        q.ndarray = img
        return q
    raise ValueError("Unsupported image shape for QImage")
