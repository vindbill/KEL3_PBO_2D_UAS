# MainWindow.py
import mysql.connector
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QVBoxLayout, QListWidget, QPushButton,
    QFileDialog, QGridLayout, QHBoxLayout, QWidget, QListWidgetItem, QApplication
)
from PyQt5.QtGui import QPixmap, QTransform, QIcon
from PyQt5.QtCore import QTimer, QSize, pyqtSignal

from SortirDialog import SortirDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Semua Foto - Gallery')
        self.setWindowIcon(QIcon('logo galeri.png'))
        self.setToolTip('Gallery Foto Sederhana Connect Database')
        self.setGeometry(100, 100, 200, 100)

        self.label_gambar = QLabel(self)
        self.label_gambar = QLabel("Galeri Anda Kosong Coba Pilihlah Foto Agar Galeri Anda Menjadi Indah Seperti Dia ><", self)
        self.label_gambar.setObjectName('label_gambar')
        self.label_gambar.setAlignment(QtCore.Qt.AlignCenter)

        self.line_edit_gambar = QLineEdit(self)
        self.line_edit_gambar.setReadOnly(True)
        
        self.list_widget_gambar = QListWidget(self)

        self.slide_show_timer = QTimer(self)
        self.slide_show_timer.timeout.connect(self.next_gambar)

        self.slide_show_active = False
        
        self.list_widget_gambar.setMinimumHeight(80)
        self.list_widget_gambar.setMaximumHeight(100)
        self.list_widget_gambar.setIconSize(QSize(100, 50))
        font = self.list_widget_gambar.font()
        font.setPointSize(10)
        self.list_widget_gambar.setFont(font)

        self.line_edit_search = QLineEdit(self)
        self.line_edit_search.setPlaceholderText('Cari Gambar')
        self.line_edit_search.textChanged.connect(self.cari_gambar)

        self.button_bagian_folder = QPushButton('Tambah Folder', self)
        self.button_bagian_folder.clicked.connect(self.buka_jendela_bagian_folder)

        self.button_pilih_gambar = QPushButton('Pilih Gambar', self)
        self.button_pilih_gambar.clicked.connect(self.pilih_gambar)

        self.button_rotate_left = QPushButton('Putar Kiri', self)
        self.button_rotate_left.clicked.connect(self.rotate_left)

        self.button_rotate_right = QPushButton('Putar Kanan', self)
        self.button_rotate_right.clicked.connect(self.rotate_right)

        self.button_next = QPushButton('Next', self)
        self.button_next.clicked.connect(self.next_gambar)

        self.button_previous = QPushButton('Previous', self)
        self.button_previous.clicked.connect(self.previous_gambar)

        self.button_hapus = QPushButton('Hapus', self)
        self.button_hapus.clicked.connect(self.hapus_gambar)

        self.button_sortir = QPushButton('Sortir', self)
        self.button_sortir.clicked.connect(self.buka_jendela_sortir)

        self.button_slide_show = QPushButton('Slide Show / Stop Show', self)
        self.button_slide_show.clicked.connect(self.toggle_slide_show)
        
        self.list_widget_gambar.itemClicked.connect(self.item_gambar_dipilih)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.line_edit_search)

        layout = QVBoxLayout()

        image_layout = QVBoxLayout()

        image_layout.addWidget(self.button_bagian_folder)
        image_layout.addWidget(self.label_gambar)
        image_layout.addWidget(self.line_edit_gambar)

        layout.addLayout(search_layout)
        layout.addLayout(image_layout)
        layout.addWidget(self.list_widget_gambar)
        
        button_layout = QGridLayout()

        buttons = [
            self.button_pilih_gambar,
            self.button_slide_show,
            self.button_rotate_left,
            self.button_rotate_right,
            self.button_next,
            self.button_previous,
            self.button_hapus,
            self.button_sortir
        ]

        for i, btn in enumerate(buttons):
            row = i // 2
            col = i % 2
            button_layout.addWidget(btn, row, col)

        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.daftar_gambar = []
        self.indeks_tampil = 0

        #self.muat_indeks_terakhir()
        self.muat_gambar_dari_database()
        self.tampilkan_daftar_gambar()
        self.tampilkan_gambar()
#-------------------------------------------
#PENERIMA SINYAL 1--------------------------
    def update_image_list(self, new_image):
        self.daftar_gambar.append(new_image)
        self.tampilkan_daftar_gambar()
        self.simpan_path_gambar(new_image)
        self.muat_gambar_dari_database()
#-------------------------------------------
#PENERIMA SINYAL 2--------------------------------
    def hapus_gambar_dari_daftar(self, file_path):
        if file_path in self.daftar_gambar:
            self.daftar_gambar.remove(file_path)
            self.tampilkan_daftar_gambar()
            self.tampilkan_gambar()
