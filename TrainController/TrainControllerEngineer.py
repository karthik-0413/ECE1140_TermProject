from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
import sys

class TrainEngineer:
    def __init__(self):
        self.trains = {
            1: {'kp': 0.0, 'ki': 0.0},
            2: {'kp': 0.0, 'ki': 0.0},
            3: {'kp': 0.0, 'ki': 0.0}
        }
        
    def set_kp(self, train_number, kp):
        self.trains[train_number]['kp'] = kp
        print(f"Train {train_number} Kp set to {kp}")
        
    def set_ki(self, train_number, ki):
        self.trains[train_number]['ki'] = ki
        print(f"Train {train_number} Ki set to {ki}")
        
    def get_kp(self, train_number):
        return self.trains[train_number]['kp']
    
    def get_ki(self, train_number):
        return self.trains[train_number]['ki']
    
class TrainEngineerUI(QWidget):
    def __init__(self, engineer):
        super().__init__()
        self.engineer = engineer
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Engineer View')
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add the bigger header
        header_label = QLabel("Engineer's View")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("background-color: #2B78E4; color: white; font-size: 20px; padding: 5px; margin-bottom: 0px;")
        layout.addWidget(header_label)
        
        self.table = QTableWidget(3, 3)
        self.table.setHorizontalHeaderLabels(['Train Number', 'Kp', 'Ki'])
        
        # Hide the vertical header to remove row numbers
        self.table.verticalHeader().hide()
        
        # Set header background color to grey (D3D3D3) and text color to black
        header = self.table.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #D3D3D3; color: black; }")
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Set the default stylesheet for the table items
        self.table.setStyleSheet("""
            QTableWidget { color: black; }
            QTableWidget::item { color: black; }
            QTableWidget::item:selected { color: black; }
            QTableWidget::item:editable { color: black; }
        """)

        
        self.update_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect the cellChanged signal to the slot
        self.table.cellChanged.connect(self.cell_changed)
        
    def update_table(self):
        for i, train_number in enumerate(self.engineer.trains.keys()):
            train_item = QTableWidgetItem(str(train_number))
            train_item.setFlags(train_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            train_item.setForeground(QBrush(QColor(0, 0, 0)))  # Set text color to black
            background_color = QColor("#9FC5F8") if i % 2 == 0 else QColor("#FFFFFF")  # Alternate row colors
            train_item.setBackground(QBrush(background_color))
            self.table.setItem(i, 0, train_item)
            
            kp_item = QTableWidgetItem(str(self.engineer.get_kp(train_number)))
            kp_item.setFlags(kp_item.flags() | Qt.ItemFlag.ItemIsEditable)
            kp_item.setForeground(QBrush(QColor(0, 0, 0)))  # Set text color to black
            kp_item.setBackground(QBrush(background_color))
            self.table.setItem(i, 1, kp_item)
            
            ki_item = QTableWidgetItem(str(self.engineer.get_ki(train_number)))
            ki_item.setFlags(ki_item.flags() | Qt.ItemFlag.ItemIsEditable)
            ki_item.setForeground(QBrush(QColor(0, 0, 0)))  # Set text color to black
            ki_item.setBackground(QBrush(background_color))
            self.table.setItem(i, 2, ki_item)
        
    def cell_changed(self, row, column):
        train_number = int(self.table.item(row, 0).text())
        if column == 1:  # Kp column
            try:
                kp = float(self.table.item(row, column).text())
                self.engineer.set_kp(train_number, kp)
                self.table.item(row, column).setForeground(QBrush(QColor(0, 0, 0)))  # Set text color to black
            except ValueError:
                pass
        elif column == 2:  # Ki column
            try:
                ki = float(self.table.item(row, column).text())
                self.engineer.set_ki(train_number, ki)
                self.table.item(row, column).setForeground(QBrush(QColor(0, 0, 0)))  # Set text color to black
            except ValueError:
                pass

if __name__ == "__main__":
    engineer = TrainEngineer()
    app = QApplication(sys.argv)
    ui = TrainEngineerUI(engineer)
    ui.show()
    sys.exit(app.exec())
