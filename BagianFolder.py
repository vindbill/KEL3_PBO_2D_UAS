# BagianFolder.py
import mysql.connector
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QWidget, QLabel,
    QGridLayout
)
from PyQt5.QtGui import QIcon, QPixmap, QTransform
from PyQt5.QtCore import QTimer, QSize, pyqtSignal

from SortirDialog import SortirDialog
from MainWindow import MainWindow

class BagianFolder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Folder')
        self.setWindowIcon(QIcon('logo galeri.png'))
        self.setGeometry(100, 100, 200, 100)
        
        self.counter_click = 0

        self.daftar_gambar = []

        layout = QVBoxLayout()
        # PENAMBAHAN UNTUK MENCARI FOLDER --------------------------------
        self.search_text = QLineEdit(self)
        self.search_text.setPlaceholderText('Cari Folder')
        self.search_text.textChanged.connect(self.on_search_changed)
        layout.addWidget(self.search_text)
        # ---------------------------------------------------------------
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText('Nama Folder')
        layout.addWidget(self.input_text)

        button_ok = QPushButton('Simpan', self)
        button_ok.clicked.connect(self.on_simpan_clicked)
        layout.addWidget(button_ok)

        self.folder_list_widget = QListWidget(self)
        #layout.addWidget(self.folder_list_widget)

        delete_button = QPushButton('Hapus Folder', self)
        delete_button.clicked.connect(self.on_hapus_clicked)
        layout.addWidget(delete_button)

        self.folder_list_widget.itemDoubleClicked.connect(self.on_folder_double_clicked)

        self.setLayout(layout)

        self.load_folders()
        
    def some_function_that_needs_MainWindow():
        from MainWindow import MainWindow
        main_window = MainWindow()

    def on_search_changed(self, text):
        search_text = self.search_text.text().lower()
        count = self.folder_list_widget.count()

        for i in range(count):
            item = self.folder_list_widget.item(i)
            if search_text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def load_folders(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='folder_galeri'
        )
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # for table in tables:
        #     folder_name = table[0]
        #     item = QListWidgetItem(folder_name) #PENAMBAHAN SETELAH MENAMBAH UNTUK MENCARI FOLDER
        #     item.setHidden(True) #PENAMBAHAN SETELAH MENAMBAH UNTUK MENCARI FOLDER
        #     self.folder_list_widget.addItem(item) #PERGANTIAN ATRIBUT FOLDER_NAME MENJADI ITEM

        connection.close()

    def on_simpan_clicked(self):
        self.counter_click += 1
        
        if self.counter_click == 1:
            input_text_value = self.input_text.text()
            print("Nilai Input:", input_text_value)

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='folder_galeri'
            )

            cursor = connection.cursor()

            create_table_query = f"CREATE TABLE IF NOT EXISTS {input_text_value} (id INT AUTO_INCREMENT PRIMARY KEY, file_path VARCHAR(255))"

            cursor.execute(create_table_query)
            connection.commit()

            cursor.close()
            connection.close()

            print(f"Tabel '{input_text_value}' berhasil dibuat.")

            if input_text_value:
                item = QListWidgetItem(input_text_value)
                self.folder_list_widget.addItem(item)
                
            elif self.counter_click == 2:
                self.folder_list_window()

            self.input_text.clear()
        
        #self.accept() #TIDAK WAJIB NOTE: BERFUNGSI UNTUK MENUTUP JENDELA SETELAH MELAKUKAN KEGIATAN TERTENTU
    
    def folder_list_window(self):
        folder_list_window = QDialog()
        folder_list_window.setWindowTitle('Daftar List Folder')
        folder_list_window.setGeometry(200, 200, 300, 200)

        # Layout untuk jendela baru
        layout = QVBoxLayout()

        # Menambahkan daftar list folder ke dalam QListWidget di jendela baru
        folder_list_widget = QListWidget()
        for index in range(self.folder_list_widget.count()):
            item = self.folder_list_widget.item(index)
            folder_list_widget.addItem(item.text())

        layout.addWidget(folder_list_widget)
        folder_list_window.setLayout(layout)

        # Tampilkan jendela baru
        folder_list_window.exec_()
    
    def on_hapus_clicked(self):
        selected_item = self.folder_list_widget.currentItem()
        if selected_item is not None:
            folder_name = selected_item.text()
            confirmation = QMessageBox.question(self, 'Hapus Folder', f'Anda yakin ingin menghapus folder {folder_name}?',
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.hapus_folder(folder_name)

    def hapus_folder(self, folder_name):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='folder_galeri'
        )
        cursor = connection.cursor()

        drop_table_query = f"DROP TABLE IF EXISTS {folder_name}"
        cursor.execute(drop_table_query)
        connection.commit()

        current_row = self.folder_list_widget.currentRow()
        self.folder_list_widget.takeItem(current_row)

        cursor.close()
        connection.close()

    def on_folder_double_clicked(self, item):
        folder_name = item.text()
        self.sub_window = QWidget() #PENAMBAHAN SELF
        
        self.sub_window.setWindowTitle(f'Detail Folder: {folder_name}') #PENAMBAHAN SELF
        self.sub_window.setWindowIcon(QIcon('logo galeri.png'))
        self.setGeometry(100, 100, 200, 100)
        self.is_maximized = False

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

        layout = QGridLayout()
        layout.addWidget(self.line_edit_search, 0, 0, 1, 2)
        layout.addWidget(self.label_gambar, 1, 0, 1, 2)
        layout.addWidget(self.line_edit_gambar, 2, 0, 1, 2)
        layout.addWidget(self.list_widget_gambar, 3, 0, 1, 2)
        layout.addWidget(self.button_pilih_gambar, 4, 0)
        layout.addWidget(self.button_slide_show, 4, 1)
        layout.addWidget(self.button_rotate_left, 5, 0)
        layout.addWidget(self.button_rotate_right, 5, 1)
        layout.addWidget(self.button_next, 6, 0)
        layout.addWidget(self.button_previous, 6, 1)
        layout.addWidget(self.button_hapus, 7, 0)
        layout.addWidget(self.button_sortir, 7, 1)
        
        self.sub_window.setLayout(layout) #PENAMBAHAN SELF
        self.sub_window.resize(400, 300) #PENAMBAHAN SELF

        self.daftar_gambar = []
        self.indeks_tampil = 0

        self.muat_gambar_dari_database(folder_name)
        self.tampilkan_gambar()
        self.tampilkan_daftar_gambar()

        self.sub_window.show() #PENAMBAHAN SELF

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
            selected_item = self.folder_list_widget.currentItem()
            if selected_item is not None:
                folder_name = selected_item.text()
                self.daftar_gambar.append(file_name)
                self.indeks_tampil = len(self.daftar_gambar) - 1
                self.tampilkan_gambar()
                
                self.simpan_path_gambar(file_name, folder_name)
                self.tampilkan_daftar_gambar()
                
                #self.sortir_nama_file()

    def simpan_path_gambar(self, file_path, folder_name):
        connection1 = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='folder_galeri'
        )
        cursor = connection1.cursor()

        query = f"INSERT INTO {folder_name} (file_path) VALUES (%s)"
        cursor.execute(query, (file_path,))
        connection1.commit()

        cursor.close()
        connection1.close()
    #PEMBERIAN KODE PADA JENDELA MAINWINDOW AGAR BERTAMBAH FOTO JUGA (SINYAL 1)
        parent_window = self.parent()
        if parent_window:
            parent_window.update_image_list(file_path)
    #--------------------------------------------------------------------------
    def muat_gambar_dari_database(self, folder_name):
        connection1 = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='folder_galeri'
        )

        cursor = connection1.cursor()

        query = f"SELECT file_path FROM {folder_name}"
        cursor.execute(query)

        rows = cursor.fetchall()
        self.daftar_gambar = [row[0] for row in rows]

        cursor.close()
        connection1.close()

    def tampilkan_gambar(self):
        if hasattr(self, 'label_gambar') and self.daftar_gambar:
            pixmap = QPixmap(self.daftar_gambar[self.indeks_tampil])
            label_size = self.label_gambar.size()

            if not label_size.isEmpty():
                pixmap = pixmap.scaled(label_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                pixmap = pixmap.scaledToHeight(label_size.height(), QtCore.Qt.SmoothTransformation)

            self.label_gambar.setPixmap(pixmap)
            self.label_gambar.setAlignment(QtCore.Qt.AlignCenter)
            self.line_edit_gambar.setText(self.daftar_gambar[self.indeks_tampil])

            self.label_gambar.showMaximized()
        elif hasattr(self, 'label_gambar'):
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
            selected_item = self.folder_list_widget.currentItem()
            if selected_item is not None:
                folder_name = selected_item.text()
                self.hapus_gambar_dari_database(file_path, folder_name)
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
        #PEMBERIAN KODE PADA JENDELA MAINWINDOW AGAR FOTO TERHAPUS JUGA (SINYAL 2)
            parent_window = self.parent()
            if isinstance(parent_window, MainWindow):
                parent_window.hapus_gambar_dari_daftar(file_path)
                parent_window.hapus_gambar_dari_database(file_path)
        #-------------------------------------------------------------------------
    def hapus_gambar_dari_database(self, file_path, folder_name):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='folder_galeri'
        )

        cursor = connection.cursor()

        query = f"DELETE FROM {folder_name} WHERE file_path = %s"
        cursor.execute(query, (file_path,))
        connection.commit()
        
        cursor.close()
        connection.close()
        pass