from PyQt6 import QtWidgets

class IOPanel(QtWidgets.QWidget):
    def __init__(self, st, on_export_settings, on_import_settings, on_export_svg, on_save_pngs):
        super().__init__()
        lay = QtWidgets.QVBoxLayout(self)
        self.save_svg_btn = QtWidgets.QPushButton("Export Mask as SVG…")
        self.save_png_btn = QtWidgets.QPushButton("Save Previews (PNG)…")
        self.save_json_btn = QtWidgets.QPushButton("Export Settings (JSON)…")
        self.load_json_btn = QtWidgets.QPushButton("Import Settings (JSON)…")
        lay.addWidget(self.save_svg_btn)
        lay.addWidget(self.save_png_btn)
        lay.addWidget(self.save_json_btn)
        lay.addWidget(self.load_json_btn)
        lay.addStretch(1)
        self.save_svg_btn.clicked.connect(on_export_svg)
        self.save_png_btn.clicked.connect(on_save_pngs)
        self.save_json_btn.clicked.connect(on_export_settings)
        self.load_json_btn.clicked.connect(on_import_settings)
