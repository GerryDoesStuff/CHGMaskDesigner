# CGH Mask Designer (modular)

CGH Mask Designer is a modular PyQt6 application for creating polymer (or metal-on-glass) micro-aperture masks that form a desired 2D intensity pattern at a projection plane (wall/ceiling/floor) under laser illumination. It’s aimed at amplitude-only, rounded-aperture layouts etched on a glass slide (e.g., 20×20 mm), not 3D holograms.

# What it does

Converts a target image into a mask of rounded apertures using:

  Binary Density (with optional Floyd–Steinberg halftoning),

  Size Modulation (hole diameter encodes local intensity),

  Grayscale Density (for future processes that can do partial transmission).

  Simulates the resulting optical reconstruction with either:

  Fourier model (mask in a 4f system / lens present),

  Fresnel model (lensless propagation to a user-set distance).

# What it is not

It’s not a 3D hologram / phase-SLM tool; it targets amplitude masks with rounded apertures.

It doesn’t yet include process-calibrated compensation curves (diameter-to-transmission, etch bias).

# Live previews

Mask domain preview shows the aperture field.

Reconstruction preview shows the predicted intensity pattern at the selected plane (Fourier or Fresnel).

# Key parameters (all user-tunable)

Canvas size (px) and sampling (µm/px), mask area (up to 60×60 mm; default 20×20 mm).

Wavelength (defaults to 532 nm, adjustable).

Model: Fourier (with focal length) or Fresnel (with propagation distance).

Encoding mode: Binary Density, Size Modulation, Grayscale Density.

Fabrication constraints: grid pitch (µm), min/max hole diameter (µm).

Write-spot preview FWHM (µm) to reflect lithography/etch broadening.

Optional GS “helper” hooks exist in the core for later refinement, but the shipped UI focuses on amplitude encodings.

# I/O and persistence

JSON import/export of all settings (plus auto-persist between runs).

SVG export (units in µm) for the fabrication mask:

Size-modulation exports true circles at grid points with computed radii.

Density/grayscale mode exports pixel-sampled circles (step-thinned to keep files small).

PNG saves of both previews for documentation.

# Intended workflow

Load or set a target image and choose your encoding (start with Binary Density + halftoning for robustness).

Set mask sampling (µm/px), grid pitch, and min/max hole size to respect your process limits (e.g., 6–25 µm holes, 50 µm pitch).

Pick Fourier or Fresnel and set focal length or projection distance.

Inspect mask and reconstruction in the previews; tweak parameters to balance speckle, contrast, and manufacturability.

Export SVG for fabrication and JSON for reproducibility.

## Installation

### Prerequisites
- Python 3.10 or newer.
- `pip` (ships with modern Python distributions) and a virtual environment
  tool such as `python -m venv` or `conda` are recommended so the
  application's dependencies stay isolated from your system packages.

### Standard install
```bash
python -m pip install .
```

### Editable / development install
```bash
python -m pip install -e .
```

## Running
```bash
python -m cgh_mask_designer
```

The UI is powered by PyQt6. On Windows and macOS the required Qt libraries
are bundled with the PyPI wheels. On Linux you may need the system's Qt
platform plugins (e.g., XCB/Wayland packages) available so the application
can start.