#-------------------------------------------------
    def buka_jendela_bagian_folder(self):
        from BagianFolder import BagianFolder
        bagian_folder_dialog = BagianFolder(self)
        bagian_folder_dialog.show()

    def tampilkan_daftar_gambar(self):
        self.list_widget_gambar.clear()
        for gambar in self.daftar_gambar:
            item = QListWidgetItem(gambar)
            self.list_widget_gambar.addItem(item)
            
    def item_gambar_dipilih(self, item):
        index = self.list_widget_gambar.row(item)
        if 0 <= index < len(self.daftar_gambar):
            self.indeks_tampil = index
            self.tampilkan_gambar()
    
    def pilih_gambar(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Gambar (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        file_dialog.selectNameFilter("Gambar (*.png *.jpg *.jpeg *.bmp)")
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_name = file_dialog.selectedFiles()[0]
            self.daftar_gambar.append(file_name)
            self.indeks_tampil = len(self.daftar_gambar) - 1
            self.tampilkan_gambar()

            self.simpan_path_gambar(file_name)
            self.tampilkan_daftar_gambar()
            
            #self.sortir_nama_file()

    def simpan_path_gambar(self, file_path):
        import mysql.connector
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='galerilite'
        )

        cursor = connection.cursor()

        query = "INSERT INTO gambarinfo (file_path) VALUES (%s)"
        cursor.execute(query, (file_path,))
        connection.commit()

        cursor.close()
        connection.close()

    def muat_gambar_dari_database(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='galerilite'
        )

        cursor = connection.cursor()

        query = "SELECT file_path FROM gambarinfo"
        cursor.execute(query)

        rows = cursor.fetchall()
        if rows:
            self.daftar_gambar = [row[0] for row in rows]

        cursor.close()
        connection.close()

        self.all_images = self.daftar_gambar[:]

    def tampilkan_gambar(self):
        if self.daftar_gambar and self.indeks_tampil < len(self.daftar_gambar): #PENAMBAHAN AND DST
            pixmap = QPixmap(self.daftar_gambar[self.indeks_tampil])
            label_size = self.label_gambar.size()

            if not label_size.isEmpty():
                pixmap = pixmap.scaled(label_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                pixmap = pixmap.scaledToHeight(label_size.height(), QtCore.Qt.SmoothTransformation)

            self.label_gambar.setPixmap(pixmap)
            self.line_edit_gambar.setText(self.daftar_gambar[self.indeks_tampil])
        else:
            self.label_gambar.clear()
            self.line_edit_gambar.clear()
            self.label_gambar.setText("Galeri Anda Masih Kosong, Coba Pilihlah Foto Agar Galeri Anda Menjadi Indah Seperti Dia ><")

    def showEvent(self, event):
        super().showEvent(event)
        self.tampilkan_gambar()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.tampilkan_gambar()

    def rotate_left(self):
        self.rotate_image(-90)

    def rotate_right(self):
        self.rotate_image(90)

    def rotate_image(self, angle):
        if self.daftar_gambar:
            pixmap = QPixmap(self.daftar_gambar[self.indeks_tampil])
            pixmap = pixmap.transformed(QTransform().rotate(angle))

            label_size = self.label_gambar.size()
            if not label_size.isEmpty():
                pixmap = pixmap.scaled(label_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                pixmap = pixmap.scaledToHeight(label_size.height(), QtCore.Qt.SmoothTransformation)

            self.label_gambar.setPixmap(pixmap)

    def cari_gambar(self):
        search_text = self.line_edit_search.text().lower()

        if search_text:
            filtered_images = [image for image in self.daftar_gambar if search_text in image.lower()]
            if filtered_images:
                self.daftar_gambar = filtered_images
                self.indeks_tampil = 0
                self.tampilkan_gambar()
            else:
                self.label_gambar.clear()
                self.line_edit_gambar.clear()
                self.label_gambar.setText('Gambar tidak ditemukan')
        else:
            self.daftar_gambar = self.all_images
            self.indeks_tampil = 0
            self.tampilkan_gambar()

    def buka_jendela_sortir(self):
        sortir_dialog = SortirDialog(self)
        if sortir_dialog.exec_():
            selected_option = sortir_dialog.get_selected_sort_option()
            if selected_option == 'alfabet':
                self.sortir_nama_file()

    def sortir_nama_file(self):
        if self.daftar_gambar:
            self.daftar_gambar.sort()
            self.indeks_tampil = 0
            self.tampilkan_gambar()
            self.tampilkan_daftar_gambar()

    def toggle_slide_show(self):
        if not self.slide_show_active:
            self.start_slide_show()
        else:
            self.stop_slide_show()

    def start_slide_show(self):
        if self.daftar_gambar and not self.slide_show_active:
            print("Slide show started.")
            self.slide_show_active = True
            self.slide_show_timer.start(1000)

    def stop_slide_show(self):
        if self.slide_show_active:
            print("Slide show stopped.")
            self.slide_show_active = False
            self.slide_show_timer.stop()

    def next_gambar(self):
        if self.daftar_gambar:
            self.indeks_tampil = (self.indeks_tampil + 1) % len(self.daftar_gambar)
            self.tampilkan_gambar()

    def previous_gambar(self):
        if self.daftar_gambar:
            self.indeks_tampil = (self.indeks_tampil - 1 + len(self.daftar_gambar)) % len(self.daftar_gambar)
            self.tampilkan_gambar()

    def hapus_gambar(self):
        if self.daftar_gambar:
            file_path = self.daftar_gambar[self.indeks_tampil]
            self.hapus_gambar_dari_database(file_path)
            del self.daftar_gambar[self.indeks_tampil]
            if len(self.daftar_gambar) == 0:
                self.label_gambar.clear()
                self.line_edit_gambar.clear()
                self.label_gambar.setText('Galeri Anda Kosong Coba Pilihlah Foto Agar Galeri Anda Menjadi Indah Seperti Dia ><')
            else:
                if self.indeks_tampil >= len(self.daftar_gambar):
                    self.indeks_tampil = len(self.daftar_gambar) - 1
                self.tampilkan_gambar()
            
            self.tampilkan_daftar_gambar()

    def hapus_gambar_dari_database(self, file_path):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='galerilite'
        )
        
        cursor = connection.cursor()

        query = "DELETE FROM gambarinfo WHERE file_path = %s"
        cursor.execute(query, (file_path,))
        connection.commit()

        cursor.close()
        connection.close()


if __name__ == '__main__':
    app = QApplication([])

    with open('style.qss', 'r') as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    app.exec_()
