import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class TableWidgetExample(QWidget):
    def __init__(self, data):
        super().__init__()
        
        self.setWindowTitle("QTableWidget with Predefined Data")
        self.setGeometry(100, 100, 400, 200)

        print(data)
        
        # Create a QTableWidget
        self.table_widget = QTableWidget(self)
        
        # Set the number of rows and columns based on the data
        rows = 1  # Since we're using one row
        columns = len(data)  # Number of columns equals the length of the data
        
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(columns)
        
        # Fill the table with the predefined array of integers
        for i, value in enumerate(data):
            item = QTableWidgetItem(value if value != None else 'None')
            self.table_widget.setItem(0, i, item)  # Set each item in the first row

        # Layout to hold the table
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

if __name__ == "__main__":
    # Predefined array of integers
    data = [None] * 10
    
    app = QApplication(sys.argv)
    window = TableWidgetExample(data)
    window.show()
    sys.exit(app.exec())
