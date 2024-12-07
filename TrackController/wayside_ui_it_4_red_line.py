# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# Program:          Wayside User Interface      
#
# Created:          12/06/2024
# Last Update:      12/06/2024
# Last Updated by:  Zachary McPherson
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the Wayside user interface program for the Train Control System.
#        This program represents the red line wayside controller.
#        This program communicates with the Wayside Shell file


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt6.QtCore import Qt, QRect
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cell_colors = {}  # Store custom colors for individual cells

    def paintEvent(self, event):
        # Call the base class paintEvent to handle default drawing (such as grid, text, etc.)
        super().paintEvent(event)

        painter = QPainter(self.viewport())

        # Iterate over all rows
        for row in range(self.rowCount()):
            # Get the visual rectangle that spans across all columns for this row
            rect = self.visualRect(self.model().index(row, 0))  # Start with the first column
            
            # Expand the rect to span the entire row (all columns)
            row_rect = QRect(0, rect.top(), self.viewport().width(), rect.height())

            # Use alternating row colors
            if row % 2 == 0:
                # Even rows - set light blue color
                painter.fillRect(row_rect, QColor(159, 197, 248))
            else:
                # Odd rows - set white color
                painter.fillRect(row_rect, QColor(255, 255, 255))

            # Now, paint the individual cells (over the row background)
            for col in range(self.columnCount()):
                # Get the rectangle for the specific cell
                cell_rect = self.visualRect(self.model().index(row, col))

                # Check if we have a custom color for this cell
                if (row, col) in self.cell_colors:
                    cell_color, paint_full = self.cell_colors[(row, col)]
                    if paint_full:
                        # Paint the full cell with the color
                        painter.fillRect(cell_rect, cell_color)
                    else:

                        # Paint the full cell with white color
                        painter.fillRect(cell_rect, QColor('white'))

                        # Paint only the border of the cell with thicker border
                        pen = QPen(cell_color)
                        pen.setWidth(3)  # Set the thickness of the border
                        painter.setPen(pen)
                        painter.drawRect(cell_rect)  # Draw border around the cell

                # Paint the text in the cell (same as default behavior)
                item = self.item(row, col)
                if item is not None:
                    painter.setPen(Qt.GlobalColor.black)  # Set text color
                    painter.drawText(cell_rect, Qt.AlignmentFlag.AlignCenter, item.text())  # Draw text centered

        painter.end()

    def updateCellColor(self, row, col, color, paint_full=True):
        """
        Manually update the color of a specific cell.
        
        Parameters:
        - row: the row of the cell
        - col: the column of the cell
        - color: the QColor to use for the cell or border
        - paint_full: If True, fill the entire cell; if False, only paint the border
        """
        # Store the color, paint flag, and border thickness for the cell
        self.cell_colors[(row, col)] = (color, paint_full)
        
        # Trigger a repaint of the entire table
        self.update()

    def resetToAlternatingColors(self):
        """
        Reset the table to alternating row colors and clear any custom cell colors.
        """
        self.cell_colors.clear()  # Clear the custom cell colors
        self.update()  # Trigger a repaint to restore alternating colors

