# announcement.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class AnnouncementDialog(QDialog):
    def __init__(self, train_index, parent=None):
        super().__init__(parent)
        self.train_index = train_index  # Store the train index
        self.setWindowTitle(f"Enter the Announcement for Train {train_index + 1}")
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()
        self.label = QLabel(f"Enter the announcement for Train {train_index + 1}:")
        self.label.setFont(QFont('Arial', 14))
        self.label.setStyleSheet("color: black;")
        layout.addWidget(self.label)

        self.text_edit = QLineEdit()
        self.text_edit.setFont(QFont('Arial', 14))
        self.text_edit.setStyleSheet("color: black;")
        layout.addWidget(self.text_edit)

        # OK Button with white background and black text
        self.ok_button = QPushButton("OK")
        self.ok_button.setFont(QFont('Arial', 14))
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def get_announcement(self):
        return self.text_edit.text()

    def get_train_index(self):
        return self.train_index
