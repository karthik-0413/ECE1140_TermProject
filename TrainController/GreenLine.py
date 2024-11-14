import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class TrackBlock:
    def __init__(self, line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, seconds_to_traverse):
        self.line = line
        self.section = section
        self.block_number = block_number
        self.block_length = block_length
        self.block_grade = block_grade
        self.speed_limit = speed_limit
        self.infrastructure = infrastructure
        self.station_side = station_side
        self.elevation = elevation
        self.cumulative_elevation = cumulative_elevation
        self.seconds_to_traverse = seconds_to_traverse

def read_excel_to_array(file_path):
    df = pd.read_excel(file_path)
    track_blocks = []
    for _, row in df.iterrows():
        block = TrackBlock(
            line=row['Line'],
            section=row['Section'],
            block_number=row['Block Number'],
            block_length=row['Block Length'],
            block_grade=row['Block Grade'],
            speed_limit=row['Speed Limit'],
            infrastructure=row['Infrastructure'],
            station_side=row['Station Side'],
            elevation=row['Elevation'],
            cumulative_elevation=row['Cumulative Elevation'],
            seconds_to_traverse=row['Seconds to Traverse']
        )
        track_blocks.append(block)
    return track_blocks

class TrackTable(QWidget):
    def __init__(self, track_blocks):
        super().__init__()
        self.setWindowTitle("Track Layout")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(len(track_blocks))
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "Line", "Section", "Block Number", "Block Length", "Block Grade", 
            "Speed Limit", "Infrastructure", "Station Side", "Elevation", 
            "Cumulative Elevation", "Seconds to Traverse"
        ])
        for i, block in enumerate(track_blocks):
            self.table.setItem(i, 0, QTableWidgetItem(block.line))
            self.table.setItem(i, 1, QTableWidgetItem(block.section))
            self.table.setItem(i, 2, QTableWidgetItem(str(block.block_number)))
            self.table.setItem(i, 3, QTableWidgetItem(str(block.block_length)))
            self.table.setItem(i, 4, QTableWidgetItem(str(block.block_grade)))
            self.table.setItem(i, 5, QTableWidgetItem(str(block.speed_limit)))
            self.table.setItem(i, 6, QTableWidgetItem(block.infrastructure))
            self.table.setItem(i, 7, QTableWidgetItem(block.station_side))
            self.table.setItem(i, 8, QTableWidgetItem(str(block.elevation)))
            self.table.setItem(i, 9, QTableWidgetItem(str(block.cumulative_elevation)))
            self.table.setItem(i, 10, QTableWidgetItem(str(block.seconds_to_traverse)))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_path = '/path/to/your/excel/file.xlsx'  # Update this path to your Excel file
    track_blocks = read_excel_to_array(file_path)
    window = TrackTable(track_blocks)
    window.show()
    sys.exit(app.exec())