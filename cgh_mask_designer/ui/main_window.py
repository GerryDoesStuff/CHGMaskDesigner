from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt, QSettings, QRectF
from PyQt6.QtSvg import QSvgRenderer
import numpy as np

from ..core.settings import Settings
from ..core.image_utils import normalize01, to_qimage
from ..core.diffraction import sim_fourier, sim_fresnel
from ..core.encoding import floyd_steinberg_halftone, raster_size_modulation
from ..io.json_io import export_settings, import_settings
from ..io.svg_export import export_svg_pixels, export_svg_circles
from .image_pane import ImagePane
from .controls.target_panel import TargetPanel
from .controls.optics_panel import OpticsPanel
from .controls.encoding_panel import EncodingPanel
from .controls.io_panel import IOPanel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, st: Settings):
        super().__init__()
        self.setWindowTitle("CGH Mask Designer – modular")
        self.setMinimumSize(1100, 600)
        self.st = st
        self.target = np.zeros((self.st.height_px, self.st.width_px), dtype=np.float32)
        self.mask = np.zeros_like(self.target)
        self.recon = np.zeros_like(self.target)
        self._build_ui()
        self._load_qsettings()
        self.update_all()

    def _build_ui(self):
        central = QtWidgets.QWidget(); self.setCentralWidget(central)
        h = QtWidgets.QHBoxLayout(central)
        tabs = QtWidgets.QTabWidget(); h.addWidget(tabs, 0)

        self.target_panel = TargetPanel(self.st, self.maybe_auto)
        self.optics_panel = OpticsPanel(self.st, self.maybe_auto)
        self.encoding_panel = EncodingPanel(self.st, self.maybe_auto)
        self.io_panel = IOPanel(self.st, self.export_json, self.import_json, self.export_svg, self.save_previews)

        tabs.addTab(self.target_panel, "Target")
        tabs.addTab(self.optics_panel, "Optics")
        tabs.addTab(self.encoding_panel, "Encoding")
        tabs.addTab(self.io_panel, "I/O")

        right = QtWidgets.QVBoxLayout(); h.addLayout(right, 1)
        self.prev_target = ImagePane("Target / Mask domain")
        self.prev_recon = ImagePane("Reconstruction preview")
        right.addWidget(self.prev_target, 1)
        right.addWidget(self.prev_recon, 1)

        buttons = QtWidgets.QHBoxLayout()
        self.update_btn = QtWidgets.QPushButton("Update")
        self.auto_cb = QtWidgets.QCheckBox("Auto‑update"); self.auto_cb.setChecked(self.st.auto_update)
        buttons.addWidget(self.update_btn)
        buttons.addWidget(self.auto_cb)
        right.addLayout(buttons)

        self.update_btn.clicked.connect(self.update_all)
        self.auto_cb.toggled.connect(self.maybe_auto)

        # Wire a subset of controls for auto update
        for w in [
            self.target_panel.width_sb, self.target_panel.height_sb, self.target_panel.upp_dsb,
            self.target_panel.mask_w_dsb, self.target_panel.mask_h_dsb,
            self.optics_panel.model_cb, self.optics_panel.wl_dsb, self.optics_panel.focal_dsb, self.optics_panel.dist_dsb,
            self.encoding_panel.enc_cb, self.encoding_panel.halftone_cb, self.encoding_panel.pitch_dsb,
            self.encoding_panel.minhole_dsb, self.encoding_panel.maxhole_dsb, self.encoding_panel.spot_dsb,
        ]:
            if hasattr(w, 'valueChanged'):
                w.valueChanged.connect(self.maybe_auto)
            elif hasattr(w, 'currentIndexChanged'):
                w.currentIndexChanged.connect(self.maybe_auto)
            elif hasattr(w, 'toggled'):
                w.toggled.connect(self.maybe_auto)

        self.target_panel.load_btn.clicked.connect(self.load_target)

    def pull_settings(self):
        st = self.st
        st.width_px = int(self.target_panel.width_sb.value())
        st.height_px = int(self.target_panel.height_sb.value())
        st.um_per_px = float(self.target_panel.upp_dsb.value())
        st.mask_w_mm = float(self.target_panel.mask_w_dsb.value())/1000.0
        st.mask_h_mm = float(self.target_panel.mask_h_dsb.value())/1000.0
        st.model = self.optics_panel.model_cb.currentText()
        st.wavelength_nm = float(self.optics_panel.wl_dsb.value())
        st.focal_len_mm = float(self.optics_panel.focal_dsb.value())
        st.distance_mm = float(self.optics_panel.dist_dsb.value())
        st.encoding = self.encoding_panel.enc_cb.currentText()
        st.use_halftone = bool(self.encoding_panel.halftone_cb.isChecked())
        st.grid_pitch_um = float(self.encoding_panel.pitch_dsb.value())
        st.min_hole_um = float(self.encoding_panel.minhole_dsb.value())
        st.max_hole_um = float(self.encoding_panel.maxhole_dsb.value())
        st.write_spot_um = float(self.encoding_panel.spot_dsb.value())
        st.auto_update = bool(self.auto_cb.isChecked())

    def push_settings(self):
        st = self.st
        self.target_panel.width_sb.setValue(st.width_px)
        self.target_panel.height_sb.setValue(st.height_px)
        self.target_panel.upp_dsb.setValue(st.um_per_px)
        self.target_panel.mask_w_dsb.setValue(st.mask_w_mm*1000)
        self.target_panel.mask_h_dsb.setValue(st.mask_h_mm*1000)
        self.optics_panel.model_cb.setCurrentText(st.model)
        self.optics_panel.wl_dsb.setValue(st.wavelength_nm)
        self.optics_panel.focal_dsb.setValue(st.focal_len_mm)
        self.optics_panel.dist_dsb.setValue(st.distance_mm)
        self.encoding_panel.enc_cb.setCurrentText(st.encoding)
        self.encoding_panel.halftone_cb.setChecked(st.use_halftone)
        self.encoding_panel.pitch_dsb.setValue(st.grid_pitch_um)
        self.encoding_panel.minhole_dsb.setValue(st.min_hole_um)
        self.encoding_panel.maxhole_dsb.setValue(st.max_hole_um)
        self.encoding_panel.spot_dsb.setValue(st.write_spot_um)
        self.auto_cb.setChecked(st.auto_update)

    def _load_qsettings(self):
        qs = QSettings("CGHMaskDesigner", "Main")
        blob = qs.value("settings_json", "")
        if blob:
            try:
                self.st = Settings.from_json(blob)
                self.push_settings()
            except Exception:
                pass

    def _save_qsettings(self):
        qs = QSettings("CGHMaskDesigner", "Main")
        qs.setValue("settings_json", self.st.to_json())

    def closeEvent(self, event):
        self.pull_settings()
        self._save_qsettings()
        super().closeEvent(event)

    def export_json(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export settings", "settings.json", "JSON (*.json)")
        if fn:
            export_settings(fn, self.st)

    def import_json(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import settings", "", "JSON (*.json)")
        if fn:
            self.st = import_settings(fn)
            self.push_settings()
            self.update_all()

    def save_previews(self):
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder for PNGs")
        if not dir_: return
        QtGui.QImage(to_qimage(self.mask)).save(dir_ + "/mask_preview.png")
        QtGui.QImage(to_qimage(self.recon)).save(dir_ + "/reconstruction.png")

    def export_svg(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export SVG mask", "mask.svg", "SVG (*.svg)")
        if not fn: return
        H, W = self.mask.shape
        um_per_px = self.st.um_per_px
        if self.st.encoding == "Size Modulation":
            pitch = self.st.grid_pitch_um
            pitch_px = max(1.0, pitch / um_per_px)
            nx = int(W / pitch_px); ny = int(H / pitch_px)
            cx0 = (W - (nx-1)*pitch_px)/2 if nx>1 else W/2
            cy0 = (H - (ny-1)*pitch_px)/2 if ny>1 else H/2
            tar = normalize01(self.target)
            circles = []
            for j in range(ny):
                for i in range(nx):
                    cx = cx0 + i*pitch_px; cy = cy0 + j*pitch_px
                    ix = int(round(cy)); iy = int(round(cx))
                    ix = max(0, min(H-1, ix)); iy = max(0, min(W-1, iy))
                    val = float(tar[ix, iy])
                    d_um = self.st.min_hole_um + val*(self.st.max_hole_um - self.st.min_hole_um)
                    circles.append((cx*um_per_px, cy*um_per_px, 0.5*d_um))
            export_svg_circles(fn, circles)
        else:
            step = max(1, int(round(self.st.grid_pitch_um / um_per_px)))
            export_svg_pixels(fn, self.mask, um_per_px, step)

    def load_target(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open target image", "", "Images (*.png *.jpg *.bmp *.tif *.svg)")
        if not fn: return
        if fn.lower().endswith(".svg"):
            renderer = QSvgRenderer(fn)
            if not renderer.isValid():
                return
            img = QtGui.QImage(self.st.width_px, self.st.height_px, QtGui.QImage.Format.Format_ARGB32)
            img.fill(Qt.GlobalColor.white)
            painter = QtGui.QPainter(img)
            try:
                view_box = renderer.viewBoxF()
                if view_box.isEmpty():
                    default_size = renderer.defaultSize()
                    view_box = QRectF(0, 0, default_size.width(), default_size.height())
                if view_box.width() <= 0 or view_box.height() <= 0:
                    target_rect = QRectF(0, 0, img.width(), img.height())
                else:
                    scale = min(img.width() / view_box.width(), img.height() / view_box.height())
                    render_w = view_box.width() * scale
                    render_h = view_box.height() * scale
                    target_rect = QRectF(
                        (img.width() - render_w) / 2.0,
                        (img.height() - render_h) / 2.0,
                        render_w,
                        render_h,
                    )
                renderer.render(painter, target_rect)
            finally:
                painter.end()
            img = img.convertToFormat(QtGui.QImage.Format.Format_Grayscale8)
        else:
            img = QtGui.QImage(fn)
            if img.isNull(): return
            img = img.convertToFormat(QtGui.QImage.Format.Format_Grayscale8)
            img = img.scaled(self.st.width_px, self.st.height_px, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        ptr = img.bits(); ptr.setsize(img.height()*img.bytesPerLine())
        arr = np.frombuffer(ptr, np.uint8).reshape((img.height(), img.bytesPerLine()))[:, :img.width()].copy()
        self.target = arr.astype(np.float32)/255.0
        self.update_all()

    def maybe_auto(self, *args):
        if self.auto_cb.isChecked():
            self.update_all()
        elif self.sender() is self.auto_cb:
            self.pull_settings()
            self._save_qsettings()

    def update_all(self):
        self.pull_settings()
        if self.target.shape != (self.st.height_px, self.st.width_px):
            self.target = np.zeros((self.st.height_px, self.st.width_px), dtype=np.float32)
        if np.all(self.target == 0):
            yy, xx = np.mgrid[0:self.st.height_px, 0:self.st.width_px]
            cx, cy = self.st.width_px/2, self.st.height_px/2
            r = np.sqrt((xx-cx)**2 + (yy-cy)**2)
            self.target = np.exp(-0.5*(r/(0.2*min(self.st.width_px,self.st.height_px)))**2).astype(np.float32)
        tar = normalize01(self.target)

        if self.st.encoding == "Binary Density":
            src = tar
            if self.st.use_halftone:
                src = floyd_steinberg_halftone(src)
            mask_amp = (src > 0.5).astype(np.float32)
        elif self.st.encoding == "Grayscale Density":
            mask_amp = np.clip(tar, 0, 1)
        else:
            mask_amp = raster_size_modulation(tar, self.st.min_hole_um, self.st.max_hole_um, self.st.um_per_px, self.st.grid_pitch_um)

        if self.st.write_spot_um > 0:
            sigma_px = (self.st.write_spot_um/2.355) / self.st.um_per_px
            if sigma_px > 0.25:
                rad = max(3, int(3*sigma_px))
                yy, xx = np.mgrid[-rad:rad+1, -rad:rad+1]
                g = np.exp(-(xx*xx+yy*yy)/(2*sigma_px*sigma_px))
                g /= g.sum()
                F = np.fft.fft2(mask_amp)
                G = np.fft.fft2(g, s=mask_amp.shape)
                mask_vis = np.real(np.fft.ifft2(F*G))
                mask_vis = normalize01(mask_vis)
            else:
                mask_vis = mask_amp
        else:
            mask_vis = mask_amp

        wl = self.st.wavelength_nm * 1e-9
        dx = self.st.um_per_px * 1e-6
        if self.st.model == "Fourier":
            recon = sim_fourier(mask_amp)
        else:
            z = self.st.distance_mm * 1e-3
            recon = sim_fresnel(mask_amp, wl, dx, dx, z)

        self.mask = np.clip(mask_amp, 0, 1)
        self.recon = normalize01(recon)

        self.prev_target.set_array(self.mask)
        self.prev_recon.set_array(self.recon)
        self._save_qsettings()
