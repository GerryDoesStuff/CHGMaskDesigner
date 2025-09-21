from PyQt6 import QtWidgets

class TargetPanel(QtWidgets.QWidget):
    def __init__(self, st, on_change):
        super().__init__()
        self.st = st; self.on_change = on_change
        form = QtWidgets.QFormLayout(self)
        self.load_btn = QtWidgets.QPushButton("Load Target Image…")
        self.width_sb = QtWidgets.QSpinBox(); self.width_sb.setRange(64, 4096); self.width_sb.setValue(st.width_px)
        self.height_sb = QtWidgets.QSpinBox(); self.height_sb.setRange(64, 4096); self.height_sb.setValue(st.height_px)
        self.upp_dsb = QtWidgets.QDoubleSpinBox(); self.upp_dsb.setRange(0.5, 2000.0); self.upp_dsb.setDecimals(2); self.upp_dsb.setSuffix(" µm/px"); self.upp_dsb.setValue(st.um_per_px)
        self.mask_w_dsb = QtWidgets.QDoubleSpinBox(); self.mask_w_dsb.setRange(1.0, 60_000.0); self.mask_w_dsb.setSuffix(" µm"); self.mask_w_dsb.setDecimals(1); self.mask_w_dsb.setValue(st.mask_w_mm*1000)
        self.mask_h_dsb = QtWidgets.QDoubleSpinBox(); self.mask_h_dsb.setRange(1.0, 60_000.0); self.mask_h_dsb.setSuffix(" µm"); self.mask_h_dsb.setDecimals(1); self.mask_h_dsb.setValue(st.mask_h_mm*1000)
        form.addRow(self.load_btn)
        form.addRow("Canvas width", self.width_sb)
        form.addRow("Canvas height", self.height_sb)
        form.addRow("Sampling", self.upp_dsb)
        form.addRow("Mask width", self.mask_w_dsb)
        form.addRow("Mask height", self.mask_h_dsb)
