import numpy as np

def export_svg_pixels(path: str, mask: np.ndarray, um_per_px: float, step: int = 1):
    H, W = mask.shape
    width_um = W * um_per_px
    height_um = H * um_per_px
    ys, xs = np.where(mask > 0.5)
    with open(path, 'w') as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width_um}um' height='{height_um}um' viewBox='0 0 {width_um} {height_um}'>\n")
        f.write("  <g fill='black' stroke='none'>\n")
        for (y, x) in zip(ys[::step], xs[::step]):
            cx_um = x * um_per_px
            cy_um = y * um_per_px
            r_um = 0.5 * um_per_px
            f.write(f"    <circle cx='{cx_um:.3f}' cy='{cy_um:.3f}' r='{r_um:.3f}' />\n")
        f.write("  </g>\n</svg>\n")

def export_svg_circles(path: str, circles_um):
    # circles_um: iterable of (cx_um, cy_um, r_um)
    if not circles_um:
        circles_um = []
    width_um = max((c[0] for c in circles_um), default=0) * 1.02 + 100
    height_um = max((c[1] for c in circles_um), default=0) * 1.02 + 100
    with open(path, 'w') as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width_um}um' height='{height_um}um' viewBox='0 0 {width_um} {height_um}'>\n")
        f.write("  <g fill='black' stroke='none'>\n")
        for (cx, cy, r) in circles_um:
            f.write(f"    <circle cx='{cx:.3f}' cy='{cy:.3f}' r='{r:.3f}' />\n")
        f.write("  </g>\n</svg>\n")
