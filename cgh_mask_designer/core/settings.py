from dataclasses import dataclass, asdict
import json

@dataclass
class Settings:
    # Canvas / sampling
    width_px: int = 512
    height_px: int = 512
    um_per_px: float = 20.0

    # Mask area (mm), for export scaling
    mask_w_mm: float = 20.0
    mask_h_mm: float = 20.0

    # Illumination / optics
    wavelength_nm: float = 532.0
    model: str = "Fourier"  # or "Fresnel"
    focal_len_mm: float = 200.0  # Fourier default (4f focal length)
    distance_mm: float = 200.0   # Fresnel propagation distance

    # Encoding
    encoding: str = "Binary Density"  # "Binary Density" | "Size Modulation" | "Grayscale Density"
    use_halftone: bool = True
    grid_pitch_um: float = 50.0
    min_hole_um: float = 6.0
    max_hole_um: float = 25.0

    # Laser writer preview
    write_spot_um: float = 10.0  # Gaussian blur sigma is derived from FWHM

    # GS helper (experimental)
    use_gs_helper: bool = False
    gs_iters: int = 20

    # UI
    auto_update: bool = True

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
    @staticmethod
    def from_json(s: str) -> "Settings":
        return Settings(**json.loads(s))
