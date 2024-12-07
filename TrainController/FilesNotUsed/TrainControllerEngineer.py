from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtCore import Qt, QSize
import sys

class TrainEngineer:
    def __init__(self):
        self._kp = 0.0
        self._ki = 0.0
        
    def set_kp(self, kp):
        self._kp = kp
        # # print(f"Kp set to {self._kp}")
        
    def set_ki(self, ki):
        self._ki = ki
        # # print(f"Ki set to {self._ki}")
        
    def get_kp(self):
        return self._kp
    
    def get_ki(self):
        return self._ki
    
class TrainEngineerUI(QWidget):
    def __init__(self, engineer):
        super().__init__()
        self.engineer = engineer
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Train Engineer Controller')
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        
        header_label = QLabel("Engineer's View")
        header_label.setStyleSheet("background-color: #2B78E4; color: white; font-size: 16px; padding: 5px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        
        self.table = QTableWidget(1, 3)
        self.table.setHorizontalHeaderLabels(['Train Number', 'Kp', 'Ki'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        train_number_item = QTableWidgetItem('1')  # Example train number
        train_number_item.setFlags(train_number_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable
        self.table.setItem(0, 0, train_number_item)
        
        self.table.setItem(0, 1, QTableWidgetItem(str(self.engineer.get_kp())))
        self.table.setItem(0, 2, QTableWidgetItem(str(self.engineer.get_ki())))
        self.table.itemChanged.connect(self.update_values)
        
        # Hide the number column to the left of the train number column
        self.table.verticalHeader().setVisible(False)
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
            }
            QTableWidget::item {
                color: black;
                background-color: #9FC5F8;
            }
            QTableWidget::item:alternate {
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #2B78E4;
                color: white;
            }
            QHeaderView::section {
                background-color: lightgrey;
                color: black;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.fill_empty_rows()
        
    def fill_empty_rows(self):
        # Calculate the number of rows that can fit in the available height
        row_height = self.table.verticalHeader().defaultSectionSize()
        available_height = self.table.viewport().height()
        num_rows = available_height // row_height
        
        # Add empty rows if needed
        current_row_count = self.table.rowCount()
        for _ in range(current_row_count, num_rows):
            self.table.insertRow(self.table.rowCount())
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fill_empty_rows()
        
    def update_values(self, item):
        row = item.row()
        col = item.column()
        
        if col == 1:  # Kp column
            try:
                kp = float(item.text())
                self.engineer.set_kp(kp)
            except ValueError:
                item.setText(str(self.engineer.get_kp()))  # Reset to previous value if invalid
        elif col == 2:  # Ki column
            try:
                ki = float(item.text())
                self.engineer.set_ki(ki)
            except ValueError:
                item.setText(str(self.engineer.get_ki()))  # Reset to previous value if invalid

if __name__ == "__main__":
    engineer = TrainEngineer()
    app = QApplication(sys.argv)
    ui = TrainEngineerUI(engineer)
    ui.show()
    sys.exit(app.exec())