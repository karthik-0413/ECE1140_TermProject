# announcement.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class AnnouncementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter the Announcement")
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Enter the announcement you want to display:")
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
