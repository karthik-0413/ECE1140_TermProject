# base_page.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt


class BasePage(QWidget):
    """Base class for all pages in the application."""

    def __init__(self, title, train_id_callback):
        super().__init__()

        # Set background color to very light gray
        self.setStyleSheet("background-color: #F5F5F5;")  # Very light gray

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 10, 0)  # Add margin to the right
        header_layout.setSpacing(0)

        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("""
            background-color: rgb(43,120,228);  /* Blue */
            padding: 5px 0;
        """)
        header_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Title label
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the title
        title_label.setFont(QFont('Arial', 32, QFont.Weight.Bold))

        # Dropdown menu
        dropdown_layout = QHBoxLayout()
        dropdown_layout.setSpacing(5)
        dropdown_layout.setContentsMargins(0, 0, 0, 0)
        train_id_label = QLabel("Train ID:")
        train_id_label.setFont(QFont('Arial', 14))
        self.train_id_combo = QComboBox()
        self.train_id_combo.setFixedWidth(60)
        self.train_id_combo.setStyleSheet("""
            QComboBox {
                color: black;
                border: 2px solid black;
                font-weight: bold;
            }
        """)
        # Connect action on Train ID change
        self.train_id_combo.currentTextChanged.connect(train_id_callback)

        # Add to dropdown_layout
        dropdown_layout.addWidget(train_id_label)
        dropdown_layout.addWidget(self.train_id_combo)
        dropdown_widget = QWidget()
        dropdown_widget.setLayout(dropdown_layout)

        # Add to header_layout
        header_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch()
        header_layout.addWidget(dropdown_widget, alignment=Qt.AlignmentFlag.AlignRight)

        # Add header_widget to main_layout
        main_layout.addWidget(header_widget)

        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Added margins to prevent hugging edges
        self.content_layout.setSpacing(0)
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

    def set_train_id_combo(self, train_id):
        """Set the current train ID in the combo box without emitting signals."""
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.setCurrentText(train_id)
        self.train_id_combo.blockSignals(False)

    def update_train_id_list(self, train_ids):
        """Update the train ID combo box with the new list."""
        current_id = self.train_id_combo.currentText()
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.clear()
        self.train_id_combo.addItems(train_ids)
        if current_id in train_ids:
            self.train_id_combo.setCurrentText(current_id)
        else:
            if train_ids:
                self.train_id_combo.setCurrentIndex(0)
            else:
                self.train_id_combo.setCurrentText('')
        self.train_id_combo.blockSignals(False)