import numpy as np
from .diffraction import ifft2c, fft2c, angular_spectrum
from .image_utils import normalize01

def gs_optimize(mask_amp: np.ndarray, target_amp: np.ndarray, iters: int, fourier: bool,
                wavelength: float, dx: float, dy: float, z: float) -> np.ndarray:
    field = target_amp * np.exp(1j*np.random.uniform(-np.pi, np.pi, size=target_amp.shape))
    for _ in range(max(1, int(iters))):
        if fourier:
            slm = ifft2c(field)
            slm = np.clip(np.abs(slm), 0, 1) * np.exp(1j*np.angle(slm))
            field = fft2c(slm)
        else:
            slm = angular_spectrum(field, wavelength, dx, dy, -z)
            slm = np.clip(np.abs(slm), 0, 1) * np.exp(1j*np.angle(slm))
            field = angular_spectrum(slm, wavelength, dx, dy, +z)
        field = target_amp * np.exp(1j*np.angle(field))
    if fourier:
        slm = ifft2c(field)
    else:
        slm = angular_spectrum(field, wavelength, dx, dy, -z)
    return np.clip(normalize01(np.abs(slm)), 0, 1)
