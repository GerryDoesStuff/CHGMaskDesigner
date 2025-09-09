import numpy as np
from .image_utils import normalize01

def fft2c(x):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))

def ifft2c(X):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X)))

def sim_fourier(mask_amp: np.ndarray) -> np.ndarray:
    field = fft2c(mask_amp)
    return normalize01(np.abs(field))

def angular_spectrum(field0: np.ndarray, wavelength: float, dx: float, dy: float, z: float) -> np.ndarray:
    H, W = field0.shape
    k = 2*np.pi / wavelength
    fx = np.fft.fftfreq(W, d=dx)
    fy = np.fft.fftfreq(H, d=dy)
    FX, FY = np.meshgrid(fx, fy)
    KX = 2*np.pi*FX; KY = 2*np.pi*FY
    kz_sq = k*k - KX*KX - KY*KY
    kz = np.sqrt(np.maximum(0.0, kz_sq))
    Hprop = np.exp(1j*kz*z)
    return np.fft.ifft2(np.fft.fft2(field0) * Hprop)

def sim_fresnel(mask_amp: np.ndarray, wavelength: float, dx: float, dy: float, z: float) -> np.ndarray:
    field = angular_spectrum(mask_amp, wavelength, dx, dy, z)
    return normalize01(np.abs(field))
