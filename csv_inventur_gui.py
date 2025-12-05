import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from csv_filter import filter_csv_blocks
import os

def resource_path(relative_path):
    if hasattr(sys, 'frozen'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

class CSVInventurTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSV Inventur Tool')
        # Icon aus img-Ordner laden, kompatibel mit PyInstaller
        icon_path = resource_path(os.path.join('img', 'KTN.F.svg'))
        self.setWindowIcon(QIcon(icon_path))
        self.resize(700, 500)
        self.data = []
        self.filtered_data = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel('Lade deine CSV-Datei hoch und starte die Inventur')
        self.info_label.setStyleSheet("color: #3FB498; font-weight: bold;")
        font = self.info_label.font()
        font.setPointSize(15)
        self.info_label.setFont(font)
        layout.addWidget(self.info_label)

        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton('CSV-Datei öffnen')
        self.open_btn.clicked.connect(self.open_file)
        btn_layout.addWidget(self.open_btn)
        self.export_btn = QPushButton('Als CSV exportieren')
        self.export_btn.clicked.connect(self.export_csv)
        self.export_btn.setEnabled(False)
        btn_layout.addWidget(self.export_btn)
        layout.addLayout(btn_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Suche nach Artikelnummer oder Artikel...')
        self.search_input.textChanged.connect(self.update_filter)
        self.count_label = QLabel('Gefundene Einträge: 0')
        self.count_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.count_label)
        self.search_input.setEnabled(False)
        layout.addWidget(self.search_input)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(['Art-Nummer', 'Artikel'])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'CSV-Datei auswählen', '', 'CSV Dateien (*.csv *.txt)')
        if not path:
            return
        with open(path, encoding='utf-8') as f:
            content = f.read()
        self.data = filter_csv_blocks(content)
        self.filtered_data = self.data.copy()
        self.update_table()
        self.info_label.setText(f'Ausgewählt: {path}')
        self.search_input.setEnabled(True)
        self.export_btn.setEnabled(True)

    def update_filter(self):
        term = self.search_input.text().lower()
        self.filtered_data = [item for item in self.data if term in item['kNummer'].lower() or term in item['artikel'].lower()]
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        for item in self.filtered_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item['kNummer']))
            self.table.setItem(row, 1, QTableWidgetItem(item['artikel']))

        self.count_label.setText(f"Gefundene Einträge: {len(self.filtered_data)}")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Als CSV exportieren', 'inventur_export.csv', 'CSV Dateien (*.csv)')
        if not path:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Artikel-Nummer', 'Artikel'])
            for item in self.filtered_data:
                writer.writerow([item['kNummer'], item['artikel']])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CSVInventurTool()
    win.show()
    sys.exit(app.exec_())
