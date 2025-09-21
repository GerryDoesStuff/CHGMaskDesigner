from typing import Tuple

import numpy as np


def _pad_for_oversample(field: np.ndarray, factor: int) -> np.ndarray:
    if factor == 1:
        return field
    h, w = field.shape
    pad_h, pad_w = h * factor, w * factor
    padded = np.zeros((pad_h, pad_w), dtype=field.dtype)
    y0 = (pad_h - h) // 2
    x0 = (pad_w - w) // 2
    padded[y0:y0 + h, x0:x0 + w] = field
    return padded

def fft2c(x):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))

def ifft2c(X):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X)))

def sim_fourier(mask_amp: np.ndarray, dx: float, oversample: bool = False) -> Tuple[np.ndarray, Tuple[float, float]]:
    """Simulate a Fourier reconstruction.

    Returns the complex field alongside the effective sampling pitch (dx, dy).
    """
    factor = 2 if oversample else 1
    padded = _pad_for_oversample(mask_amp, factor)
    field = fft2c(padded)
    eff_pitch = dx / factor
    return field, (eff_pitch, eff_pitch)

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

def sim_fresnel(
    mask_amp: np.ndarray,
    wavelength: float,
    dx: float,
    dy: float,
    z: float,
    oversample: bool = False,
) -> Tuple[np.ndarray, Tuple[float, float]]:
    """Simulate a Fresnel reconstruction with optional oversampling."""
    factor = 2 if oversample else 1
    padded = _pad_for_oversample(mask_amp, factor)
    field = angular_spectrum(padded, wavelength, dx, dy, z)
    eff_pitch = (dx / factor, dy / factor)
    return field, eff_pitch
