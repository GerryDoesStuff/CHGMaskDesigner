from PyQt6 import QtWidgets

class OpticsPanel(QtWidgets.QWidget):
    def __init__(self, st, on_change):
        super().__init__()
        self.st = st; self.on_change = on_change
        form = QtWidgets.QFormLayout(self)
        self.model_cb = QtWidgets.QComboBox(); self.model_cb.addItems(["Fourier","Fresnel"]) 
        self.wl_dsb = QtWidgets.QDoubleSpinBox(); self.wl_dsb.setRange(200.0, 2000.0); self.wl_dsb.setSuffix(" nm"); self.wl_dsb.setDecimals(1); self.wl_dsb.setValue(st.wavelength_nm)
        self.focal_dsb = QtWidgets.QDoubleSpinBox(); self.focal_dsb.setRange(10.0, 3000.0); self.focal_dsb.setSuffix(" mm"); self.focal_dsb.setDecimals(1); self.focal_dsb.setValue(st.focal_len_mm)
        self.dist_dsb = QtWidgets.QDoubleSpinBox(); self.dist_dsb.setRange(1.0, 5000.0); self.dist_dsb.setSuffix(" mm"); self.dist_dsb.setDecimals(1); self.dist_dsb.setValue(st.distance_mm)
        form.addRow("Model", self.model_cb)
        form.addRow("Wavelength", self.wl_dsb)
        form.addRow("Focal length (Fourier)", self.focal_dsb)
        form.addRow("Distance (Fresnel)", self.dist_dsb)
