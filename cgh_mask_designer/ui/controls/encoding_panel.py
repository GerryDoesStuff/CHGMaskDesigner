from PyQt6 import QtWidgets

class EncodingPanel(QtWidgets.QWidget):
    def __init__(self, st, on_change):
        super().__init__()
        self.st = st; self.on_change = on_change
        form = QtWidgets.QFormLayout(self)
        self.enc_cb = QtWidgets.QComboBox(); self.enc_cb.addItems(["Binary Density","Size Modulation","Grayscale Density"]) 
        self.halftone_cb = QtWidgets.QCheckBox("Use error‑diffusion halftoning")
        self.pitch_dsb = QtWidgets.QDoubleSpinBox(); self.pitch_dsb.setRange(2.0, 2000.0); self.pitch_dsb.setSuffix(" µm"); self.pitch_dsb.setDecimals(2); self.pitch_dsb.setValue(st.grid_pitch_um)
        self.minhole_dsb = QtWidgets.QDoubleSpinBox(); self.minhole_dsb.setRange(0.0, 2000.0); self.minhole_dsb.setSuffix(" µm"); self.minhole_dsb.setDecimals(2); self.minhole_dsb.setValue(st.min_hole_um)
        self.maxhole_dsb = QtWidgets.QDoubleSpinBox(); self.maxhole_dsb.setRange(0.0, 2000.0); self.maxhole_dsb.setSuffix(" µm"); self.maxhole_dsb.setDecimals(2); self.maxhole_dsb.setValue(st.max_hole_um)
        self.spot_dsb = QtWidgets.QDoubleSpinBox(); self.spot_dsb.setRange(0.0, 2000.0); self.spot_dsb.setSuffix(" µm (write spot)"); self.spot_dsb.setDecimals(2); self.spot_dsb.setValue(st.write_spot_um)
        form.addRow("Encoding mode", self.enc_cb)
        form.addRow(self.halftone_cb)
        form.addRow("Grid pitch", self.pitch_dsb)
        form.addRow("Min hole diameter", self.minhole_dsb)
        form.addRow("Max hole diameter", self.maxhole_dsb)
        form.addRow("Write spot (preview)", self.spot_dsb)
