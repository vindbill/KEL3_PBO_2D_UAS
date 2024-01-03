# SortirDialog.py
from PyQt5.QtWidgets import QDialog, QRadioButton, QVBoxLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon

class SortirDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Pilihan Sortir')
        self.setWindowIcon(QIcon('logo galeri.png'))
        layout = QVBoxLayout()

        self.radio_button_alfabet = QRadioButton('Berdasarkan Alfabet')

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(self.radio_button_alfabet)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_selected_sort_option(self):
        if self.radio_button_alfabet.isChecked():
            return 'alfabet'
        else:
            return None