class wayside_ui_red_line(object):

        #########################################################################################
        #
        #                                       QT Designer
        #
        #########################################################################################

        def setupUi(self, MainWindow: QtWidgets.QMainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1118, 807)
                MainWindow.setBaseSize(QtCore.QSize(1000, 750))
                MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.tabWidget.setFont(font)
                self.tabWidget.setStyleSheet("")
                self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
                self.tabWidget.setObjectName("tabWidget")
                self.Controller = QtWidgets.QWidget()
                self.Controller.setObjectName("Controller")
                self.FilterFrame = QtWidgets.QFrame(parent=self.Controller)
                self.FilterFrame.setGeometry(QtCore.QRect(0, 220, 311, 531))
                self.FilterFrame.setStyleSheet("background-color: rgb(204, 204, 204);\n"
                "border: 3px solid black;\n"
                "")
                self.FilterFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.FilterFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
                self.FilterFrame.setObjectName("FilterFrame")
                self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.FilterFrame)
                self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 311, 531))
                self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
                self.FilterList_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
                self.FilterList_Layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
                self.FilterList_Layout.setContentsMargins(70, 0, 70, 0)
                self.FilterList_Layout.setSpacing(7)
                self.FilterList_Layout.setObjectName("FilterList_Layout")
                self.SpeedButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SpeedButton.setMinimumSize(QtCore.QSize(170, 50))
                self.SpeedButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SpeedButton.setObjectName("SpeedButton")
                self.FilterList_Layout.addWidget(self.SpeedButton)
                self.AuthorityButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.AuthorityButton.setMinimumSize(QtCore.QSize(170, 50))
                self.AuthorityButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.AuthorityButton.setObjectName("AuthorityButton")
                self.FilterList_Layout.addWidget(self.AuthorityButton)
                self.SwitchButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SwitchButton.setMinimumSize(QtCore.QSize(170, 50))
                self.SwitchButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SwitchButton.setObjectName("SwitchButton")
                self.FilterList_Layout.addWidget(self.SwitchButton)
                self.SignalButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SignalButton.setMinimumSize(QtCore.QSize(170, 50))
                self.SignalButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SignalButton.setObjectName("SignalButton")
                self.FilterList_Layout.addWidget(self.SignalButton)
                self.OccupancyButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.OccupancyButton.setMinimumSize(QtCore.QSize(170, 50))
                self.OccupancyButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.OccupancyButton.setObjectName("OccupancyButton")
                self.FilterList_Layout.addWidget(self.OccupancyButton)
                self.CrossingButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.CrossingButton.setMinimumSize(QtCore.QSize(170, 50))
                self.CrossingButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.CrossingButton.setObjectName("CrossingButton")
                self.FilterList_Layout.addWidget(self.CrossingButton)
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 160, 311, 61))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.filterHeader_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.filterHeader_layout.setContentsMargins(0, 0, 0, 0)
                self.filterHeader_layout.setObjectName("filterHeader_layout")
                self.FilterHeader = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
                self.FilterHeader.setStyleSheet("background-color: rgb(153, 153, 153);\n"
                "color: rgb(0, 0, 0);\n"
                "font: 18pt \"Times New Roman\";\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.FilterHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.FilterHeader.setObjectName("FilterHeader")
                self.filterHeader_layout.addWidget(self.FilterHeader)
                self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(310, 160, 471, 591))
                self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
                self.dataTable_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
                self.dataTable_layout.setContentsMargins(0, 0, 0, 0)
                self.dataTable_layout.setObjectName("dataTable_layout")
                self.ControllerHeader_layout = QtWidgets.QVBoxLayout()
                self.ControllerHeader_layout.setObjectName("ControllerHeader_layout")
                self.DataTable = CustomTableWidget(parent=self.verticalLayoutWidget_6)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                self.DataTable.setFont(font)
                self.DataTable.setStyleSheet('font-weight: bold; font-size: 11pt;')
                self.DataTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                self.DataTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.DataTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
                self.DataTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                self.DataTable.setAlternatingRowColors(True)
                self.DataTable.setShowGrid(False)
                self.DataTable.setRowCount(0)
                self.DataTable.setColumnCount(3)
                self.DataTable.setObjectName("DataTable")
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(2, item)
                self.DataTable.horizontalHeader().setDefaultSectionSize(152)
                self.DataTable.horizontalHeader().setMinimumSectionSize(40)
                self.DataTable.verticalHeader().setVisible(False)
                self.DataTable.verticalHeader().setDefaultSectionSize(33)
                self.ControllerHeader_layout.addWidget(self.DataTable)
                self.dataTable_layout.addLayout(self.ControllerHeader_layout)
                self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(780, 160, 311, 61))
                self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
                self.updateHeader_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
                self.updateHeader_layout.setContentsMargins(0, 0, 0, 0)
                self.updateHeader_layout.setObjectName("updateHeader_layout")
                self.UpdateHeader = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
                self.UpdateHeader.setStyleSheet("background-color: rgb(153, 153, 153);\n"
                "color: rgb(0, 0, 0);\n"
                "font: 18pt \"Times New Roman\";\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.UpdateHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.UpdateHeader.setObjectName("UpdateHeader")
                self.updateHeader_layout.addWidget(self.UpdateHeader)
                self.UpdateFrame = QtWidgets.QFrame(parent=self.Controller)
                self.UpdateFrame.setGeometry(QtCore.QRect(780, 220, 311, 531))
                self.UpdateFrame.setStyleSheet("background-color: rgb(204, 204, 204);\n"
                "border: 3px solid black;")
                self.UpdateFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.UpdateFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.UpdateFrame.setObjectName("UpdateFrame")
                self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.UpdateFrame)
                self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 311, 531))
                self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
                self.UpdateLog_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
                self.UpdateLog_layout.setContentsMargins(0, 0, 0, 0)
                self.UpdateLog_layout.setObjectName("UpdateLog_layout")
                self.UpdateLog = CustomTableWidget(parent=self.verticalLayoutWidget_5)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                self.UpdateLog.setFont(font)
                self.UpdateLog.setStyleSheet("font-weight: bold; font-size: 12pt;")
                self.UpdateLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.UpdateLog.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                self.UpdateLog.setShowGrid(True)
                self.UpdateLog.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
                self.UpdateLog.setRowCount(0)
                self.UpdateLog.setColumnCount(1)
                self.UpdateLog.setObjectName("UpdateLog")
                item = QtWidgets.QTableWidgetItem()
                self.UpdateLog.setHorizontalHeaderItem(0, item)
                self.UpdateLog.horizontalHeader().setVisible(False)
                self.UpdateLog.horizontalHeader().setDefaultSectionSize(307)
                self.UpdateLog.horizontalHeader().setHighlightSections(True)
                self.UpdateLog.verticalHeader().setVisible(False)
                self.UpdateLog.verticalHeader().setCascadingSectionResizes(False)
                self.UpdateLog.verticalHeader().setDefaultSectionSize(60)
                self.UpdateLog.verticalHeader().setHighlightSections(False)
                self.UpdateLog_layout.addWidget(self.UpdateLog)
                self.ControllerHeader = QtWidgets.QLabel(parent=self.Controller)
                self.ControllerHeader.setGeometry(QtCore.QRect(0, 1, 1091, 161))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(30)
                font.setBold(True)
                font.setItalic(False)
                font.setWeight(75)
                self.ControllerHeader.setFont(font)
                self.ControllerHeader.setStyleSheet("background-color: rgb(43, 120, 228);\n"
                "font: 30pt \"Times New Roman\";\n"
                "color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.ControllerHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ControllerHeader.setIndent(0)
                self.ControllerHeader.setObjectName("ControllerHeader")
                self.WaysideSelectComboBox = QtWidgets.QComboBox(parent=self.Controller)
                self.WaysideSelectComboBox.setGeometry(QtCore.QRect(170, 90, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.WaysideSelectComboBox.setFont(font)
                self.WaysideSelectComboBox.setStyleSheet("border: 2px solid black; font-weight: bold; font-size: 12pt;")
                self.WaysideSelectComboBox.setCurrentText("")
                self.WaysideSelectComboBox.setObjectName("WaysideSelectComboBox")
                self.WaysideSelectComboBox.addItem("")
                self.WaysideSelectComboBox.setItemText(0, "")
                self.WaysideSelectComboBox.addItem("")
                self.WaysideSelectComboBox.addItem("")
                self.WaysideSelectComboBox.addItem("")
                self.WaysideSelectComboBoxLabel = QtWidgets.QLabel(parent=self.Controller)
                self.WaysideSelectComboBoxLabel.setGeometry(QtCore.QRect(170, 50, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.WaysideSelectComboBoxLabel.setFont(font)
                self.WaysideSelectComboBoxLabel.setStyleSheet("background: rgb(43, 120, 228);\n"
                "color: rgb(255, 255, 255);")
                self.WaysideSelectComboBoxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.WaysideSelectComboBoxLabel.setObjectName("WaysideSelectComboBoxLabel")
                self.UploadPLCButton = QtWidgets.QPushButton(parent=self.Controller)
                self.UploadPLCButton.setGeometry(QtCore.QRect(950, 40, 121, 101))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.UploadPLCButton.setFont(font)
                self.UploadPLCButton.setStyleSheet("border: 2px solid black;\n"
                "border-radius: 5px;")
                self.UploadPLCButton.setObjectName("UploadPLCButton")
                self.LineSelectComboBoxLabel = QtWidgets.QLabel(parent=self.Controller)
                self.LineSelectComboBoxLabel.setGeometry(QtCore.QRect(30, 50, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.LineSelectComboBoxLabel.setFont(font)
                self.LineSelectComboBoxLabel.setStyleSheet("background: rgb(43, 120, 228);\n"
                "color: rgb(255, 255, 255);")
                self.LineSelectComboBoxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.LineSelectComboBoxLabel.setObjectName("LineSelectComboBoxLabel")
                self.ManualButton = QtWidgets.QPushButton(parent=self.Controller)
                self.ManualButton.setGeometry(QtCore.QRect(800, 40, 131, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.ManualButton.setFont(font)
                self.ManualButton.setStyleSheet("border: 2px solid black;\n"
                "border-radius: 5px;")
                self.ManualButton.setObjectName("ManualButton")
                self.AutomaticButton = QtWidgets.QPushButton(parent=self.Controller)
                self.AutomaticButton.setGeometry(QtCore.QRect(800, 100, 131, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.AutomaticButton.setFont(font)
                self.AutomaticButton.setStyleSheet("border: 2px solid black;\n"
                "border-radius: 5px;\n"
                "background-color: lime;")
                self.AutomaticButton.setObjectName("AutomaticButton")
                self.label = QtWidgets.QLabel(parent=self.Controller)
                self.label.setGeometry(QtCore.QRect(30, 90, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.label.setFont(font)
                self.label.setStyleSheet("border: 2px solid black; font-weight: bold; font-size: 12pt;")
                self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label.setObjectName("label")
                self.ControllerHeader.raise_()
                self.FilterFrame.raise_()
                self.verticalLayoutWidget_2.raise_()
                self.verticalLayoutWidget_6.raise_()
                self.verticalLayoutWidget_4.raise_()
                self.UpdateFrame.raise_()
                self.WaysideSelectComboBox.raise_()
                self.WaysideSelectComboBoxLabel.raise_()
                self.UploadPLCButton.raise_()
                self.LineSelectComboBoxLabel.raise_()
                self.ManualButton.raise_()
                self.AutomaticButton.raise_()
                self.label.raise_()
                self.tabWidget.addTab(self.Controller, "")
                self.horizontalLayout.addWidget(self.tabWidget)
                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi(MainWindow)
                self.tabWidget.setCurrentIndex(0)
                self.WaysideSelectComboBox.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow: QtWidgets.QMainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Wayside Controller"))
                self.SpeedButton.setText(_translate("MainWindow", "Speed"))
                self.AuthorityButton.setText(_translate("MainWindow", "Authority"))
                self.SwitchButton.setText(_translate("MainWindow", "Switches"))
                self.SignalButton.setText(_translate("MainWindow", "Signals"))
                self.OccupancyButton.setText(_translate("MainWindow", "Occupancy"))
                self.CrossingButton.setText(_translate("MainWindow", "Crossings"))
                self.FilterHeader.setText(_translate("MainWindow", "Filter List"))
                self.DataTable.setSortingEnabled(False)
                self.UpdateHeader.setText(_translate("MainWindow", "Updates"))
                item = self.UpdateLog.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "column"))
                self.ControllerHeader.setText(_translate("MainWindow", "Wayside Controller"))
                self.WaysideSelectComboBox.setItemText(1, _translate("MainWindow", "1"))
                self.WaysideSelectComboBox.setItemText(2, _translate("MainWindow", "2"))
                self.WaysideSelectComboBox.setItemText(3, _translate("MainWindow", "3"))
                self.WaysideSelectComboBoxLabel.setText(_translate("MainWindow", "Wayside"))
                self.UploadPLCButton.setText(_translate("MainWindow", "Upload\n"
                "PLC"))
                self.LineSelectComboBoxLabel.setText(_translate("MainWindow", "Line"))
                self.ManualButton.setText(_translate("MainWindow", "Manual"))
                self.AutomaticButton.setText(_translate("MainWindow", "Automatic"))
                self.label.setText(_translate("MainWindow", "RED"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.Controller), _translate("MainWindow", "Controller"))

        #########################################################################################
        #
        #                                 Constructor & Variables
        #
        #########################################################################################

        # Speed
        ui_sugg_speed = [None] * 78
        ui_cmd_speed = [None] * 78
        ui_past_sugg_speed = []

        # Authority
        ui_sugg_authority = [None] * 78
        ui_cmd_authority = [None] * 78
        ui_past_cmd_authority = []

        # Switches      C   F   H1   H4  H5  H8  J1
        ui_switches = [ 0,  0,   0,   0,  0,  0,  0]
        #               0,  1,   2,   3,  4,  5,  6
        ui_past_switches = []

        # Signals      A   C   D   E   F  H1  H2  H3  H4  H5  H6  H7  H8  J1  J2   N   O   Q   R   T  Yard
        ui_signals = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,    0 ]
        #              0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,   20

        # Occupancy
        ui_occupancy = [0] * 78
        
        # Wayside Occupancy
        wayside_1_occupied = 0
        wayside_2_occupied = 0
        wayside_3_occupied = 0
        wayside_1_past_occupied = 0
        wayside_2_past_occupied = 0
        wayside_3_past_occupied = 0

        # Crossings      D,  I
        ui_crossings = [ 0,  0 ]
        #               11, 47
        ui_past_crossings = []

        # Other
        selected_filter = 0 # 1 = Speed, 2 = Authority, 3 = Switches, 4 = Signals, 5 = Occupancy, 6 = Crossings
        wayside_1_operational_mode = 2 # 1 = Manual, 2 = Automatic
        wayside_2_operational_mode = 2 # 1 = Manual, 2 = Automatic
        wayside_3_operational_mode = 2 # 1 = Manual, 2 = Automatic

        """ # Contructor
        def __init__(self, MainWindow: QtWidgets.QMainWindow):

                # QT Designer
                self.setupUi(MainWindow)

                MainWindow.show()

                # Connect signals
                self.connect_filter_buttons_signals()
                self.connect_operational_mode_signals()
                self.connect_wayside_select_signals()
                self.connect_toggle_switch_signals()

                # Initial past data
                self.ui_past_sugg_speed = self.ui_sugg_speed.copy()
                self.ui_past_cmd_authority = self.ui_cmd_authority.copy()
                self.ui_past_switches = self.ui_switches.copy()
                self.ui_past_crossings = self.ui_crossings.copy() """

        #########################################################################################
        #
        #                        Manual & Auto Buttons (RED LINE COMPLETE)
        #
        #########################################################################################

        def clear_operational_mode_buttons(self):
                style_sheet_white = """border: 2px solid black;
                                   border-radius: 5px;
                                   background-color: white;"""

                self.ManualButton.setStyleSheet(style_sheet_white)
                self.AutomaticButton.setStyleSheet(style_sheet_white)

        def set_auto_manual_button_color(self):

                style_sheet_lime = """border: 2px solid black;
                                   border-radius: 5px;
                                   background-color: lime;"""

                # Reset buttons to white
                self.clear_operational_mode_buttons()

                # Wayside 1
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # In manual mode
                        if self.wayside_1_operational_mode == 1:

                                # Set background color
                                self.ManualButton.setStyleSheet(style_sheet_lime)

                        # In automatic mode
                        elif self.wayside_1_operational_mode == 2:

                                # Set background color
                                self.AutomaticButton.setStyleSheet(style_sheet_lime)

                # Wayside 2
                elif self.WaysideSelectComboBox.currentIndex() == 2:

                        # In manual mode
                        if self.wayside_2_operational_mode == 1:

                                # Set background color
                                self.ManualButton.setStyleSheet(style_sheet_lime)

                        # In automatic mode
                        elif self.wayside_2_operational_mode == 2:

                                # Set background color
                                self.AutomaticButton.setStyleSheet(style_sheet_lime)

                # Wayside 3
                elif self.WaysideSelectComboBox.currentIndex() == 3:

                        # In manual mode
                        if self.wayside_3_operational_mode == 1:

                                # Set background color
                                self.ManualButton.setStyleSheet(style_sheet_lime)

                        # In automatic mode
                        elif self.wayside_3_operational_mode == 2:

                                # Set background color
                                self.AutomaticButton.setStyleSheet(style_sheet_lime)

        def update_operational_mode(self, mode):

                # Wayside 1
                if self.WaysideSelectComboBox.currentIndex() == 1:
                        
                        # Check Wayside occupancy
                        if self.wayside_1_occupied:
                                
                                # Set to automatic mode
                                self.wayside_1_operational_mode = 2
                        else:
                                # Update wayside 1 operational mode
                                self.wayside_1_operational_mode = mode
                        
                # Wayside 2
                elif self.WaysideSelectComboBox.currentIndex() == 2:
                                
                        # Check Wayside occupancy
                        if self.wayside_2_occupied:
                                
                                # Set to automatic mode
                                self.wayside_2_operational_mode = 2
                        else:
                                # Update wayside 2 operational mode
                                self.wayside_2_operational_mode = mode
                        
                # Wayside 3
                elif self.WaysideSelectComboBox.currentIndex() == 3:
                                
                        # Check Wayside occupancy
                        if self.wayside_3_occupied:
                                
                                # Set to automatic mode
                                self.wayside_3_operational_mode = 2
                        else:
                                # Update wayside 3 operational mode
                                self.wayside_3_operational_mode = mode

                # Update button colors
                self.set_auto_manual_button_color()
                              
        def connect_operational_mode_signals(self):
                self.ManualButton.clicked.connect(lambda: self.update_operational_mode(1))
                self.AutomaticButton.clicked.connect(lambda: self.update_operational_mode(2))

        #########################################################################################
        #
        #                           Filter Buttons (RED LINE COMPLETE)
        #
        #########################################################################################

        def clear_filter_button(self):
                style_sheet_white = """font: 15pt \"Times New Roman\";
                                    border: none;
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 5px;"""
                
                self.SpeedButton.setStyleSheet(style_sheet_white)
                self.AuthorityButton.setStyleSheet(style_sheet_white)
                self.SwitchButton.setStyleSheet(style_sheet_white)
                self.SignalButton.setStyleSheet(style_sheet_white)
                self.OccupancyButton.setStyleSheet(style_sheet_white)
                self.CrossingButton.setStyleSheet(style_sheet_white)

        def update_filter_button(self, filter):
                
                style_sheet_yellow = """font: 15pt \"Times New Roman\";
                                    border: none;
                                    background-color: rgb(255, 255, 0);
                                    border-radius: 5px;"""

                # Reset all buttons to white
                self.clear_filter_button()

                # Set selected button to yellow
                if filter != self.selected_filter:
                        if filter == 1:
                                self.SpeedButton.setStyleSheet(style_sheet_yellow)
                        elif filter == 2:
                                self.AuthorityButton.setStyleSheet(style_sheet_yellow)
                        elif filter == 3:
                                self.SwitchButton.setStyleSheet(style_sheet_yellow)
                        elif filter == 4:
                                self.SignalButton.setStyleSheet(style_sheet_yellow)
                        elif filter == 5:
                                self.OccupancyButton.setStyleSheet(style_sheet_yellow)
                        elif filter == 6:
                                self.CrossingButton.setStyleSheet(style_sheet_yellow)

                # Update selected filter
                if filter == self.selected_filter:
                        self.selected_filter = 0
                else:
                        self.selected_filter = filter

        #########################################################################################
        #
        #                          Update Data Table (RED LINE COMPLETE)
        #
        #########################################################################################

        # Switch toggle cells
        # (RED LINE COMPLETE)
        def toggle_switch(self, row, col):

                # Check if switch filter is active
                if self.selected_filter == 3:

                        # Check if toggle cell has been clicked

                        # First switch
                        if row == 7 and col == 1:

                                # Wayside 1
                                if self.WaysideSelectComboBox.currentIndex() == 1 and self.wayside_1_operational_mode == 1:

                                        # Toggle switch
                                        self.ui_switches[0] = not self.ui_switches[0]
                                
                                # Wayside 2
                                elif self.WaysideSelectComboBox.currentIndex() == 2 and self.wayside_2_operational_mode == 1:

                                        # Toggle switch
                                        self.ui_switches[2] = not self.ui_switches[2]

                                # Wayside 3
                                elif self.WaysideSelectComboBox.currentIndex() == 3 and self.wayside_3_operational_mode == 1:

                                        # Toggle switch
                                        self.ui_switches[6] = not self.ui_switches[6]

                        # Second switch
                        elif row == 14 and col == 1:

                                # Wayside 1
                                if self.WaysideSelectComboBox.currentIndex() == 1 and self.wayside_1_operational_mode == 1:

                                        # Toggle switch
                                        self.ui_switches[1] = not self.ui_switches[1]
                                
                                # Wayside 2
                                elif self.WaysideSelectComboBox.currentIndex() == 2 and self.wayside_2_operational_mode == 1:

                                        # Toggle switch
                                        self.ui_switches[3] = not self.ui_switches[3]

                                # Wayside 3
                                elif self.WaysideSelectComboBox.currentIndex() == 3 and self.wayside_3_operational_mode == 1:
                                    pass
                            
                        # Third switch
                        elif row == 22 and col == 1:
                            
                            # Wayside 2
                            if self.WaysideSelectComboBox.currentIndex() == 2 and self.wayside_2_operational_mode == 1:
                                
                                # Toggle switch
                                self.ui_switches[4] = not self.ui_switches[4]

                            # Wayside 1 and 3
                            else:
                                    pass
                            
                        # Fourth switch
                        elif row == 29 and col == 1:
                                
                                # Wayside 2
                                if self.WaysideSelectComboBox.currentIndex() == 2 and self.wayside_2_operational_mode == 1:
                                        
                                        # Toggle switch
                                        self.ui_switches[5] = not self.ui_switches[5]

                                # Wayside 1 and 3
                                else:
                                        pass
                        
                        # Any other cell
                        else:
                                pass 

                        # Update table
                        self.update_data_table()
                
                # Not in switch filter
                else:
                        pass

        # Translate text to integer for Wayside 1 speed and authority
        # (RED LINE COMPLETE)
        def translate_text_to_int(self, text) -> int:

                # Check if text has a number
                num = re.findall(r'\d+', text)

                # Check if number is not empty
                if num:

                        # Return number
                        return int(num[0])

                # None
                else:
                        return None

        # Item background for speed and authority
        # (RED LINE COMPLETE)
        def set_item_background(self, row, value):
                if value == 0:
                        self.DataTable.updateCellColor(row, 0, QColor('crimson'))
                        self.DataTable.updateCellColor(row, 1, QColor('crimson'))
                        self.DataTable.updateCellColor(row, 2, QColor('crimson'))
                elif value != None:
                        self.DataTable.updateCellColor(row, 0, QColor('yellow'))
                        self.DataTable.updateCellColor(row, 1, QColor('yellow'))
                        self.DataTable.updateCellColor(row, 2, QColor('yellow'))

        # Item background for occupancy
        # (RED LINE COMPLETE)
        def set_item_background_occupancy(self, row, value):
                if value:
                        self.DataTable.updateCellColor(row, 0, QColor('yellow'))
                        self.DataTable.updateCellColor(row, 1, QColor('yellow'))

        # Copy items for insertion into table
        # (RED LINE COMPLETE)
        def copy_table_widget_item(self, source_item: QTableWidgetItem, target_item: QTableWidgetItem):
                target_item.setText(source_item.text())
                target_item.setIcon(source_item.icon())
                target_item.setStatusTip(source_item.statusTip())
                target_item.setToolTip(source_item.toolTip())
                target_item.setWhatsThis(source_item.whatsThis())
                target_item.setFont(source_item.font())
                target_item.setBackground(source_item.background())
                target_item.setForeground(source_item.foreground())
                target_item.setFlags(source_item.flags())

        # Reset data table
        # (RED LINE COMPLETE)
        def data_table_reset(self):
                self.DataTable.resetToAlternatingColors()
                self.DataTable.clear()

        # Set colors of the signals in the table
        # (RED LINE COMPLETE)
        def set_table_signal_status(self, status, row, col):

                # Set item attributes
                bright_green_color = QColor(0, 255, 0)
                bright_red_color = QColor(255, 0, 0)
                dark_green_color = QColor(0, 75, 0)
                dark_red_color = QColor(75, 0, 0)

                # Set signal status
                if status:
                        for i in range(3):

                                # Set colors
                                self.DataTable.updateCellColor(row + i, col, bright_red_color)
                                self.DataTable.updateCellColor(row + 5 + i, col, dark_green_color)

                else:
                        for i in range(3):

                                # Set colors
                                self.DataTable.updateCellColor(row + i, col, dark_red_color)
                                self.DataTable.updateCellColor(row + 5 + i, col, bright_green_color)

        # Update speed data in table
        # (RED LINE COMPLETE)               
        def data_table_speed(self):

                # Reset table
                self.data_table_reset()

                # Set columns
                self.DataTable.setColumnCount(3)
                self.DataTable.horizontalHeader().setDefaultSectionSize(152)
                self.DataTable.setHorizontalHeaderLabels(["Block", "Sugg. Speed", "Cmd. Speed"])

                # Wayside 1 Data
                # (RED LINE COMPLETE)
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # Set row count
                        self.DataTable.setRowCount(24)
                        
                        # Set data
                        for i in range(24):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i if i != 0 else 'Yard'}")
                                temp_sugg_item.setText(f'{f'{round(self.ui_sugg_speed[i] / 1.609)} mph' if self.ui_sugg_speed[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{round(self.ui_cmd_speed[i] / 1.609)} mph' if self.ui_cmd_speed[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i, self.ui_cmd_speed[i])

                                # Set items
                                self.DataTable.setItem(i, 0, temp_block_item)
                                self.DataTable.setItem(i, 1, temp_sugg_item)
                                self.DataTable.setItem(i, 2, temp_cmd_item)

                # Wayside 2 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 2:
                        
                        # Set row count
                        self.DataTable.setRowCount(32)

                        # Sections H1 --> H8
                        for i in range(24, 46):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{round(self.ui_sugg_speed[i] / 1.609)} mph' if self.ui_sugg_speed[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{round(self.ui_cmd_speed[i] / 1.609)} mph' if self.ui_cmd_speed[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-24, self.ui_cmd_speed[i])

                                # Set items
                                self.DataTable.setItem(i-24, 0, temp_block_item)
                                self.DataTable.setItem(i-24, 1, temp_sugg_item)
                                self.DataTable.setItem(i-24, 2, temp_cmd_item)

                        # Sections O --> T
                        for i in range(68, 78):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{round(self.ui_sugg_speed[i] / 1.609)} mph' if self.ui_sugg_speed[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{round(self.ui_cmd_speed[i] / 1.609)} mph' if self.ui_cmd_speed[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-46, self.ui_cmd_speed[i])

                                self.DataTable.setItem(i-46, 0, temp_block_item)
                                self.DataTable.setItem(i-46, 1, temp_sugg_item)
                                self.DataTable.setItem(i-46, 2, temp_cmd_item)
              
                # Wayside 3 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 3:
                        
                        # Set row count
                        self.DataTable.setRowCount(22)

                        # Fill Table with block speed data
                        for i in range(46, 68):
                                
                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{round(self.ui_sugg_speed[i] / 1.609)} mph' if self.ui_sugg_speed[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{round(self.ui_cmd_speed[i] / 1.609)} mph' if self.ui_cmd_speed[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-46, self.ui_cmd_speed[i])

                                self.DataTable.setItem(i-46, 0, temp_block_item)
                                self.DataTable.setItem(i-46, 1, temp_sugg_item)
                                self.DataTable.setItem(i-46, 2, temp_cmd_item)

        # Update authority data in table
        # (RED LINE COMPLETE)
        def data_table_authority(self):
                
                # Reset table
                self.data_table_reset()

                # Set columns
                self.DataTable.setColumnCount(3)
                self.DataTable.horizontalHeader().setDefaultSectionSize(152)
                self.DataTable.setHorizontalHeaderLabels(["Block", "Sugg. Authority", "Cmd. Authority"])

                # Wayside 1 Data
                # (RED LINE COMPLETE)
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # Set row count
                        self.DataTable.setRowCount(24)
                        
                        # Set data
                        for i in range(24):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i if i != 0 else 'Yard'}")
                                temp_sugg_item.setText(f'{f'{self.ui_sugg_authority[i]} blocks' if self.ui_sugg_authority[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{self.ui_cmd_authority[i]} blocks' if self.ui_cmd_authority[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i, self.ui_cmd_authority[i])

                                # Set items
                                self.DataTable.setItem(i, 0, temp_block_item)
                                self.DataTable.setItem(i, 1, temp_sugg_item)
                                self.DataTable.setItem(i, 2, temp_cmd_item)

                # Wayside 2 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 2:

                        # Set row count
                        self.DataTable.setRowCount(32)

                        # Sections H1 --> H8
                        # (RED LINE COMPLETE)
                        for i in range(24, 46):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{self.ui_sugg_authority[i]} blocks' if self.ui_sugg_authority[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{self.ui_cmd_authority[i]} blocks' if self.ui_cmd_authority[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-24, self.ui_cmd_authority[i])

                                # Set items
                                self.DataTable.setItem(i-24, 0, temp_block_item)
                                self.DataTable.setItem(i-24, 1, temp_sugg_item)
                                self.DataTable.setItem(i-24, 2, temp_cmd_item)

                        # Sections O --> T
                        # (RED LINE COMPLETE)
                        for i in range(68, 78):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{self.ui_sugg_authority[i]} blocks' if self.ui_sugg_authority[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{self.ui_cmd_authority[i]} blocks' if self.ui_cmd_authority[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-46, self.ui_cmd_authority[i])

                                self.DataTable.setItem(i-46, 0, temp_block_item)
                                self.DataTable.setItem(i-46, 1, temp_sugg_item)
                                self.DataTable.setItem(i-46, 2, temp_cmd_item)
              
                # Wayside 3 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 3:

                        # Set row count
                        self.DataTable.setRowCount(22)

                        # Fill Table with block speed data
                        for i in range(46, 68):

                                # Temp table items
                                temp_block_item = QtWidgets.QTableWidgetItem()
                                temp_sugg_item = QtWidgets.QTableWidgetItem()
                                temp_cmd_item = QtWidgets.QTableWidgetItem()

                                # Set item information
                                temp_block_item.setText(f"{i}")
                                temp_sugg_item.setText(f'{f'{self.ui_sugg_authority[i]} blocks' if self.ui_sugg_authority[i] != None else "None"}')
                                temp_cmd_item.setText(f'{f'{self.ui_cmd_authority[i]} blocks' if self.ui_cmd_authority[i] != None else "None"}')

                                # Set background
                                self.set_item_background(i-46, self.ui_cmd_authority[i])

                                self.DataTable.setItem(i-46, 0, temp_block_item)
                                self.DataTable.setItem(i-46, 1, temp_sugg_item)
                                self.DataTable.setItem(i-46, 2, temp_cmd_item)

        # Update switch data in table
        # (RED LINE COMPLETE)
        def data_table_switches(self):

                # Reset table
                self.data_table_reset()

                # Set column count
                self.DataTable.setColumnCount(5)

                # Table items
                temp_text_item = QtWidgets.QTableWidgetItem()
                temp_toggle_item = QtWidgets.QTableWidgetItem()

                # Table colors
                solid_color = QColor(100, 149, 237, 255)

                # Set item attributes

                        # Text
                temp_text_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                temp_toggle_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                temp_toggle_item.setText('Toggle')

                        # Disable checkable flag
                temp_text_item.setFlags(temp_text_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_toggle_item.setFlags(temp_toggle_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

                # Set columns
                self.DataTable.setColumnCount(5)
                self.DataTable.horizontalHeader().setDefaultSectionSize(92)
                self.DataTable.setHorizontalHeaderLabels(["", "", "", "", "", ""])

                # Wayside 1
                # (RED LINE COMPLETE)
                if self.WaysideSelectComboBox.currentIndex() == 1:
                        
                    # Set row count
                    self.DataTable.setRowCount(16)

                    # Set cells to white
                    for i in range(16):
                            for j in range(5):
                                    self.DataTable.updateCellColor(i, j, QColor('white'))

                    # Switch C text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("C")
                    self.DataTable.setItem(4, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("D")
                    self.DataTable.setItem(2, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("Yard")
                    self.DataTable.setItem(6, 4, item)

                    # Switch F text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("F")
                    self.DataTable.setItem(11, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("E")
                    self.DataTable.setItem(9, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("A")
                    self.DataTable.setItem(13, 4, item)

                    # Determine switch position

                    # C <--> D
                    if self.ui_switches[0]:

                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color)
                            self.DataTable.updateCellColor(2, 3, solid_color)
                            self.DataTable.updateCellColor(5, 2, solid_color, False)
                            self.DataTable.updateCellColor(6, 3, solid_color, False)

                    # C <--> Yard
                    else:

                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color, False)
                            self.DataTable.updateCellColor(2, 3, solid_color, False)
                            self.DataTable.updateCellColor(5, 2, solid_color)
                            self.DataTable.updateCellColor(6, 3, solid_color)

                    # F <--> E
                    if self.ui_switches[1]:

                            self.DataTable.updateCellColor(11, 1, solid_color)
                            self.DataTable.updateCellColor(10, 2, solid_color)
                            self.DataTable.updateCellColor(9, 3, solid_color)
                            self.DataTable.updateCellColor(12, 2, solid_color, False)
                            self.DataTable.updateCellColor(13, 3, solid_color, False)
                    
                    # F <--> A
                    else:

                            self.DataTable.updateCellColor(11, 1, solid_color)
                            self.DataTable.updateCellColor(10, 2, solid_color, False)
                            self.DataTable.updateCellColor(9, 3, solid_color, False)
                            self.DataTable.updateCellColor(12, 2, solid_color)
                            self.DataTable.updateCellColor(13, 3, solid_color)

                    # Insert toggle items
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(7, 1, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(14, 1, temp_toggle_item)

                    # Set toggle item backgrounds
                    self.DataTable.updateCellColor(7, 1, QColor('yellow'))
                    self.DataTable.updateCellColor(14, 1, QColor('yellow'))

                # Wayside 2
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 2:
                        
                    # Set row count
                    self.DataTable.setRowCount(32)

                    # Set cells to white
                    for i in range(32):
                            for j in range(5):
                                    self.DataTable.updateCellColor(i, j, QColor('white'))

                    # Switch H1 text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H1")
                    self.DataTable.setItem(4, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("T")
                    self.DataTable.setItem(2, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H2")
                    self.DataTable.setItem(6, 4, item)

                    # Switch H4 text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H4")
                    self.DataTable.setItem(11, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H3")
                    self.DataTable.setItem(9, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("R")
                    self.DataTable.setItem(13, 4, item)

                    # Switch H5 text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H5")
                    self.DataTable.setItem(19, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("Q")
                    self.DataTable.setItem(17, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H6")
                    self.DataTable.setItem(21, 4, item)

                    # Switch H8 text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H8")
                    self.DataTable.setItem(26, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("H7")
                    self.DataTable.setItem(24, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("O")
                    self.DataTable.setItem(28, 4, item)

                    # Determine switch position

                    # H1 <--> T
                    if self.ui_switches[2]:

                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color)
                            self.DataTable.updateCellColor(2, 3, solid_color)
                            self.DataTable.updateCellColor(5, 2, solid_color, False)
                            self.DataTable.updateCellColor(6, 3, solid_color, False)

                    # H1 <--> H2
                    else:

                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color, False)
                            self.DataTable.updateCellColor(2, 3, solid_color, False)
                            self.DataTable.updateCellColor(5, 2, solid_color)
                            self.DataTable.updateCellColor(6, 3, solid_color)

                    # H4 <--> H3
                    if self.ui_switches[3]:

                            self.DataTable.updateCellColor(11, 1, solid_color)
                            self.DataTable.updateCellColor(10, 2, solid_color)
                            self.DataTable.updateCellColor(9, 3, solid_color)
                            self.DataTable.updateCellColor(12, 2, solid_color, False)
                            self.DataTable.updateCellColor(13, 3, solid_color, False)
                    
                    # H4 <--> R
                    else:

                            self.DataTable.updateCellColor(11, 1, solid_color)
                            self.DataTable.updateCellColor(10, 2, solid_color, False)
                            self.DataTable.updateCellColor(9, 3, solid_color, False)
                            self.DataTable.updateCellColor(12, 2, solid_color)
                            self.DataTable.updateCellColor(13, 3, solid_color)

                    # H5 <--> Q
                    if self.ui_switches[4]:

                            self.DataTable.updateCellColor(19, 1, solid_color)
                            self.DataTable.updateCellColor(18, 2, solid_color)
                            self.DataTable.updateCellColor(17, 3, solid_color)
                            self.DataTable.updateCellColor(20, 2, solid_color, False)
                            self.DataTable.updateCellColor(21, 3, solid_color, False)
                    
                    # H5 <--> H6
                    else:

                            self.DataTable.updateCellColor(19, 1, solid_color)
                            self.DataTable.updateCellColor(18, 2, solid_color, False)
                            self.DataTable.updateCellColor(17, 3, solid_color, False)
                            self.DataTable.updateCellColor(20, 2, solid_color)
                            self.DataTable.updateCellColor(21, 3, solid_color)

                    # H8 <--> H7
                    if self.ui_switches[5]:

                            self.DataTable.updateCellColor(26, 1, solid_color)
                            self.DataTable.updateCellColor(25, 2, solid_color)
                            self.DataTable.updateCellColor(24, 3, solid_color)
                            self.DataTable.updateCellColor(27, 2, solid_color, False)
                            self.DataTable.updateCellColor(28, 3, solid_color, False)
                    
                    # H8 <--> O
                    else:

                            self.DataTable.updateCellColor(26, 1, solid_color)
                            self.DataTable.updateCellColor(25, 2, solid_color, False)
                            self.DataTable.updateCellColor(24, 3, solid_color, False)
                            self.DataTable.updateCellColor(27, 2, solid_color)
                            self.DataTable.updateCellColor(28, 3, solid_color)

                    # Insert toggle items
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(7, 1, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(14, 1, temp_toggle_item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(22, 1, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(29, 1, item)

                    # Set toggle item backgrounds
                    self.DataTable.updateCellColor(7, 1, QColor('yellow'))
                    self.DataTable.updateCellColor(14, 1, QColor('yellow'))
                    self.DataTable.updateCellColor(22, 1, QColor('yellow'))
                    self.DataTable.updateCellColor(29, 1, QColor('yellow'))

                # Wayside 3
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 3:
                        
                    # Set row count
                    self.DataTable.setRowCount(16)

                    # Set cells to white
                    for i in range(16):
                            for j in range(5):
                                    self.DataTable.updateCellColor(i, j, QColor('white'))

                    # Switch J1 text
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("J1")
                    self.DataTable.setItem(4, 0, item)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("N")
                    self.DataTable.setItem(2, 4, item)

                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_text_item, item)
                    item.setText("J2")
                    self.DataTable.setItem(6, 4, item)

                    # Determine switch position

                    # J1 <--> N
                    if self.ui_switches[6]:

                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color)
                            self.DataTable.updateCellColor(2, 3, solid_color)
                            self.DataTable.updateCellColor(5, 2, solid_color, False)
                            self.DataTable.updateCellColor(6, 3, solid_color, False)

                    # J1 <--> J2
                    else:
                            
                            self.DataTable.updateCellColor(4, 1, solid_color)
                            self.DataTable.updateCellColor(3, 2, solid_color, False)
                            self.DataTable.updateCellColor(2, 3, solid_color, False)
                            self.DataTable.updateCellColor(5, 2, solid_color)
                            self.DataTable.updateCellColor(6, 3, solid_color)

                    # Insert toggle item
                    item = QtWidgets.QTableWidgetItem()
                    self.copy_table_widget_item(temp_toggle_item, item)
                    self.DataTable.setItem(7, 1, item)

                    # Set toggle item background
                    self.DataTable.updateCellColor(7, 1, QColor('yellow'))

        # Update signal data in table
        # (RED LINE COMPLETE)
        def data_table_signals(self):
                
                # Reset table
                self.data_table_reset()

                # Set table style
                self.DataTable.setStyleSheet("")

                # Temp table items
                temp_text_letter_item = QtWidgets.QTableWidgetItem()
                temp_text_sec_item = QtWidgets.QTableWidgetItem()
                temp_solid_black_item = QtWidgets.QTableWidgetItem()
                temp_white_item = QtWidgets.QTableWidgetItem()

                # Set item attributes

                        # Text
                temp_text_letter_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                temp_text_sec_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                temp_text_sec_item.setText('Section:')

                        # Disable checkable flag
                temp_text_letter_item.setFlags(temp_text_letter_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_text_sec_item.setFlags(temp_text_sec_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_solid_black_item.setFlags(temp_solid_black_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_white_item.setFlags(temp_white_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

                # Wayside 1
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # Set columns
                        self.DataTable.setColumnCount(9)
                        self.DataTable.horizontalHeader().setDefaultSectionSize(51)
                        self.DataTable.setHorizontalHeaderLabels(["", "", "", "", "", "", "", "", ""])

                        # Set row count
                        self.DataTable.setRowCount(48)

                        # Set cells to white
                        for i in range(48):
                                for j in range(9):
                                        self.DataTable.updateCellColor(i, j, QColor('white'))

                        # Set section text
                        for i, j in zip([2, 2, 17, 17, 33, 33], [1, 5, 1, 5, 1, 5]):

                                # Copy text item
                                item = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_sec_item, item)

                                # Set item
                                self.DataTable.setItem(i, j, item)

                        # Set section letters
                        for i, j, text, in zip([2, 2, 17, 17, 33, 33], [2, 6, 2, 6, 2, 6], ['C', 'D', 'Yard', 'F', 'A', 'E']):
                            item = QtWidgets.QTableWidgetItem()
                            self.copy_table_widget_item(temp_text_letter_item, item)
                            item.setText(text)
                            self.DataTable.setItem(i, j, item)

                        # Set light outlines
                        for col, row in zip([1, 5, 1, 5, 1, 5], [4, 4, 19, 19, 35, 35]):
                                for i in range(row, row + 10):
                                        for j in range(col, col + 3):
                                                self.DataTable.updateCellColor(i, j, QColor('black'))

                        # Set signal colors
                        self.set_table_signal_status(self.ui_signals[1], 5, 2)
                        self.set_table_signal_status(self.ui_signals[2], 5, 6)
                        self.set_table_signal_status(self.ui_signals[20], 20, 2)
                        self.set_table_signal_status(self.ui_signals[4], 20, 6)
                        self.set_table_signal_status(self.ui_signals[0], 36, 2)
                        self.set_table_signal_status(self.ui_signals[3], 36, 6)

                # Wayside 2
                elif self.WaysideSelectComboBox.currentIndex() == 2:

                        # Set columns
                        self.DataTable.setColumnCount(9)
                        self.DataTable.horizontalHeader().setDefaultSectionSize(51)
                        self.DataTable.setHorizontalHeaderLabels(['', '', '', '', '', '', '', '', ''])

                        # Set row count
                        self.DataTable.setRowCount(96)

                        # Set cells to white
                        for i in range(96):
                                for j in range(9):
                                        self.DataTable.updateCellColor(i, j, QColor('white'))

                        # Set section text
                        for i, j, in zip([2, 2, 17, 17, 33, 33, 49, 49, 65, 65, 81, 81], [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5]):
                            item = QtWidgets.QTableWidgetItem()
                            self.copy_table_widget_item(temp_text_sec_item, item)
                            self.DataTable.setItem(i, j, item)

                        # Set section letters
                        for i, j, text, in zip([2, 2, 17, 17, 33, 33, 49, 49, 65, 65, 81, 81], [2, 6, 2, 6, 2, 6, 2, 6, 2, 6, 2, 6], ['H1', 'H2', 'T', 'H4', 'H3', 'R', 'H5', 'H6', 'Q', 'H8', 'H7', 'O']):
                            item = QtWidgets.QTableWidgetItem()
                            self.copy_table_widget_item(temp_text_letter_item, item)
                            item.setText(text)
                            self.DataTable.setItem(i, j, item)

                        # Set light outlines
                        for col, row in zip([1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5], [4, 4, 19, 19, 35, 35, 51, 51, 67, 67, 83, 83]):
                                for i in range(row, row + 10):
                                        for j in range(col, col + 3):
                                                self.DataTable.updateCellColor(i, j, QColor('black'))

                        # Set signal colors
                        self.set_table_signal_status(self.ui_signals[5], 5, 2) # H1
                        self.set_table_signal_status(self.ui_signals[6], 5, 6) # H2
                        self.set_table_signal_status(self.ui_signals[19], 20, 2) # T
                        self.set_table_signal_status(self.ui_signals[8], 20, 6) # H4
                        self.set_table_signal_status(self.ui_signals[7], 36, 2) # H3
                        self.set_table_signal_status(self.ui_signals[18], 36, 6) # R
                        self.set_table_signal_status(self.ui_signals[9], 52, 2) # H5
                        self.set_table_signal_status(self.ui_signals[10], 52, 6) # H6
                        self.set_table_signal_status(self.ui_signals[17], 68, 2) # Q
                        self.set_table_signal_status(self.ui_signals[12], 68, 6) # H8
                        self.set_table_signal_status(self.ui_signals[11], 84, 2) # H7
                        self.set_table_signal_status(self.ui_signals[16], 84, 6) # O

                # Wayside 3
                elif self.WaysideSelectComboBox.currentIndex() == 3:

                        # Set columns
                        self.DataTable.setColumnCount(9)
                        self.DataTable.horizontalHeader().setDefaultSectionSize(51)
                        self.DataTable.setHorizontalHeaderLabels(["", "", "", "", "", "", "", "", ""])

                        # Set row count
                        self.DataTable.setRowCount(32)

                        # Set cells to white
                        for i in range(32):
                                for j in range(9):
                                        self.DataTable.updateCellColor(i, j, QColor('white'))

                        # Set section text
                        for i, j in zip([2, 2, 17], [1, 5, 1]):

                                # Copy text item
                                item = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_sec_item, item)

                                # Set item
                                self.DataTable.setItem(i, j, item)

                        # Set section letters
                        for i, j, text, in zip([2, 2, 17], [2, 6, 2], ['J1', 'J2', 'N']):
                            item = QtWidgets.QTableWidgetItem()
                            self.copy_table_widget_item(temp_text_letter_item, item)
                            item.setText(text)
                            self.DataTable.setItem(i, j, item)

                        # Set light outlines
                        for col, row in zip([1, 5, 1], [4, 4, 19]):
                                for i in range(row, row + 10):
                                        for j in range(col, col + 3):
                                                self.DataTable.updateCellColor(i, j, QColor('black'))

                        # Set signal colors
                        self.set_table_signal_status(self.ui_signals[13], 5, 2) # J1
                        self.set_table_signal_status(self.ui_signals[14], 5, 6) # J2
                        self.set_table_signal_status(self.ui_signals[15], 20, 2) # N

        # Update occupancy data in table
        # (RED LINE COMPLETE)
        def data_table_occupancy(self):
                
                # Reset table
                self.data_table_reset()

                # Temp table items
                temp_block_item = QtWidgets.QTableWidgetItem()
                temp_occupancy_item = QtWidgets.QTableWidgetItem()

                # Set item attributes

                        # Text
                temp_block_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                temp_occupancy_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                        # Disable checkable flag
                temp_block_item.setFlags(temp_block_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_occupancy_item.setFlags(temp_occupancy_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

                # Set columns
                self.DataTable.setColumnCount(2)
                self.DataTable.horizontalHeader().setDefaultSectionSize(228)
                self.DataTable.setHorizontalHeaderLabels(["Block", "Occupancy"])

                # Wayside 1 Data
                # (RED LINE COMPLETE)
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # Set row count
                        self.DataTable.setRowCount(24)
                        
                        # Set data
                        for i in range(24):

                                # Copy items
                                block_item = QtWidgets.QTableWidgetItem()
                                occupancy_item = QtWidgets.QTableWidgetItem()

                                self.copy_table_widget_item(temp_block_item, block_item)
                                self.copy_table_widget_item(temp_occupancy_item, occupancy_item)

                                # Set item information
                                block_item.setText(f"{i if i != 0 else 'Yard'}")
                                occupancy_item.setText(f'{'Occupied' if self.ui_occupancy[i] else "Vacant"}')

                                # Set background
                                self.set_item_background_occupancy(i, self.ui_occupancy[i])

                                # Set items
                                self.DataTable.setItem(i, 0, block_item)
                                self.DataTable.setItem(i, 1, occupancy_item)

                # Wayside 2 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 2:

                        # Set row count
                        self.DataTable.setRowCount(32)

                        # Sections H1 --> H8
                        for i in range(24, 46):

                                # Copy items
                                block_item = QtWidgets.QTableWidgetItem()
                                occupancy_item = QtWidgets.QTableWidgetItem()

                                self.copy_table_widget_item(temp_block_item, block_item)
                                self.copy_table_widget_item(temp_occupancy_item, occupancy_item)

                                # Set item information
                                block_item.setText(f"{i}")
                                occupancy_item.setText(f'{'Occupied' if self.ui_occupancy[i] else "Vacant"}')

                                # Set background
                                self.set_item_background_occupancy(i-24, self.ui_occupancy[i])

                                # Set items
                                self.DataTable.setItem(i-24, 0, block_item)
                                self.DataTable.setItem(i-24, 1, occupancy_item)

                        # Sections O --> T
                        for i in range(68, 78):

                                # Copy items
                                block_item = QtWidgets.QTableWidgetItem()
                                occupancy_item = QtWidgets.QTableWidgetItem()

                                self.copy_table_widget_item(temp_block_item, block_item)
                                self.copy_table_widget_item(temp_occupancy_item, occupancy_item)

                                # Set item information
                                block_item.setText(f"{i}")
                                occupancy_item.setText(f'{'Occupied' if self.ui_occupancy[i] else "Vacant"}')

                                # Set background
                                self.set_item_background_occupancy(i-46, self.ui_occupancy[i])

                                # Set items
                                self.DataTable.setItem(i-46, 0, block_item)
                                self.DataTable.setItem(i-46, 1, occupancy_item)
                
                # Wayside 3 Data
                # (RED LINE COMPLETE)
                elif self.WaysideSelectComboBox.currentIndex() == 3:

                        # Set row count
                        self.DataTable.setRowCount(22)

                        # Fill Table with block speed data
                        for i in range(46, 68):

                                # Copy items
                                block_item = QtWidgets.QTableWidgetItem()
                                occupancy_item = QtWidgets.QTableWidgetItem()

                                self.copy_table_widget_item(temp_block_item, block_item)
                                self.copy_table_widget_item(temp_occupancy_item, occupancy_item)

                                # Set item information
                                block_item.setText(f"{i}")
                                occupancy_item.setText(f'{'Occupied' if self.ui_occupancy[i] else "Vacant"}')

                                # Set background
                                self.set_item_background_occupancy(i-46, self.ui_occupancy[i])

                                # Set items
                                self.DataTable.setItem(i-46, 0, block_item)
                                self.DataTable.setItem(i-46, 1, occupancy_item)

        # Update crossing data in table
        # (RED LINE COMPLETE)
        def data_table_crossings(self):
                
                # Reset table
                self.data_table_reset()

                # Temp table items
                temp_text_value_item = QtWidgets.QTableWidgetItem()
                temp_text_label_item = QtWidgets.QTableWidgetItem()

                # Set item attributes

                        # Text
                temp_text_value_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                temp_text_label_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

                        # Disable checkable flag
                temp_text_value_item.setFlags(temp_text_value_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
                temp_text_label_item.setFlags(temp_text_label_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

                # Set columns
                self.DataTable.setColumnCount(9)
                self.DataTable.horizontalHeader().setDefaultSectionSize(51)
                self.DataTable.setHorizontalHeaderLabels(["", "", "", "", "", "", "", "", ""])

                # Set rows
                self.DataTable.setRowCount(16)

                # Set cells to white
                for i in range(16):
                        for j in range(9):
                                self.DataTable.updateCellColor(i, j, QColor('white'))

                # Set crossing frame
                if self.WaysideSelectComboBox.currentIndex() == 1 or self.WaysideSelectComboBox.currentIndex() == 3:

                        # Set section & block text
                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_label_item, item)
                        item.setText('Section:')
                        self.DataTable.setItem(2, 6, item)

                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_label_item, item)
                        item.setText('Block:')
                        self.DataTable.setItem(3, 6, item)

                        # Set black outlines
                        for i in range(9, 14):

                                self.DataTable.updateCellColor(i, 7, QColor('black'))
                        
                        for i in range(11, 14):

                                self.DataTable.updateCellColor(i, 1, QColor('black'))

                # Wayside 1 data
                if self.WaysideSelectComboBox.currentIndex() == 1:

                        # Set section text
                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_value_item, item)
                        item.setText('D')
                        self.DataTable.setItem(2, 7, item)

                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_value_item, item)
                        item.setText('11')
                        self.DataTable.setItem(3, 7, item)

                        # Closed
                        if self.ui_crossings[0]:

                                # Insert red items
                                for i in [7, 6, 5, 4, 3, 2, 1]:

                                       self.DataTable.updateCellColor(10, i, QColor('crimson'))

                        # Open
                        else:
                                # Insert red items
                                for i, j, in zip([10, 9, 8, 7, 6, 5, 4], [7, 6, 5, 4, 3, 2, 1]):
                                        
                                        self.DataTable.updateCellColor(i, j, QColor('crimson'))

                # Wayside 3 data
                elif self.WaysideSelectComboBox.currentIndex() == 3:

                        # Set section text
                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_value_item, item)
                        item.setText('I')
                        self.DataTable.setItem(2, 7, item)

                        item = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_value_item, item)
                        item.setText('47')
                        self.DataTable.setItem(3, 7, item)

                        # Closed
                        if self.ui_crossings[1]:

                                # Insert red items
                                for i in [7, 6, 5, 4, 3, 2, 1]:

                                        # Set item
                                        self.DataTable.updateCellColor(10, i, QColor('crimson'))

                        # Open
                        else:
                                # Insert red items
                                for i, j, in zip([10, 9, 8, 7, 6, 5, 4], [7, 6, 5, 4, 3, 2, 1]):

                                        self.DataTable.updateCellColor(i, j, QColor('crimson'))

                # Wayside 2 data (no crossings)
                elif self.WaysideSelectComboBox.currentIndex() == 2:
                        pass

        # Call all data table update functions
        # (RED LINE COMPLETE)
        def update_data_table(self):
                if self.selected_filter == 1:
                        self.data_table_speed()
                elif self.selected_filter == 2:
                        self.data_table_authority()
                elif self.selected_filter == 3:
                        self.data_table_switches()
                elif self.selected_filter == 4:
                        self.data_table_signals()
                elif self.selected_filter == 5:
                        self.data_table_occupancy()
                elif self.selected_filter == 6:
                        self.data_table_crossings()
                else:
                        self.data_table_reset()

        #########################################################################################
        #
        #                         Handle Table Filters (RED LINE COMPLETE)
        #
        #########################################################################################

        def table_speed_handler(self):

                # Set filter
                self.update_filter_button(1)

                # Update table based on filter
                self.update_data_table()

        def table_authority_handler(self):

                # Set filter
                self.update_filter_button(2)

                # Update table based on filter
                self.update_data_table()

        def table_switches_handler(self):

                # Set filter
                self.update_filter_button(3)

                # Update table based on filter
                self.update_data_table()

        def table_signals_handler(self):

                # Set filter
                self.update_filter_button(4)

                # Update table based on filter
                self.update_data_table()

        def table_occupancy_handler(self):

                # Set filter
                self.update_filter_button(5)

                # Update table based on filter
                self.update_data_table()

        def table_crossings_handler(self):

                # Set filter
                self.update_filter_button(6)

                # Update table based on filter
                self.update_data_table()

        def connect_filter_buttons_signals(self):

                # Connect filter buttons
                self.SpeedButton.clicked.connect(self.table_speed_handler)
                self.AuthorityButton.clicked.connect(self.table_authority_handler)
                self.SwitchButton.clicked.connect(self.table_switches_handler)
                self.SignalButton.clicked.connect(self.table_signals_handler)
                self.OccupancyButton.clicked.connect(self.table_occupancy_handler)
                self.CrossingButton.clicked.connect(self.table_crossings_handler)

        def connect_wayside_select_signals(self):

                # Connect wayside select
                self.WaysideSelectComboBox.currentIndexChanged.connect(self.set_auto_manual_button_color)
                self.WaysideSelectComboBox.currentIndexChanged.connect(self.update_data_table)

        def connect_toggle_switch_signals(self):

                # Connect toggle switch signals
                self.DataTable.cellClicked.connect(self.toggle_switch)

        #########################################################################################
        #
        #                           Update Log Table (RED LINE COMPLETE)
        #
        #########################################################################################

        # Add log item to table
        # (RED LINE COMPLETE)
        def add_log_item(self, item: QTableWidgetItem):
                
                # Insert row
                self.UpdateLog.insertRow(0)

                # Set background
                for i in range(self.UpdateLog.rowCount()):
                        self.UpdateLog.updateCellColor(i, 0, QColor('#ffe6a7'))

                # Set item
                self.UpdateLog.setItem(0, 0, item)

        # Determine block text
        # (RED LINE COMPLETE)
        def set_block_text(self, index: int) -> str:

                # Set block text
                if index == 0:
                        text = 'Yard'
                else:
                        text = str(index)

                # Return text
                return text
        
        # Determine joint text
        # (RED LINE COMPLETE)
        def set_joint_text(self, index: int) -> str:

                # Set joint text
                if index == 0:
                        text = 'C'
                elif index == 1:
                        text = 'F'
                elif index == 2:
                        text = 'H1'
                elif index == 3:
                        text = 'H4'
                elif index == 4:
                        text = 'H5'
                elif index == 5:
                        text = 'H8'
                elif index == 6:
                        text = 'J1'

                # Return text
                return text

        # Determine gate text
        # (RED LINE COMPLETE)
        def set_gate_text(self, index: int) -> str:

                # Set gate text
                if index == 0:
                        text = 'D'
                elif index == 1:
                        text = 'I'

                # Return text
                return text

        # Determine leg text
        # (RED LINE COMPLETE)
        def set_leg_text(self, index: int, value: int) -> str:

                # Switch D
                if index == 0:

                        # Set leg text
                        if value:
                                text = 'D'
                        else:
                                text = 'Yard'
                
                # Switch F
                elif index == 1:

                        # Set leg text
                        if value:
                                text = 'E'
                        else:
                                text = 'A'

                # Switch H1
                elif index == 2:

                        # Set leg text
                        if value:
                                text = 'T'
                        else:
                                text = 'H2'

                # Switch H4
                elif index == 3:

                        # Set leg text
                        if value:
                                text = 'H3'
                        else:
                                text = 'R'

                # Switch H5
                elif index == 4:

                        # Set leg text
                        if value:
                                text = 'Q'
                        else:
                                text = 'H6'

                # Switch H8
                elif index == 5:

                        # Set leg text
                        if value:
                                text = 'H7'
                        else:
                                text = 'O'
                                
                # Switch J1
                elif index == 6:

                        # Set leg text
                        if value:
                                text = 'N'
                        else:
                                text = 'J2'

                # Other
                else:
                        text = 'None'

                # Return text
                return text

        # Update log table
        # (RED LINE COMPLETE)
        def update_log_table(self):
                
                # Table items
                temp_text_item = QtWidgets.QTableWidgetItem()

                # Set item attributes

                        # Text
                temp_text_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                        # Disable checkable flag
                temp_text_item.setFlags(temp_text_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)

                # Check change in sugg speed
                for i in range(len(self.ui_sugg_speed)):

                        # Check if new speed is different
                        if self.ui_sugg_speed[i] != self.ui_past_sugg_speed[i]:

                                # Set block text
                                block = self.set_block_text(i)

                                # Create log item
                                entry = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_item, entry)

                                # Set item text (sugg speed)
                                entry.setText(f'Block {block} sugg speed set to {round(self.ui_sugg_speed[i] / 1.609)} mph\n'
                                              f'Block {block} cmd speed set to {round(self.ui_cmd_speed[i] / 1.609)} mph')
                                
                                # Add log item
                                self.add_log_item(entry)

                # Check change in cmd authority
                for i in range(len(self.ui_cmd_authority)):

                        # Check if new authority is different
                        if self.ui_cmd_authority[i] != self.ui_past_cmd_authority[i]:

                                # Set block text
                                block = self.set_block_text(i)

                                # Create log item
                                entry = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_item, entry) 

                                # Set item text
                                entry.setText(f'Block {block} cmd auth set to {self.ui_cmd_authority[i]} blocks')
                                
                                # Add log item
                                self.add_log_item(entry)

                # Check change in switches
                for i in range(len(self.ui_switches)):

                        # Check if new switch position is different
                        if self.ui_switches[i] != self.ui_past_switches[i]:

                                # Set joint text
                                joint = self.set_joint_text(i)

                                # Set leg text
                                leg = self.set_leg_text(i, self.ui_switches[i])

                                # Create log item
                                entry = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_item, entry)

                                # Set item text
                                entry.setText(f'Section {joint} switched to section {leg}')
                                
                                # Add log item
                                self.add_log_item(entry)

                # Check change in crossings
                for i in range(len(self.ui_crossings)):

                        # Check if new crossing position is different
                        if self.ui_crossings[i] != self.ui_past_crossings[i]:

                                # Set gate text
                                gate = self.set_gate_text(i)

                                # Create log item
                                entry = QtWidgets.QTableWidgetItem()
                                self.copy_table_widget_item(temp_text_item, entry)

                                # Set item text
                                entry.setText(f'Section {gate} crossing CLOSED' if self.ui_crossings[i] else f'Section {gate} crossing OPEN')

                                # Add log item
                                self.add_log_item(entry)

                # Check change in Wayside 1 occupancy
                if self.wayside_1_occupied != self.wayside_1_past_occupied:

                        # Create log item
                        entry = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_item, entry)

                        # Set item text
                        entry.setText(f'{'Wayside 1 now OCCUPIED' if self.wayside_1_occupied else 'Wayside 1 now VACANT'}')

                        # Add log item
                        self.add_log_item(entry)

                # Check change in Wayside 2 occupancy
                if self.wayside_2_occupied != self.wayside_2_past_occupied:

                        # Create log item
                        entry = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_item, entry)

                        # Set item text
                        entry.setText(f'{'Wayside 2 now OCCUPIED' if self.wayside_2_occupied else 'Wayside 2 now VACANT'}')

                        # Add log item
                        self.add_log_item(entry)

                # Check change in Wayside 3 occupancy
                if self.wayside_3_occupied != self.wayside_3_past_occupied:

                        # Create log item
                        entry = QtWidgets.QTableWidgetItem()
                        self.copy_table_widget_item(temp_text_item, entry)

                        # Set item text
                        entry.setText(f'{'Wayside 3 now OCCUPIED' if self.wayside_3_occupied else 'Wayside 3 now VACANT'}')

                        # Add log item
                        self.add_log_item(entry)
                
        #########################################################################################
        #
        #                               Shell Handler function
        #
        #########################################################################################

        # Determine wayside occupancy
        def determine_wayside_occupancy(self):

                # Set past occupancy
                self.wayside_1_past_occupied = self.wayside_1_occupied
                self.wayside_2_past_occupied = self.wayside_2_occupied
                self.wayside_3_past_occupied = self.wayside_3_occupied

                # Reset wayside occupancy
                self.wayside_1_occupied = 0
                self.wayside_2_occupied = 0
                self.wayside_3_occupied = 0

                # Wayside 1
                for i in range(24):

                        # Check if block is occupied
                        if self.ui_occupancy[i]:

                                # Set wayside 1 occupancy
                                self.wayside_1_occupied = 1
                                break

                # Wayside 2
                for i in range(24, 46):

                        # Check if block is occupied
                        if self.ui_occupancy[i]:

                                # Set wayside 2 occupancy
                                self.wayside_2_occupied = 1
                                break
                
                # Blocks 105 -> 149 and Yard
                if not self.wayside_2_occupied:
                        for i in range(68, 78):

                                # Check if block is occupied
                                if self.ui_occupancy[i]:

                                        # Set wayside 2 occupancy
                                        self.wayside_2_occupied = 1
                                        break

                # Wayside 3
                for i in range(46, 68):

                        # Check if block is occupied
                        if self.ui_occupancy[i]:

                                # Set wayside 3 occupancy
                                self.wayside_3_occupied = 1
                                break

        # Determine operational mode
        def determine_operational_mode(self):

                # Wayside 1
                if self.wayside_1_occupied:

                        # Set operational mode to automatic
                        self.wayside_1_operational_mode = 2

                # Wayside 2
                if self.wayside_2_occupied:

                        # Set operational mode to automatic
                        self.wayside_2_operational_mode = 2

                # Wayside 3
                if self.wayside_3_occupied:

                        # Set operational mode to automatic
                        self.wayside_3_operational_mode = 2

        # Speed and Authority handler
        def shell_speed_auth_handler(self, sugg_speed: list, cmd_speed: list, sugg_auth: list, cmd_auth: list):

                # Set past speed and authority
                self.ui_past_sugg_speed = self.ui_sugg_speed.copy()
                self.ui_past_cmd_authority = self.ui_cmd_authority.copy()

                # Set new speed
                self.ui_sugg_speed = sugg_speed.copy()
                self.ui_cmd_speed = cmd_speed.copy()

                # Set new authority
                self.ui_sugg_authority = sugg_auth.copy()
                self.ui_cmd_authority = cmd_auth.copy()

        # Switch, Signal, and Crossing Handler
        def shell_switch_signal_crossing_handler(self, switch_cmds: list, signal_cmds: list, crossing_cmds: list):

                # Set past switch and crossing commands
                self.ui_past_switches = self.ui_switches.copy()
                self.ui_past_crossings = self.ui_crossings.copy()

                # Set new switch commands
                self.ui_switches = switch_cmds.copy()

                # Set new crossing commands
                self.ui_crossings = crossing_cmds.copy()

                # Set new signal commands
                self.ui_signals = signal_cmds.copy()

        # Occupancy Handler
        def shell_occupancy_handler(self, occupancy: list):

                # Set past occupancy
                self.ui_past_occupancy = self.ui_occupancy.copy()

                # Set new occupancy
                self.ui_occupancy = occupancy.copy()

                # Set new wayside occupancy
                self.determine_wayside_occupancy()

                # Set new operational mode
                self.determine_operational_mode()
                



#########################################################################################
#
#                           Main execution (RED LINE COMPLETE)
#
#########################################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = wayside_ui_red_line()
    sys.exit(app.exec())