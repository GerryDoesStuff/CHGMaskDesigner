import numpy as np
from .image_utils import normalize01

def floyd_steinberg_halftone(img: np.ndarray) -> np.ndarray:
    a = img.copy().astype(np.float32)
    H, W = a.shape
    out = np.zeros_like(a)
    for y in range(H):
        if y % 2 == 0:
            xs = range(W); d = 1
        else:
            xs = range(W-1, -1, -1); d = -1
        for x in xs:
            old = a[y, x]
            new = 1.0 if old >= 0.5 else 0.0
            err = old - new
            out[y, x] = new
            nx = x + d
            if 0 <= nx < W:
                a[y, nx] += err * 7/16
            if y+1 < H:
                if x-1 >= 0: a[y+1, x-1] += err * 3/16
                a[y+1, x] += err * 5/16
                if x+1 < W: a[y+1, x+1] += err * 1/16
    return out

def raster_size_modulation(img: np.ndarray, min_d_um: float, max_d_um: float, um_per_px: float, pitch_um: float) -> np.ndarray:
    H, W = img.shape
    pitch_px = max(1.0, pitch_um / um_per_px)
    out = np.zeros_like(img, dtype=np.float32)
    nx = int(W / pitch_px); ny = int(H / pitch_px)
    cx0 = (W - (nx-1)*pitch_px)/2 if nx>1 else W/2
    cy0 = (H - (ny-1)*pitch_px)/2 if ny>1 else H/2
    yy, xx = np.mgrid[0:H, 0:W]
    for j in range(ny):
        for i in range(nx):
            cx = cx0 + i*pitch_px
            cy = cy0 + j*pitch_px
            iy = int(round(cx)); ix = int(round(cy))
            ix = np.clip(ix, 0, H-1); iy = np.clip(iy, 0, W-1)
            val = float(img[ix, iy])
            d_um = min_d_um + val*(max_d_um - min_d_um)
            r_px = 0.5 * (d_um / um_per_px)
            if r_px <= 0.5: continue
            rr2 = (xx-cx)**2 + (yy-cy)**2
            out = np.maximum(out, (rr2 <= r_px*r_px).astype(np.float32))
    return out
