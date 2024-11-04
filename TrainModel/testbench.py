# testbench.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QPushButton, QLineEdit, QComboBox, QWidget, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt

from base_page import BasePage
from announcement import AnnouncementDialog
from power_dialog import SetCommandedPowerDialog


class TestBenchPage(BasePage):
    """Page representing the Test Bench for Train Control Inputs."""

    def __init__(self, train_data, train_id_callback):
        super().__init__("                                 Test Bench", train_id_callback)
        self.train_data = train_data  # Store the train data

        self.current_train_index = 0  # Default to first train

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget and vertical layout inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F5F5;")

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setContentsMargins(10, 0, 10, 10)
        main_vertical_layout.setSpacing(5)
        main_vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.font_label = QFont('Arial', 13)  # Increased by 1
        self.font_label.setBold(True)
        self.font_value = QFont('Arial', 13)  # Increased by 1

        self.tc_edit_fields = {}
        self.cabin_edit_fields = {}

        # Main horizontal layout to place tables side by side
        main_horizontal_layout = QHBoxLayout()
        main_horizontal_layout.setSpacing(20)

        # Train Control Input Section
        tc_section_layout = QVBoxLayout()
        tc_section_layout.setSpacing(5)

        tc_title = QLabel("Train Control Input")
        tc_title.setFont(QFont('Arial', 17, QFont.Weight.Bold))  # Increased by 1
        tc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tc_title.setStyleSheet("color: black;")

        tc_input_layout = QGridLayout()
        tc_input_layout.setSpacing(5)
        tc_input_layout.setHorizontalSpacing(10)  # Adjusted horizontal spacing
        tc_input_layout.setContentsMargins(0, 0, 0, 0)

        tc_data_items = [
            ("Commanded Power(kw)", "commanded_power"),
            ("Commanded Speed(km/h)", "commanded_speed_tc"),
            ("Authority(m)", "authority"),
            ("Service Brake", "service_brake"),
            ("Exterior Light", "exterior_light"),
            ("Interior Light", "interior_light"),
            ("Emergency Brake", "emergency_brake"),
            ("Beacon", "beacon"),
            ("Train Count", "train_count"),  # Added train count
        ]

        for i, (label_text, var_name, *rest) in enumerate(tc_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["service_brake", "exterior_light", "interior_light", "emergency_brake"]:
                # Use a button for ON/OFF
                button = QPushButton("OFF")
                button.setCheckable(True)
                button.setFont(self.font_value)
                button.setFixedWidth(80)
                button.clicked.connect(lambda checked, var=var_name, btn=button: self.toggle_on_off(var, btn))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = button
            elif var_name == "beacon":
                # Use a combo box for beacon with "We are approaching"
                station_combo = QComboBox()
                station_combo.addItems(["Station Alpha", "Station Beta", "Station Delta"])
                if self.train_data.train_count > 0:
                    station_combo.setCurrentText(self.train_data.beacon_station[self.current_train_index] if self.train_data.beacon_station else "Station Alpha")
                else:
                    station_combo.setCurrentText("Station Alpha")
                station_combo.setFont(self.font_value)
                station_combo.setStyleSheet("color: black;")
                station_combo.currentTextChanged.connect(self.update_beacon)
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                beacon_layout = QHBoxLayout()
                prefix_label = QLabel("We are approaching")
                prefix_label.setFont(self.font_value)
                prefix_label.setStyleSheet("color: black;")
                beacon_layout.addWidget(prefix_label)
                beacon_layout.addWidget(station_combo)

                tc_input_layout.addLayout(beacon_layout, i, 1)
                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields["beacon_station"] = station_combo
            elif var_name == "commanded_power":
                # Replace QLineEdit and OK button with a single button to open a popup
                set_power_button = QPushButton("Set Commanded Power")
                set_power_button.setFont(self.font_value)
                set_power_button.setFixedWidth(200)
                set_power_button.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border-radius: 5px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #0b7dda;
                    }
                """)
                set_power_button.clicked.connect(self.open_set_commanded_power_dialog)
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(set_power_button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = set_power_button
            elif var_name == "train_count":
                # Numeric input for modifying train count
                value = self.train_data.train_count
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                # Create a horizontal layout for input field and OK button
                input_layout = QHBoxLayout()
                input_layout.setContentsMargins(0, 0, 0, 0)
                input_layout.setSpacing(5)
                input_layout.addWidget(value_edit)

                ok_button = QPushButton("OK")
                ok_button.setFont(self.font_value)
                ok_button.setFixedWidth(50)
                ok_button.setStyleSheet("""
                    QPushButton {
                        color: black;
                        border: 2px solid black;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #E0E0E0;
                    }
                """)
                ok_button.clicked.connect(lambda _, var=var_name, edit=value_edit: self.update_train_count(var, edit.text()))
                input_layout.addWidget(ok_button)

                tc_input_layout.addLayout(input_layout, i, 1)

                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = value_edit
            else:
                # Numeric inputs
                value = getattr(self.train_data, var_name)[self.current_train_index] if getattr(self.train_data, var_name) else 0
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")  # Ensuring black font color
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                tc_input_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                tc_input_layout.addWidget(value_edit, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                tc_input_layout.addWidget(unit_label, i, 2, alignment=Qt.AlignmentFlag.AlignLeft)
                self.tc_edit_fields[var_name] = value_edit

        tc_section_layout.addWidget(tc_title)
        tc_section_layout.addLayout(tc_input_layout)

        # Train Control Input Widget
        tc_input_widget = QWidget()
        tc_input_widget.setLayout(tc_section_layout)
        tc_input_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Cabin Control Section
        cabin_section_layout = QVBoxLayout()
        cabin_section_layout.setSpacing(5)

        cabin_title = QLabel("Cabin Control")
        cabin_title.setFont(QFont('Arial', 17, QFont.Weight.Bold))  # Increased by 1
        cabin_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cabin_title.setStyleSheet("color: black;")

        cabin_control_layout = QGridLayout()
        cabin_control_layout.setSpacing(5)
        cabin_control_layout.setHorizontalSpacing(10)  # Adjusted horizontal spacing
        cabin_control_layout.setContentsMargins(0, 0, 0, 0)

        cabin_data_items = [
            ("Desired Temperature", "desired_temperature", "°F"),
            ("Train Left Door", "train_left_door"),
            ("Train Right Door", "train_right_door"),
            ("Advertisement", "advertisement", ["Picture1", "Picture2", "Picture3"]),
            ("Passenger Boarding", "passenger_boarding", ""),
        ]

        for i, (label_text, var_name, *rest) in enumerate(cabin_data_items):
            label = QLabel(label_text)
            label.setFont(self.font_label)
            label.setStyleSheet("color: black;")

            if var_name in ["train_left_door", "train_right_door"]:
                # Use a button for ON/OFF
                button = QPushButton("OFF")
                button.setCheckable(True)
                button.setFont(self.font_value)
                button.setFixedWidth(80)
                button.clicked.connect(lambda checked, var=var_name, btn=button: self.toggle_on_off(var, btn))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                cabin_control_layout.addWidget(button, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                cabin_control_layout.addWidget(unit_label, i, 2)
                self.cabin_edit_fields[var_name] = button
            elif var_name == "advertisement":
                # Use a combo box for advertisement
                options = rest[0]
                combo_box = QComboBox()
                combo_box.addItems(options)
                if self.train_data.train_count > 0:
                    combo_box.setCurrentText(self.train_data.advertisement[self.current_train_index] if self.train_data.advertisement else options[0])
                else:
                    combo_box.setCurrentText(options[0])
                combo_box.setFont(self.font_value)
                combo_box.setStyleSheet("color: black;")
                combo_box.currentTextChanged.connect(lambda text, var=var_name: self.update_train_data(var, text))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
                cabin_control_layout.addWidget(combo_box, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                cabin_control_layout.addWidget(unit_label, i, 2)
                self.cabin_edit_fields[var_name] = combo_box
            elif var_name == "passenger_boarding":
                # Numeric input with OK button
                value = self.train_data.passenger_boarding[self.current_train_index] if self.train_data.passenger_boarding else 0
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")  # Ensuring black font color
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                # Create a horizontal layout for input field and OK button
                input_layout = QHBoxLayout()
                input_layout.setContentsMargins(0, 0, 0, 0)
                input_layout.setSpacing(5)
                input_layout.addWidget(value_edit)

                ok_button = QPushButton("OK")
                ok_button.setFont(self.font_value)
                ok_button.setFixedWidth(50)
                ok_button.setStyleSheet("""
                    QPushButton {
                        color: black;
                        border: 2px solid black;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #E0E0E0;
                    }
                """)
                ok_button.clicked.connect(lambda _, var=var_name, edit=value_edit: self.update_passenger_boarding(var, edit.text()))
                input_layout.addWidget(ok_button)

                cabin_control_layout.addLayout(input_layout, i, 1)

                unit_label = QLabel("")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                cabin_control_layout.addWidget(unit_label, i, 2)
                self.cabin_edit_fields[var_name] = value_edit
            else:
                # Numeric inputs with unit label next to input field
                value = self.train_data.desired_temperature[self.current_train_index] if self.train_data.desired_temperature else 0
                value_edit = QLineEdit(str(value))
                value_edit.setFont(self.font_value)
                value_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centered text
                value_edit.setMaximumWidth(80)
                value_edit.setStyleSheet("color: black;")  # Ensuring black font color
                value_edit.editingFinished.connect(lambda var=var_name, edit=value_edit: self.update_train_data(var, edit.text()))
                cabin_control_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)

                # Create a horizontal layout for input field and unit label
                input_layout = QHBoxLayout()
                input_layout.setContentsMargins(0, 0, 0, 0)
                input_layout.setSpacing(5)
                input_layout.addWidget(value_edit)

                unit_label = QLabel(rest[0] if rest else "")
                unit_label.setFont(self.font_label)
                unit_label.setStyleSheet("color: black;")
                input_layout.addWidget(unit_label)

                cabin_control_layout.addLayout(input_layout, i, 1)
                self.cabin_edit_fields[var_name] = value_edit

        cabin_section_layout.addWidget(cabin_title)
        cabin_section_layout.addLayout(cabin_control_layout)

        # Cabin Control Widget
        cabin_control_widget = QWidget()
        cabin_control_widget.setLayout(cabin_section_layout)
        cabin_control_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Add both widgets to the horizontal layout
        main_horizontal_layout.addWidget(tc_input_widget)
        main_horizontal_layout.addWidget(cabin_control_widget)

        main_vertical_layout.addLayout(main_horizontal_layout)

        # Announcement Button (moved below the tables)
        announcement_button = QPushButton("Announcement")
        announcement_button.setFont(QFont('Arial', 15, QFont.Weight.Bold))  # Increased by 1
        announcement_button.setFixedSize(200, 50)
        announcement_button.setStyleSheet("""
            QPushButton {
                border: 2px solid black;
                background-color: #F0F0F0;
                color: black;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        announcement_button.clicked.connect(self.open_announcement_dialog)

        # Center the Announcement button
        announcement_layout = QHBoxLayout()
        announcement_layout.addStretch()
        announcement_layout.addWidget(announcement_button)
        announcement_layout.addStretch()

        main_vertical_layout.addLayout(announcement_layout)

        # Set content widget layout
        content_widget.setLayout(main_vertical_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to content_layout
        self.content_layout.addWidget(scroll_area)

        # Initialize button states
        self.update_button_states()

        # Update the displays when data changes
        self.train_data.data_changed.connect(self.update_display)

    def train_id_changed(self, new_train_id):
        """Handle Train ID change."""
        if new_train_id:
            self.current_train_index = int(new_train_id) - 1
            self.update_display()

    def update_train_id_list(self, train_ids):
        """Update the train ID combo box with the new list."""
        current_id = self.train_id_combo.currentText()
        self.train_id_combo.blockSignals(True)
        self.train_id_combo.clear()
        self.train_id_combo.addItems(train_ids)
        if current_id in train_ids:
            self.train_id_combo.setCurrentText(current_id)
            self.current_train_index = int(current_id) - 1
        else:
            if train_ids:
                self.train_id_combo.setCurrentIndex(0)
                self.current_train_index = 0
            else:
                self.current_train_index = None
        self.train_id_combo.blockSignals(False)
        self.update_display()

    def toggle_on_off(self, var_name, button):
        is_on = button.isChecked()
        button.setText("ON" if is_on else "OFF")
        # Use the same green color as in Train Model page
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'green' if is_on else 'lightgray'};
                color: black;
                font-weight: bold;
            }}
        """)
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            return
        getattr(self.train_data, var_name)[index] = is_on
        self.train_data.data_changed.emit()

    def open_set_commanded_power_dialog(self):
        if self.current_train_index is not None and self.current_train_index < self.train_data.train_count:
            current_power = self.train_data.commanded_power[self.current_train_index]
        else:
            current_power = 0
        dialog = SetCommandedPowerDialog(self, current_power=current_power)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_power = dialog.get_commanded_power()
            if new_power is not None:
                index = self.current_train_index
                self.train_data.commanded_power[index] = new_power
                self.train_data.data_changed.emit()

    def update_train_data(self, var_name, value):
        index = self.current_train_index
        try:
            if index is None or index >= self.train_data.train_count:
                return
            if var_name in ['commanded_speed_tc', 'authority', 'desired_temperature']:
                current_value = getattr(self.train_data, var_name)[index]
                if isinstance(current_value, int):
                    value = int(value)
                elif isinstance(current_value, float):
                    value = float(value)
            getattr(self.train_data, var_name)[index] = value
            self.train_data.data_changed.emit()
        except ValueError:
            pass  # Handle invalid input as desired

    def update_passenger_boarding(self, var_name, value):
        index = self.current_train_index
        try:
            if index is None or index >= self.train_data.train_count:
                return
            value = int(value)
            self.train_data.passenger_boarding[index] = value
            self.train_data.passenger_count[index] += value
            self.train_data.passenger_boarding[index] = 0  # Reset to 0
            self.train_data.update_train_weight(index)
            self.train_data.data_changed.emit()
        except ValueError:
            pass  # Handle invalid input

    def update_beacon(self, station):
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            return
        self.train_data.beacon_station[index] = station
        self.train_data.data_changed.emit()

    def open_announcement_dialog(self):
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            return
        dialog = AnnouncementDialog(index, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            announcement = dialog.get_announcement()
            self.train_data.announcement_text[index] = announcement
            self.train_data.data_changed.emit()

    def update_button_states(self):
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            # Disable buttons and inputs if no train is selected
            for widget in self.tc_edit_fields.values():
                widget.setEnabled(False)
            for widget in self.cabin_edit_fields.values():
                widget.setEnabled(False)
            return

        for widget in self.tc_edit_fields.values():
            widget.setEnabled(True)
        for widget in self.cabin_edit_fields.values():
            widget.setEnabled(True)

        for var_name, button in self.tc_edit_fields.items():
            if var_name in ["service_brake", "exterior_light", "interior_light", "emergency_brake"]:
                is_on = getattr(self.train_data, var_name)[index]
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                        font-weight: bold;
                    }}
                """)
        for var_name, button in self.cabin_edit_fields.items():
            if var_name in ["train_left_door", "train_right_door"]:
                is_on = getattr(self.train_data, var_name)[index]
                button.setChecked(is_on)
                button.setText("ON" if is_on else "OFF")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {'green' if is_on else 'lightgray'};
                        color: black;
                        font-weight: bold;
                    }}
                """)

    def update_display(self):
        index = self.current_train_index
        if index is None or index >= self.train_data.train_count:
            # Disable inputs if no valid train is selected
            for widget in self.tc_edit_fields.values():
                widget.setEnabled(False)
            for widget in self.cabin_edit_fields.values():
                widget.setEnabled(False)
            return
        else:
            for widget in self.tc_edit_fields.values():
                widget.setEnabled(True)
            for widget in self.cabin_edit_fields.values():
                widget.setEnabled(True)

        # Update the state of the buttons and input fields
        self.update_button_states()
        # Update numeric input fields
        for var_name in ['commanded_speed_tc', 'authority']:
            edit = self.tc_edit_fields.get(var_name)
            if edit:
                value = getattr(self.train_data, var_name)[index]
                edit.setText(str(value))
                edit.setStyleSheet("color: black;")  # Ensure black font
        for var_name in ['desired_temperature']:
            edit = self.cabin_edit_fields.get(var_name)
            if edit:
                value = getattr(self.train_data, var_name)[index]
                edit.setText(str(value))
                edit.setStyleSheet("color: black;")  # Ensure black font
        # Update beacon station
        station_combo = self.tc_edit_fields.get('beacon_station')
        if station_combo and self.train_data.train_count > 0:
            station_combo.setCurrentText(self.train_data.beacon_station[index])
        # Update train count field
        train_count_edit = self.tc_edit_fields.get('train_count')
        if train_count_edit:
            train_count_edit.setText(str(self.train_data.train_count))
            train_count_edit.setStyleSheet("color: black;")  # Ensure black font

    def update_train_count(self, var_name, value):
        try:
            value = int(value)
            if value < 0:
                return
            # Emit the new train count to the CTC
            self.train_data.ctc_communicate.current_train_count_signal.emit(value)
            # The TrainData instance will handle adding or removing trains
        except ValueError:
            pass  # Handle invalid input
