# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# Program:          Wayside User Interface      
#
# Created:          11/05/2024
# Last Update:      11/11/2024
# Last Updated by:  Zachary McPherson
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the Wayside user interface program for the Train Control System.
#        This program allows the execution of PLC programs
#        This program communicates with the Wayside Shell file


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QWidget
import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class Ui_MainWindow(QWidget):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1430, 1038)
                MainWindow.setMinimumSize(QtCore.QSize(1430, 1000))
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
                self.FilterFrame.setGeometry(QtCore.QRect(0, 250, 401, 741))
                self.FilterFrame.setStyleSheet("background-color: rgb(204, 204, 204);\n"
                "border: 3px solid black;\n"
                "")
                self.FilterFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.FilterFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
                self.FilterFrame.setObjectName("FilterFrame")
                self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.FilterFrame)
                self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 401, 741))
                self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
                self.FilterList_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
                self.FilterList_Layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
                self.FilterList_Layout.setContentsMargins(70, 0, 70, 0)
                self.FilterList_Layout.setSpacing(7)
                self.FilterList_Layout.setObjectName("FilterList_Layout")
                self.SpeedButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SpeedButton.setMinimumSize(QtCore.QSize(260, 60))
                self.SpeedButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SpeedButton.setObjectName("SpeedButton")
                self.FilterList_Layout.addWidget(self.SpeedButton)
                self.AuthorityButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.AuthorityButton.setMinimumSize(QtCore.QSize(260, 60))
                self.AuthorityButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.AuthorityButton.setObjectName("AuthorityButton")
                self.FilterList_Layout.addWidget(self.AuthorityButton)
                self.SwitchButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SwitchButton.setMinimumSize(QtCore.QSize(260, 60))
                self.SwitchButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SwitchButton.setObjectName("SwitchButton")
                self.FilterList_Layout.addWidget(self.SwitchButton)
                self.SignalButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.SignalButton.setMinimumSize(QtCore.QSize(260, 60))
                self.SignalButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.SignalButton.setObjectName("SignalButton")
                self.FilterList_Layout.addWidget(self.SignalButton)
                self.OccupancyButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.OccupancyButton.setMinimumSize(QtCore.QSize(260, 60))
                self.OccupancyButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.OccupancyButton.setObjectName("OccupancyButton")
                self.FilterList_Layout.addWidget(self.OccupancyButton)
                self.CrossingButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
                self.CrossingButton.setMinimumSize(QtCore.QSize(260, 60))
                self.CrossingButton.setStyleSheet("font: 15pt \"Times New Roman\";\n"
                "border: none;\n"
                "background-color: rgb(255, 255, 255);\n"
                "border-radius: 5px;")
                self.CrossingButton.setObjectName("CrossingButton")
                self.FilterList_Layout.addWidget(self.CrossingButton)
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 160, 401, 91))
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
                self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(400, 160, 601, 831))
                self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
                self.dataTable_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
                self.dataTable_layout.setContentsMargins(0, 0, 0, 0)
                self.dataTable_layout.setObjectName("dataTable_layout")
                self.ControllerHeader_layout = QtWidgets.QVBoxLayout()
                self.ControllerHeader_layout.setObjectName("ControllerHeader_layout")
                self.DataTable = QtWidgets.QTableWidget(parent=self.verticalLayoutWidget_6)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                self.DataTable.setFont(font)
                self.DataTable.setStyleSheet("QTableWidget {\n"
                "                background-color: rgb(159, 197, 248);\n"
                "                border: 2px solid black;\n"
                "        }\n"
                "        QTableWidget::item {\n"
                "                color: black;\n"
                "                background-color: rgb(159, 197, 248);\n"
                "                font-weight: bold;\n"
                "        }\n"
                "        QTableWidget::item:alternate {\n"
                "                background-color: rgb(255, 255, 255);\n"
                "                font-weight: bold;\n"
                "        }")
                self.DataTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                self.DataTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.DataTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                self.DataTable.setAlternatingRowColors(True)
                self.DataTable.setShowGrid(False)
                self.DataTable.setRowCount(24)
                self.DataTable.setColumnCount(3)
                self.DataTable.setObjectName("DataTable")
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignVCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignVCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignVCenter)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setBackground(QtGui.QColor(204, 204, 204))
                self.DataTable.setHorizontalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(0, 0, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(1, 0, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(1, 1, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(1, 2, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(2, 0, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(2, 1, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(3, 0, item)
                item = QtWidgets.QTableWidgetItem()
                self.DataTable.setItem(3, 2, item)
                self.DataTable.horizontalHeader().setDefaultSectionSize(195)
                self.DataTable.horizontalHeader().setMinimumSectionSize(40)
                self.DataTable.verticalHeader().setVisible(False)
                self.DataTable.verticalHeader().setDefaultSectionSize(33)
                self.ControllerHeader_layout.addWidget(self.DataTable)
                self.dataTable_layout.addLayout(self.ControllerHeader_layout)
                self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(1000, 160, 401, 91))
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
                self.UpdateFrame.setGeometry(QtCore.QRect(1000, 250, 401, 741))
                self.UpdateFrame.setStyleSheet("background-color: rgb(204, 204, 204);\n"
                "border: 3px solid black;")
                self.UpdateFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.UpdateFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.UpdateFrame.setObjectName("UpdateFrame")
                self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.UpdateFrame)
                self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 401, 741))
                self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
                self.UpdateLog_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
                self.UpdateLog_layout.setContentsMargins(0, 0, 0, 0)
                self.UpdateLog_layout.setObjectName("UpdateLog_layout")
                self.UpdateLog = QtWidgets.QTableWidget(parent=self.verticalLayoutWidget_5)
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                self.UpdateLog.setFont(font)
                self.UpdateLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.UpdateLog.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                self.UpdateLog.setShowGrid(True)
                self.UpdateLog.setRowCount(0)
                self.UpdateLog.setColumnCount(1)
                self.UpdateLog.setObjectName("UpdateLog")
                item = QtWidgets.QTableWidgetItem()
                self.UpdateLog.setHorizontalHeaderItem(0, item)
                self.UpdateLog.horizontalHeader().setVisible(False)
                self.UpdateLog.horizontalHeader().setDefaultSectionSize(279)
                self.UpdateLog.horizontalHeader().setHighlightSections(True)
                self.UpdateLog.verticalHeader().setVisible(False)
                self.UpdateLog.verticalHeader().setCascadingSectionResizes(False)
                self.UpdateLog.verticalHeader().setDefaultSectionSize(60)
                self.UpdateLog.verticalHeader().setHighlightSections(False)
                self.UpdateLog_layout.addWidget(self.UpdateLog)
                self.ControllerHeader = QtWidgets.QLabel(parent=self.Controller)
                self.ControllerHeader.setGeometry(QtCore.QRect(0, 1, 1401, 161))
                self.ControllerHeader.setStyleSheet("background-color: rgb(43, 120, 228);\n"
                "font: 36pt \"Times New Roman\";\n"
                "color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.ControllerHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ControllerHeader.setIndent(0)
                self.ControllerHeader.setObjectName("ControllerHeader")
                self.WaysideSelectComboBox = QtWidgets.QComboBox(parent=self.Controller)
                self.WaysideSelectComboBox.setGeometry(QtCore.QRect(210, 90, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.WaysideSelectComboBox.setFont(font)
                self.WaysideSelectComboBox.setStyleSheet("border: 2px solid black;")
                self.WaysideSelectComboBox.setCurrentText("")
                self.WaysideSelectComboBox.setObjectName("WaysideSelectComboBox")
                self.WaysideSelectComboBoxLabel = QtWidgets.QLabel(parent=self.Controller)
                self.WaysideSelectComboBoxLabel.setGeometry(QtCore.QRect(210, 50, 151, 31))
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
                self.UploadPLCButton.setGeometry(QtCore.QRect(1110, 60, 191, 61))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.UploadPLCButton.setFont(font)
                self.UploadPLCButton.setStyleSheet("border: 2px solid black;\n"
                "border-radius: 5px;")
                self.UploadPLCButton.setObjectName("UploadPLCButton")
                self.LineSelectComboBox = QtWidgets.QComboBox(parent=self.Controller)
                self.LineSelectComboBox.setGeometry(QtCore.QRect(40, 90, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.LineSelectComboBox.setFont(font)
                self.LineSelectComboBox.setStyleSheet("border: 2px solid black;")
                self.LineSelectComboBox.setCurrentText("")
                self.LineSelectComboBox.setObjectName("LineSelectComboBox")
                self.LineSelectComboBox.addItem("")
                self.LineSelectComboBox.setItemText(0, "")
                self.LineSelectComboBox.addItem("")
                self.LineSelectComboBox.addItem("")
                self.LineSelectComboBoxLabel = QtWidgets.QLabel(parent=self.Controller)
                self.LineSelectComboBoxLabel.setGeometry(QtCore.QRect(40, 50, 151, 31))
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
                self.ControllerHeader.raise_()
                self.FilterFrame.raise_()
                self.verticalLayoutWidget_2.raise_()
                self.verticalLayoutWidget_6.raise_()
                self.verticalLayoutWidget_4.raise_()
                self.UpdateFrame.raise_()
                self.WaysideSelectComboBox.raise_()
                self.WaysideSelectComboBoxLabel.raise_()
                self.UploadPLCButton.raise_()
                self.LineSelectComboBox.raise_()
                self.LineSelectComboBoxLabel.raise_()
                self.tabWidget.addTab(self.Controller, "")
                self.TestBench = QtWidgets.QWidget()
                self.TestBench.setObjectName("TestBench")
                self.verticalLayoutWidget_8 = QtWidgets.QWidget(parent=self.TestBench)
                self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(0, 0, 1401, 161))
                self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
                self.TestBenchHeader_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
                self.TestBenchHeader_Layout.setContentsMargins(0, 0, 0, 0)
                self.TestBenchHeader_Layout.setObjectName("TestBenchHeader_Layout")
                self.TestBenchHeader = QtWidgets.QLabel(parent=self.verticalLayoutWidget_8)
                self.TestBenchHeader.setStyleSheet("background-color: rgb(43, 120, 228);\n"
                "font: 36pt \"Times New Roman\";\n"
                "color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.TestBenchHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TestBenchHeader.setIndent(0)
                self.TestBenchHeader.setObjectName("TestBenchHeader")
                self.TestBenchHeader_Layout.addWidget(self.TestBenchHeader)
                self.CTCInputHeader = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputHeader.setGeometry(QtCore.QRect(40, 210, 351, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputHeader.setFont(font)
                self.CTCInputHeader.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
                self.CTCInputHeader.setStyleSheet("background-color: rgb(221, 221, 221);\n"
                "border: 2px solid black;")
                self.CTCInputHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputHeader.setObjectName("CTCInputHeader")
                self.CTCInputSecIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCInputSecIndex.setGeometry(QtCore.QRect(40, 290, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputSecIndex.setFont(font)
                self.CTCInputSecIndex.setStyleSheet("border: 2px solid black;")
                self.CTCInputSecIndex.setObjectName("CTCInputSecIndex")
                self.CTCInputBlockIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCInputBlockIndex.setGeometry(QtCore.QRect(40, 380, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputBlockIndex.setFont(font)
                self.CTCInputBlockIndex.setStyleSheet("border: 2px solid black;")
                self.CTCInputBlockIndex.setObjectName("CTCInputBlockIndex")
                self.CTCInputSecIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputSecIndexLabel.setGeometry(QtCore.QRect(210, 290, 171, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputSecIndexLabel.setFont(font)
                self.CTCInputSecIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputSecIndexLabel.setObjectName("CTCInputSecIndexLabel")
                self.CTCInputBlockIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputBlockIndexLabel.setGeometry(QtCore.QRect(210, 380, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputBlockIndexLabel.setFont(font)
                self.CTCInputBlockIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputBlockIndexLabel.setObjectName("CTCInputBlockIndexLabel")
                self.CTCInputSuggSpeedLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputSuggSpeedLabel.setGeometry(QtCore.QRect(210, 540, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputSuggSpeedLabel.setFont(font)
                self.CTCInputSuggSpeedLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputSuggSpeedLabel.setObjectName("CTCInputSuggSpeedLabel")
                self.CTCInputSuggSpeed = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCInputSuggSpeed.setGeometry(QtCore.QRect(40, 540, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputSuggSpeed.setFont(font)
                self.CTCInputSuggSpeed.setStyleSheet("border: 2px solid black;")
                self.CTCInputSuggSpeed.setObjectName("CTCInputSuggSpeed")
                self.CTCInputSuggAuthLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputSuggAuthLabel.setGeometry(QtCore.QRect(210, 630, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputSuggAuthLabel.setFont(font)
                self.CTCInputSuggAuthLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputSuggAuthLabel.setObjectName("CTCInputSuggAuthLabel")
                self.CTCInputSuggAuth = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCInputSuggAuth.setGeometry(QtCore.QRect(40, 630, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputSuggAuth.setFont(font)
                self.CTCInputSuggAuth.setStyleSheet("border: 2px solid black;")
                self.CTCInputSuggAuth.setObjectName("CTCInputSuggAuth")
                self.CTCInputSuggSWLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputSuggSWLabel.setGeometry(QtCore.QRect(210, 460, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputSuggSWLabel.setFont(font)
                self.CTCInputSuggSWLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputSuggSWLabel.setObjectName("CTCInputSuggSWLabel")
                self.CTCInputSaveButton = QtWidgets.QPushButton(parent=self.TestBench)
                self.CTCInputSaveButton.setGeometry(QtCore.QRect(40, 710, 331, 41))
                self.CTCInputSaveButton.setStyleSheet("border: 2px solid black;\n"
                "background-color: rgb(255, 255, 255);\n"
                "font: 75 12pt \"Times New Roman\";")
                self.CTCInputSaveButton.setFlat(True)
                self.CTCInputSaveButton.setObjectName("CTCInputSaveButton")
                self.TRKInputHeader = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputHeader.setGeometry(QtCore.QRect(420, 210, 281, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputHeader.setFont(font)
                self.TRKInputHeader.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
                self.TRKInputHeader.setStyleSheet("background-color: rgb(221, 221, 221);\n"
                "border: 2px solid black;")
                self.TRKInputHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputHeader.setObjectName("TRKInputHeader")
                self.TRKInputBlockIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputBlockIndexLabel.setGeometry(QtCore.QRect(590, 360, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputBlockIndexLabel.setFont(font)
                self.TRKInputBlockIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputBlockIndexLabel.setObjectName("TRKInputBlockIndexLabel")
                self.TRKInputSecIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputSecIndex.setGeometry(QtCore.QRect(420, 290, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputSecIndex.setFont(font)
                self.TRKInputSecIndex.setStyleSheet("border: 2px solid black;")
                self.TRKInputSecIndex.setObjectName("TRKInputSecIndex")
                self.TRKInputSecIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputSecIndexLabel.setGeometry(QtCore.QRect(590, 290, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputSecIndexLabel.setFont(font)
                self.TRKInputSecIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputSecIndexLabel.setObjectName("TRKInputSecIndexLabel")
                self.TRKInputBlockIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputBlockIndex.setGeometry(QtCore.QRect(420, 360, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputBlockIndex.setFont(font)
                self.TRKInputBlockIndex.setStyleSheet("border: 2px solid black;")
                self.TRKInputBlockIndex.setObjectName("TRKInputBlockIndex")
                self.CTCInputSuggSW = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCInputSuggSW.setGeometry(QtCore.QRect(40, 459, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputSuggSW.setFont(font)
                self.CTCInputSuggSW.setStyleSheet("border: 2px solid black;")
                self.CTCInputSuggSW.setObjectName("CTCInputSuggSW")
                self.TRKInputSWStatus = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputSWStatus.setGeometry(QtCore.QRect(420, 500, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputSWStatus.setFont(font)
                self.TRKInputSWStatus.setStyleSheet("border: 2px solid black;")
                self.TRKInputSWStatus.setObjectName("TRKInputSWStatus")
                self.TRKInputSWStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputSWStatusLabel.setGeometry(QtCore.QRect(590, 500, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputSWStatusLabel.setFont(font)
                self.TRKInputSWStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputSWStatusLabel.setObjectName("TRKInputSWStatusLabel")
                self.TRKInputSigStatus = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputSigStatus.setGeometry(QtCore.QRect(420, 570, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputSigStatus.setFont(font)
                self.TRKInputSigStatus.setStyleSheet("border: 2px solid black;")
                self.TRKInputSigStatus.setObjectName("TRKInputSigStatus")
                self.TRKInputSigStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputSigStatusLabel.setGeometry(QtCore.QRect(590, 570, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputSigStatusLabel.setFont(font)
                self.TRKInputSigStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputSigStatusLabel.setObjectName("TRKInputSigStatusLabel")
                self.TRKInputCrossStatus = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputCrossStatus.setGeometry(QtCore.QRect(420, 640, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputCrossStatus.setFont(font)
                self.TRKInputCrossStatus.setStyleSheet("border: 2px solid black;")
                self.TRKInputCrossStatus.setObjectName("TRKInputCrossStatus")
                self.TRKInputCrossStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputCrossStatusLabel.setGeometry(QtCore.QRect(590, 640, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputCrossStatusLabel.setFont(font)
                self.TRKInputCrossStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputCrossStatusLabel.setObjectName("TRKInputCrossStatusLabel")
                self.TRKInputOcc = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputOcc.setGeometry(QtCore.QRect(420, 430, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputOcc.setFont(font)
                self.TRKInputOcc.setStyleSheet("border: 2px solid black;")
                self.TRKInputOcc.setObjectName("TRKInputOcc")
                self.TRKInputOccLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputOccLabel.setGeometry(QtCore.QRect(590, 430, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputOccLabel.setFont(font)
                self.TRKInputOccLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputOccLabel.setObjectName("TRKInputOccLabel")
                self.TRKInputSaveButton = QtWidgets.QPushButton(parent=self.TestBench)
                self.TRKInputSaveButton.setGeometry(QtCore.QRect(420, 710, 281, 41))
                self.TRKInputSaveButton.setStyleSheet("border: 2px solid black;\n"
                "background-color: rgb(255, 255, 255);\n"
                "font: 75 12pt \"Times New Roman\";")
                self.TRKInputSaveButton.setFlat(True)
                self.TRKInputSaveButton.setObjectName("TRKInputSaveButton")
                self.TRKOutputSigCmdLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputSigCmdLabel.setGeometry(QtCore.QRect(1250, 590, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputSigCmdLabel.setFont(font)
                self.TRKOutputSigCmdLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputSigCmdLabel.setObjectName("TRKOutputSigCmdLabel")
                self.TRKOutputCmdSpeedLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputCmdSpeedLabel.setGeometry(QtCore.QRect(1250, 410, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputCmdSpeedLabel.setFont(font)
                self.TRKOutputCmdSpeedLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCmdSpeedLabel.setObjectName("TRKOutputCmdSpeedLabel")
                self.CTCOutputSecIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCOutputSecIndex.setGeometry(QtCore.QRect(750, 290, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCOutputSecIndex.setFont(font)
                self.CTCOutputSecIndex.setStyleSheet("border: 2px solid black;")
                self.CTCOutputSecIndex.setObjectName("CTCOutputSecIndex")
                self.TRKOutputSecIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKOutputSecIndex.setGeometry(QtCore.QRect(1080, 290, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKOutputSecIndex.setFont(font)
                self.TRKOutputSecIndex.setStyleSheet("border: 2px solid black;")
                self.TRKOutputSecIndex.setObjectName("TRKOutputSecIndex")
                self.CTCOutputOccLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputOccLabel.setGeometry(QtCore.QRect(920, 430, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputOccLabel.setFont(font)
                self.CTCOutputOccLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputOccLabel.setObjectName("CTCOutputOccLabel")
                self.TRKOutputBlockIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKOutputBlockIndex.setGeometry(QtCore.QRect(1080, 350, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKOutputBlockIndex.setFont(font)
                self.TRKOutputBlockIndex.setStyleSheet("border: 2px solid black;")
                self.TRKOutputBlockIndex.setObjectName("TRKOutputBlockIndex")
                self.CTCOutputBlockIndex = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCOutputBlockIndex.setGeometry(QtCore.QRect(750, 360, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCOutputBlockIndex.setFont(font)
                self.CTCOutputBlockIndex.setStyleSheet("border: 2px solid black;")
                self.CTCOutputBlockIndex.setObjectName("CTCOutputBlockIndex")
                self.TRKOutputSecIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputSecIndexLabel.setGeometry(QtCore.QRect(1250, 290, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputSecIndexLabel.setFont(font)
                self.TRKOutputSecIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputSecIndexLabel.setObjectName("TRKOutputSecIndexLabel")
                self.TRKOutputSWCmdLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputSWCmdLabel.setGeometry(QtCore.QRect(1250, 530, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputSWCmdLabel.setFont(font)
                self.TRKOutputSWCmdLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputSWCmdLabel.setObjectName("TRKOutputSWCmdLabel")
                self.CTCOutputHeader = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputHeader.setGeometry(QtCore.QRect(750, 210, 281, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.CTCOutputHeader.setFont(font)
                self.CTCOutputHeader.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
                self.CTCOutputHeader.setStyleSheet("background-color: rgb(221, 221, 221);\n"
                "border: 2px solid black;")
                self.CTCOutputHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputHeader.setObjectName("CTCOutputHeader")
                self.CTCOutputSecIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputSecIndexLabel.setGeometry(QtCore.QRect(920, 290, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputSecIndexLabel.setFont(font)
                self.CTCOutputSecIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputSecIndexLabel.setObjectName("CTCOutputSecIndexLabel")
                self.CTCOutputBlockIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputBlockIndexLabel.setGeometry(QtCore.QRect(920, 360, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputBlockIndexLabel.setFont(font)
                self.CTCOutputBlockIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputBlockIndexLabel.setObjectName("CTCOutputBlockIndexLabel")
                self.TRKOutputHeader = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputHeader.setGeometry(QtCore.QRect(1080, 210, 281, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.TRKOutputHeader.setFont(font)
                self.TRKOutputHeader.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
                self.TRKOutputHeader.setStyleSheet("background-color: rgb(221, 221, 221);\n"
                "border: 2px solid black;")
                self.TRKOutputHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputHeader.setObjectName("TRKOutputHeader")
                self.TRKOutputBlockIndexLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputBlockIndexLabel.setGeometry(QtCore.QRect(1250, 350, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputBlockIndexLabel.setFont(font)
                self.TRKOutputBlockIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputBlockIndexLabel.setObjectName("TRKOutputBlockIndexLabel")
                self.TRKOutputCrossCmdLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputCrossCmdLabel.setGeometry(QtCore.QRect(1250, 650, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputCrossCmdLabel.setFont(font)
                self.TRKOutputCrossCmdLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCrossCmdLabel.setObjectName("TRKOutputCrossCmdLabel")
                self.TRKOutputCmdAuthLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKOutputCmdAuthLabel.setGeometry(QtCore.QRect(1250, 470, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKOutputCmdAuthLabel.setFont(font)
                self.TRKOutputCmdAuthLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCmdAuthLabel.setObjectName("TRKOutputCmdAuthLabel")
                self.CTCOutputOcc = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCOutputOcc.setGeometry(QtCore.QRect(750, 430, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.CTCOutputOcc.setFont(font)
                self.CTCOutputOcc.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.CTCOutputOcc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputOcc.setReadOnly(True)
                self.CTCOutputOcc.setObjectName("CTCOutputOcc")
                self.CTCOutputSWStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputSWStatusLabel.setGeometry(QtCore.QRect(920, 500, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputSWStatusLabel.setFont(font)
                self.CTCOutputSWStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputSWStatusLabel.setObjectName("CTCOutputSWStatusLabel")
                self.CTCOutputSWStatus = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCOutputSWStatus.setGeometry(QtCore.QRect(750, 500, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.CTCOutputSWStatus.setFont(font)
                self.CTCOutputSWStatus.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.CTCOutputSWStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputSWStatus.setReadOnly(True)
                self.CTCOutputSWStatus.setObjectName("CTCOutputSWStatus")
                self.CTCOutputSigStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputSigStatusLabel.setGeometry(QtCore.QRect(920, 570, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputSigStatusLabel.setFont(font)
                self.CTCOutputSigStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputSigStatusLabel.setObjectName("CTCOutputSigStatusLabel")
                self.CTCOutputSigStatus = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCOutputSigStatus.setGeometry(QtCore.QRect(750, 570, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.CTCOutputSigStatus.setFont(font)
                self.CTCOutputSigStatus.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.CTCOutputSigStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputSigStatus.setReadOnly(True)
                self.CTCOutputSigStatus.setObjectName("CTCOutputSigStatus")
                self.CTCOutputCrossStatusLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCOutputCrossStatusLabel.setGeometry(QtCore.QRect(920, 640, 111, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCOutputCrossStatusLabel.setFont(font)
                self.CTCOutputCrossStatusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputCrossStatusLabel.setObjectName("CTCOutputCrossStatusLabel")
                self.CTCOutputCrossStatus = QtWidgets.QLineEdit(parent=self.TestBench)
                self.CTCOutputCrossStatus.setGeometry(QtCore.QRect(750, 640, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.CTCOutputCrossStatus.setFont(font)
                self.CTCOutputCrossStatus.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.CTCOutputCrossStatus.setText("")
                self.CTCOutputCrossStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCOutputCrossStatus.setReadOnly(True)
                self.CTCOutputCrossStatus.setObjectName("CTCOutputCrossStatus")
                self.TRKOutputCmdSpeed = QtWidgets.QLineEdit(parent=self.TestBench)
                self.TRKOutputCmdSpeed.setGeometry(QtCore.QRect(1080, 410, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.TRKOutputCmdSpeed.setFont(font)
                self.TRKOutputCmdSpeed.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.TRKOutputCmdSpeed.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCmdSpeed.setReadOnly(True)
                self.TRKOutputCmdSpeed.setObjectName("TRKOutputCmdSpeed")
                self.TRKOutputCmdAuth = QtWidgets.QLineEdit(parent=self.TestBench)
                self.TRKOutputCmdAuth.setGeometry(QtCore.QRect(1080, 470, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.TRKOutputCmdAuth.setFont(font)
                self.TRKOutputCmdAuth.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.TRKOutputCmdAuth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCmdAuth.setReadOnly(True)
                self.TRKOutputCmdAuth.setObjectName("TRKOutputCmdAuth")
                self.TRKOutputSWCmd = QtWidgets.QLineEdit(parent=self.TestBench)
                self.TRKOutputSWCmd.setGeometry(QtCore.QRect(1080, 530, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.TRKOutputSWCmd.setFont(font)
                self.TRKOutputSWCmd.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.TRKOutputSWCmd.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputSWCmd.setReadOnly(True)
                self.TRKOutputSWCmd.setObjectName("TRKOutputSWCmd")
                self.TRKOutputSigCmd = QtWidgets.QLineEdit(parent=self.TestBench)
                self.TRKOutputSigCmd.setGeometry(QtCore.QRect(1080, 590, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.TRKOutputSigCmd.setFont(font)
                self.TRKOutputSigCmd.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.TRKOutputSigCmd.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputSigCmd.setReadOnly(True)
                self.TRKOutputSigCmd.setObjectName("TRKOutputSigCmd")
                self.TRKOutputCrossCmd = QtWidgets.QLineEdit(parent=self.TestBench)
                self.TRKOutputCrossCmd.setGeometry(QtCore.QRect(1080, 650, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                self.TRKOutputCrossCmd.setFont(font)
                self.TRKOutputCrossCmd.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font: 10pt \"Times New Roman\";")
                self.TRKOutputCrossCmd.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKOutputCrossCmd.setReadOnly(True)
                self.TRKOutputCrossCmd.setObjectName("TRKOutputCrossCmd")
                self.CTCInputSelection = QtWidgets.QComboBox(parent=self.TestBench)
                self.CTCInputSelection.setGeometry(QtCore.QRect(40, 790, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.CTCInputSelection.setFont(font)
                self.CTCInputSelection.setStyleSheet("border: 2px solid black;")
                self.CTCInputSelection.setObjectName("CTCInputSelection")
                self.CTCInputSelectionLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.CTCInputSelectionLabel.setGeometry(QtCore.QRect(210, 790, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.CTCInputSelectionLabel.setFont(font)
                self.CTCInputSelectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.CTCInputSelectionLabel.setObjectName("CTCInputSelectionLabel")
                self.TRKInputSelection = QtWidgets.QComboBox(parent=self.TestBench)
                self.TRKInputSelection.setGeometry(QtCore.QRect(420, 790, 141, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.TRKInputSelection.setFont(font)
                self.TRKInputSelection.setStyleSheet("border: 2px solid black;")
                self.TRKInputSelection.setObjectName("TRKInputSelection")
                self.TRKInputSelectionLabel = QtWidgets.QLabel(parent=self.TestBench)
                self.TRKInputSelectionLabel.setGeometry(QtCore.QRect(580, 790, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(12)
                self.TRKInputSelectionLabel.setFont(font)
                self.TRKInputSelectionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.TRKInputSelectionLabel.setObjectName("TRKInputSelectionLabel")
                self.tabWidget.addTab(self.TestBench, "")
                self.horizontalLayout.addWidget(self.tabWidget)
                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi(MainWindow)
                self.tabWidget.setCurrentIndex(0)
                self.WaysideSelectComboBox.setCurrentIndex(-1)
                self.LineSelectComboBox.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ############################################################################################################
        #
        #                                       SIGNALS AND SLOTS
        #
        ############################################################################################################

                # Line Select ComboBox
                self.LineSelectComboBox.currentIndexChanged.connect(self.update_wayside_select_combobox)

                # Wayside Select ComboBox
                self.WaysideSelectComboBox.currentIndexChanged.connect(self.clear_table)

                # Filter Buttons
                self.SpeedButton.clicked.connect(lambda: self.filter_button_clicked(1))
                self.AuthorityButton.clicked.connect(lambda: self.filter_button_clicked(2))
                self.SwitchButton.clicked.connect(lambda: self.filter_button_clicked(3))
                self.SignalButton.clicked.connect(lambda: self.filter_button_clicked(4))
                self.OccupancyButton.clicked.connect(lambda: self.filter_button_clicked(5))
                self.CrossingButton.clicked.connect(lambda: self.filter_button_clicked(6))

                # Upload PLC Button
                self.UploadPLCButton.clicked.connect(self.open_file_dialog)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.SpeedButton.setText(_translate("MainWindow", "Speed"))
                self.AuthorityButton.setText(_translate("MainWindow", "Authority"))
                self.SwitchButton.setText(_translate("MainWindow", "Switches"))
                self.SignalButton.setText(_translate("MainWindow", "Signals"))
                self.OccupancyButton.setText(_translate("MainWindow", "Occupancy"))
                self.CrossingButton.setText(_translate("MainWindow", "Crossings"))
                self.FilterHeader.setText(_translate("MainWindow", "Filter List"))
                self.DataTable.setSortingEnabled(False)
                __sortingEnabled = self.DataTable.isSortingEnabled()
                self.DataTable.setSortingEnabled(False)
                self.DataTable.setSortingEnabled(__sortingEnabled)
                self.UpdateHeader.setText(_translate("MainWindow", "Updates"))
                item = self.UpdateLog.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "UpdateLog"))
                self.ControllerHeader.setText(_translate("MainWindow", "Wayside Controller"))
                self.WaysideSelectComboBoxLabel.setText(_translate("MainWindow", "Wayside"))
                self.UploadPLCButton.setText(_translate("MainWindow", "Upload PLC"))
                self.LineSelectComboBox.setItemText(1, _translate("MainWindow", "Green Line"))
                self.LineSelectComboBox.setItemText(2, _translate("MainWindow", "Red Line"))
                self.LineSelectComboBoxLabel.setText(_translate("MainWindow", "Line"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.Controller), _translate("MainWindow", "Controller"))
                self.TestBenchHeader.setText(_translate("MainWindow", "Test Bench"))
                self.CTCInputHeader.setText(_translate("MainWindow", "Inputs from CTC"))
                self.CTCInputSecIndexLabel.setText(_translate("MainWindow", "Section Index"))
                self.CTCInputBlockIndexLabel.setText(_translate("MainWindow", "Block Index"))
                self.CTCInputSuggSpeedLabel.setText(_translate("MainWindow", "Sugg. Speed (km/hr)"))
                self.CTCInputSuggAuthLabel.setText(_translate("MainWindow", "Sugg. Auth (meter)"))
                self.CTCInputSuggSWLabel.setText(_translate("MainWindow", "Sugg. SW"))
                self.CTCInputSaveButton.setText(_translate("MainWindow", "SAVE"))
                self.TRKInputHeader.setText(_translate("MainWindow", "Inputs from TRK Model"))
                self.TRKInputBlockIndexLabel.setText(_translate("MainWindow", "Block Index"))
                self.TRKInputSecIndexLabel.setText(_translate("MainWindow", "Section Index"))
                self.TRKInputSWStatusLabel.setText(_translate("MainWindow", "SW Status"))
                self.TRKInputSigStatusLabel.setText(_translate("MainWindow", "Sig. Status"))
                self.TRKInputCrossStatusLabel.setText(_translate("MainWindow", "Cross Status"))
                self.TRKInputOccLabel.setText(_translate("MainWindow", "Occupancy"))
                self.TRKInputSaveButton.setText(_translate("MainWindow", "SAVE"))
                self.TRKOutputSigCmdLabel.setText(_translate("MainWindow", "Sig. Cmd."))
                self.TRKOutputCmdSpeedLabel.setText(_translate("MainWindow", "Cmd. Speed"))
                self.CTCOutputOccLabel.setText(_translate("MainWindow", "Occupancy"))
                self.TRKOutputSecIndexLabel.setText(_translate("MainWindow", "Section Index"))
                self.TRKOutputSWCmdLabel.setText(_translate("MainWindow", "SW Cmd."))
                self.CTCOutputHeader.setText(_translate("MainWindow", "Outputs to CTC"))
                self.CTCOutputSecIndexLabel.setText(_translate("MainWindow", "Section Index"))
                self.CTCOutputBlockIndexLabel.setText(_translate("MainWindow", "Block Index"))
                self.TRKOutputHeader.setText(_translate("MainWindow", "Outputs to TRK Model"))
                self.TRKOutputBlockIndexLabel.setText(_translate("MainWindow", "Block Index"))
                self.TRKOutputCrossCmdLabel.setText(_translate("MainWindow", "Cross Cmd."))
                self.TRKOutputCmdAuthLabel.setText(_translate("MainWindow", "Cmd. Auth"))
                self.CTCOutputSWStatusLabel.setText(_translate("MainWindow", "SW Status"))
                self.CTCOutputSigStatusLabel.setText(_translate("MainWindow", "Sig. Status"))
                self.CTCOutputCrossStatusLabel.setText(_translate("MainWindow", "Cross Status"))
                self.CTCInputSelectionLabel.setText(_translate("MainWindow", "Input Selection"))
                self.TRKInputSelectionLabel.setText(_translate("MainWindow", "Input Selection"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.TestBench), _translate("MainWindow", "Test Bench"))

        ######################################
        #       Green Line Variables
        ######################################

        selected_filter = 0 # 1 = Speed, 2 = Authority, 3 = Switches, 4 = Signals, 5 = Occupancy, 6 = Crossings
        green_line_block_occupancy = [0] * 151
        green_line_sugg_speed = [None] * 151
        green_line_sugg_auth = [None] * 151
        green_line_cmd_speed = [None] * 151
        green_line_cmd_auth = [None] * 151

        #                     D   F   I   K  N1  N2
        green_line_sw_cmd = [ 0,  1,  0,  1,  1,  0 ]

        #                      C   D   F   G   J   K  N1  N2   O   R  Yard 
        green_line_sig_cmd = [ 0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  0 ]

        #                       E  T
        green_line_cross_cmd = [0, 0]

        processes = []

        #########################################
        #       Update UI Elements
        #########################################

        ####################
        #  Update Table
        ####################

        # Update Wayside Select ComboBox
        def update_wayside_select_combobox(self):
                # Clear Contents
                self.WaysideSelectComboBox.clear()

                # Green Line selected
                if self.LineSelectComboBox.currentText() == "Green Line":
                        self.WaysideSelectComboBox.addItem(None)
                        self.WaysideSelectComboBox.addItem("1")
                        self.WaysideSelectComboBox.addItem("2")
                        self.WaysideSelectComboBox.addItem("3")

                # Red Line selected
                elif self.LineSelectComboBox.currentText() == "Red Line":
                        self.clear_filter_button() 
        
        def clear_table(self):
                self.selected_filter = 0
                self.update_table(0)

        # Update Filter Button Background
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

        # Update current selected filter button
        def update_filter_button(self, filter):
                
                style_sheet_yellow = """font: 15pt \"Times New Roman\";
                                    border: none;
                                    background-color: rgb(255, 255, 0);
                                    border-radius: 5px;"""

                # Reset all buttons to white
                self.clear_filter_button()

                # Set selected button to yellow
                if filter != self.selected_filter and self.LineSelectComboBox.currentText() == "Green Line":
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

        # Update Table Contents
        def update_table(self):

                # Default Values
                default_row_count = 24

                # Clear Table
                self.DataTable.clear()
                
                # Set Table based on Line and Wayside selection
                if self.LineSelectComboBox.currentText() == "Green Line" and self.selected_filter != 0:
                        
                        # Speed Filter
                        if self.selected_filter == 1:

                                # Set Table Column Headers
                                self.DataTable.setHorizontalHeaderLabels(["Block", "Sugg. Speed", "Cmd. Speed"])

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:

                                        # Set Table Size
                                        self.DataTable.setRowCount(150)

                                        # Set Yard Block speed data
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[0] if self.green_line_sugg_speed[0] != None else "None"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[0] if self.green_line_cmd_speed[0] != None else "None"))

                                        # Fill Table with rest of block speed data
                                        for i in range(1, 151):

                                                self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[i] if self.green_line_sugg_speed[i] != None else "None"))
                                                self.DataTable.setItem(i, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[i] if self.green_line_cmd_speed[i] != None else "None"))

                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block speed data
                                        for i in range(1, 36):

                                                self.DataTable.setItem(i-1, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-1, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[i] if self.green_line_sugg_speed[i] != None else "None"))
                                                self.DataTable.setItem(i-1, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[i] if self.green_line_cmd_speed[i] != None else "None"))

                                        # Set Block 150 speed data
                                        self.DataTable.setItem(35, 0, QtWidgets.QTableWidgetItem(f"{150}"))
                                        self.DataTable.setItem(35, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[150] if self.green_line_sugg_speed[150] != None else "None"))
                                        self.DataTable.setItem(35, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[150] if self.green_line_cmd_speed[150] != None else "None"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        # Set Table Size
                                        self.DataTable.setRowCount(90)

                                        # Fill Table with block speed data

                                        # Set Yard Block speed data
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[0] if self.green_line_sugg_speed[0] != None else "None"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[0] if self.green_line_cmd_speed[0] != None else "None"))


                                        # Sections H --> M
                                        for i in range(33, 77):

                                                self.DataTable.setItem(i-32, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-32, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[i] if self.green_line_sugg_speed[i] != None else "None"))
                                                self.DataTable.setItem(i-32, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[i] if self.green_line_cmd_speed[i] != None else "None"))

                                        # Sections T --> Z
                                        for i in range(105, 151):

                                                self.DataTable.setItem(i-60, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-60, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[i] if self.green_line_sugg_speed[i] != None else "None"))
                                                self.DataTable.setItem(i-60, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[i] if self.green_line_cmd_speed[i] != None else "None"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block speed data
                                        for i in range(74, 110):

                                                self.DataTable.setItem(i-74, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-74, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_speed[i] if self.green_line_sugg_speed[i] != None else "None"))
                                                self.DataTable.setItem(i-74, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_speed[i] if self.green_line_cmd_speed[i] != None else "None"))

                        # Authority Filter
                        elif self.selected_filter == 2:

                                # Set Table Column Headers
                                self.DataTable.setHorizontalHeaderLabels(["Block", "Sugg. Authority", "Cmd. Authority"])

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:

                                        # Set Table Size
                                        self.DataTable.setRowCount(150)

                                        # Set Yard Block speed data
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[0] if self.green_line_sugg_auth[0] != None else "None"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[0] if self.green_line_cmd_auth[0] != None else "None"))

                                        # Fill Table with rest of block speed data
                                        for i in range(1, 151):

                                                self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[i] if self.green_line_sugg_auth[i] != None else "None"))
                                                self.DataTable.setItem(i, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[i] if self.green_line_cmd_auth[i] != None else "None"))

                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block speed data
                                        for i in range(1, 36):

                                                self.DataTable.setItem(i-1, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-1, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[i] if self.green_line_sugg_auth[i] != None else "None"))
                                                self.DataTable.setItem(i-1, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[i] if self.green_line_cmd_auth[i] != None else "None"))

                                        # Set Block 150 speed data
                                        self.DataTable.setItem(35, 0, QtWidgets.QTableWidgetItem(f"{150}"))
                                        self.DataTable.setItem(35, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[150] if self.green_line_sugg_auth[150] != None else "None"))
                                        self.DataTable.setItem(35, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[150] if self.green_line_cmd_auth[150] != None else "None"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        # Set Table Size
                                        self.DataTable.setRowCount(90)

                                        # Fill Table with block speed data
                                        
                                        # Set Yard Block speed data
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[0] if self.green_line_sugg_auth[0] != None else "None"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[0] if self.green_line_cmd_auth[0] != None else "None"))

                                        # Sections H --> M
                                        for i in range(33, 77):

                                                self.DataTable.setItem(i-32, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-32, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[i] if self.green_line_sugg_auth[i] != None else "None"))
                                                self.DataTable.setItem(i-32, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[i] if self.green_line_cmd_auth[i] != None else "None"))

                                        # Sections T --> Z
                                        for i in range(105, 151):

                                                self.DataTable.setItem(i-60, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-60, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[i] if self.green_line_sugg_auth[i] != None else "None"))
                                                self.DataTable.setItem(i-60, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[i] if self.green_line_cmd_auth[i] != None else "None"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block speed data
                                        for i in range(74, 110):

                                                self.DataTable.setItem(i-74, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-74, 1, QtWidgets.QTableWidgetItem(self.green_line_sugg_auth[i] if self.green_line_sugg_auth[i] != None else "None"))
                                                self.DataTable.setItem(i-74, 2, QtWidgets.QTableWidgetItem(self.green_line_cmd_auth[i] if self.green_line_cmd_auth[i] != None else "None"))
                                
                        # Switches Filter
                        elif self.selected_filter == 3:

                                # Set Table Colhmn Headers
                                self.DataTable.setHorizontalHeaderLabels(["Section", "Switch Cmd", ""])

                                # Set Table Size
                                self.DataTable.setRowCount(default_row_count)

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:
                                        
                                        # Fill Table with switch commands
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("D"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("D <-- A" if self.green_line_sw_cmd[0] else "D --> C"))
                                
                                        self.DataTable.setItem(1, 0, QtWidgets.QTableWidgetItem("F"))
                                        self.DataTable.setItem(1, 1, QtWidgets.QTableWidgetItem("F <-- Z" if self.green_line_sw_cmd[1] else "F --> G"))
                                
                                        self.DataTable.setItem(2, 0, QtWidgets.QTableWidgetItem("I"))
                                        self.DataTable.setItem(2, 1, QtWidgets.QTableWidgetItem("I --> J" if self.green_line_sw_cmd[2] else "I --> Yard"))
                                
                                        self.DataTable.setItem(3, 0, QtWidgets.QTableWidgetItem("K"))
                                        self.DataTable.setItem(3, 1, QtWidgets.QTableWidgetItem("K <-- Yard" if self.green_line_sw_cmd[3] else "K <-- J"))
                                
                                        self.DataTable.setItem(4, 0, QtWidgets.QTableWidgetItem("N1"))
                                        self.DataTable.setItem(4, 1, QtWidgets.QTableWidgetItem("N1 <-- M" if self.green_line_sw_cmd[4] else "N1 --> R"))
                                
                                        self.DataTable.setItem(5, 0, QtWidgets.QTableWidgetItem("N2"))
                                        self.DataTable.setItem(5, 1, QtWidgets.QTableWidgetItem("N2 <-- Q" if self.green_line_sw_cmd[5] else "N2 --> O"))

                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        # Fill Table with switch commands
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("D"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("D <-- A" if self.green_line_sw_cmd[0] else "D --> C"))
                                
                                        self.DataTable.setItem(1, 0, QtWidgets.QTableWidgetItem("F"))
                                        self.DataTable.setItem(1, 1, QtWidgets.QTableWidgetItem("F <-- Z" if self.green_line_sw_cmd[1] else "F --> G"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        # Fill Table with switch commands
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("I"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("I --> J" if self.green_line_sw_cmd[2] else "I --> Yard"))
                                
                                        self.DataTable.setItem(1, 0, QtWidgets.QTableWidgetItem("K"))
                                        self.DataTable.setItem(1, 1, QtWidgets.QTableWidgetItem("K <-- Yard" if self.green_line_sw_cmd[3] else "K <-- J"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        # Fill Table with switch commands
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("N1"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("N1 <-- M" if self.green_line_sw_cmd[4] else "N1 --> R"))
                                
                                        self.DataTable.setItem(1, 0, QtWidgets.QTableWidgetItem("N2"))
                                        self.DataTable.setItem(1, 1, QtWidgets.QTableWidgetItem("N2 <-- Q" if self.green_line_sw_cmd[5] else "N2 --> O"))

                        # Signals Filter
                        elif self.selected_filter == 4:

                                # Set Table Column Headers
                                self.DataTable.setHorizontalHeaderLabels(["Section", "Signal Cmd", ""])

                                # Set Table Size
                                self.DataTable.setRowCount(default_row_count)

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:

                                        # Fill Table with block speed data
                                        for i in range(11):

                                                if i == 0:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("C"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 1:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("D"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 2:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("F"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 3:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("G"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 4:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("J"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 5:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("K"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 6:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("N1"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 7:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("N2"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 8:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("O"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 9:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("R"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 10:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("Yard"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                
                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        # Fill Table with block speed data
                                        for i in range(4):

                                                if i == 0:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("C"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 1:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("D"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 2:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("F"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))
                                                elif i == 3:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("G"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[i] else "Green"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        # Fill Table with block speed data
                                        for i in range(3):

                                                if i == 0:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("J"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[4] else "Green"))
                                                elif i == 1:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("K"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[5] else "Green"))
                                                elif i == 2:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("Yard"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[10] else "Green"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        # Fill Table with block speed data
                                        for i in range(4):

                                                if i == 0:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("N1"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[6] else "Green"))
                                                elif i == 1:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("N2"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[7] else "Green"))
                                                elif i == 2:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("O"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[8] else "Green"))
                                                elif i == 3:
                                                        self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem("R"))
                                                        self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Red" if self.green_line_sig_cmd[9] else "Green"))
                                        
                        # Occupancy Filter
                        elif self.selected_filter == 5:

                                # Set Table Column Headers
                                self.DataTable.setHorizontalHeaderLabels(["Block", "Status", ""])

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:

                                        # Set Table Size
                                        self.DataTable.setRowCount(150)

                                        # Set Yard Block occupancy
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[0] else "Unoccupied"))

                                        # Fill Table with rest of block occupancies
                                        for i in range(1, 151):

                                                self.DataTable.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[i] else "Unoccupied"))

                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block occupancies
                                        for i in range(1, 36):

                                                self.DataTable.setItem(i-1, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-1, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[i] else "Unoccupied"))

                                        # Set Block 150 occupancy
                                        self.DataTable.setItem(35, 0, QtWidgets.QTableWidgetItem(f"{150}"))
                                        self.DataTable.setItem(35, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[150] else "Unoccupied"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        # Set Table Size
                                        self.DataTable.setRowCount(90)

                                        # Fill Table with block occupancies

                                        # Yard
                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Yard"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[0] else "Unoccupied"))

                                        # Sections H --> M
                                        for i in range(33, 77):

                                                self.DataTable.setItem(i-32, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-32, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[i] else "Unoccupied"))

                                        # Sections T --> Z
                                        for i in range(105, 151):

                                                self.DataTable.setItem(i-60, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-60, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[i] else "Unoccupied"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        # Set Table Size
                                        self.DataTable.setRowCount(36)

                                        # Fill Table with block occupancies
                                        for i in range(74, 110):

                                                self.DataTable.setItem(i-74, 0, QtWidgets.QTableWidgetItem(f"{i}"))
                                                self.DataTable.setItem(i-74, 1, QtWidgets.QTableWidgetItem("Occupied" if self.green_line_block_occupancy[i] else "Unoccupied"))

                        # Crossings Filter
                        elif self.selected_filter == 6:

                                # Set Table Column Headers
                                self.DataTable.setHorizontalHeaderLabels(["Section", "Block", "Status"])

                                # Set Table Size
                                self.DataTable.setRowCount(default_row_count)

                                # Fill Table with crossing statuses

                                # No Wayside selected, show entire line
                                if self.WaysideSelectComboBox.currentIndex() == 0:

                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("E"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{19}"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem("Closed" if self.green_line_cross_cmd[0] else "Open"))

                                        self.DataTable.setItem(1, 0, QtWidgets.QTableWidgetItem("T"))
                                        self.DataTable.setItem(1, 1, QtWidgets.QTableWidgetItem(f"{108}"))
                                        self.DataTable.setItem(1, 2, QtWidgets.QTableWidgetItem("Closed" if self.green_line_cross_cmd[1] else "Open"))
                                
                                # Wayside 1 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 1:

                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("E"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{19}"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem("Closed" if self.green_line_cross_cmd[0] else "Open"))

                                # Wayside 2 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 2:

                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("T"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{108}"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem("Closed" if self.green_line_cross_cmd[1] else "Open"))

                                # Wayside 3 selected
                                elif self.WaysideSelectComboBox.currentIndex() == 3:

                                        self.DataTable.setItem(0, 0, QtWidgets.QTableWidgetItem("None"))
                                        self.DataTable.setItem(0, 1, QtWidgets.QTableWidgetItem("None"))
                                        self.DataTable.setItem(0, 2, QtWidgets.QTableWidgetItem("None"))

                # Not Green Line
                else:
                        self.DataTable.setRowCount(default_row_count)
                        self.DataTable.setHorizontalHeaderLabels(["", "", ""])

        # Filter button clicked
        def filter_button_clicked(self, filter):
                self.update_filter_button(filter)
                self.update_table()


        ####################
        #  Update Log
        ####################

        # Variables
        log_entries = []
        past_sugg_speed = [None] * 151
        past_sugg_authority = [None] * 151
        past_sw_cmd = [None] * 6
        past_sig_cmd = [None] * 11
        past_cross_cmd = [None] * 2

        # Update Log
        def update_log_array(self):
                
                # Variables
                new_sugg_speed_entry = ''
                new_sugg_auth_entry = ''
                new_sw_cmd_entry = ''
                new_sig_cmd_entry = ''
                new_cross_cmd_entry = ''

                # Traverse through sugg speeds
                for i in range(self.green_line_sugg_speed):

                        # Check if new speed is different from past speed
                        if self.green_line_sugg_speed[i] != self.past_sugg_speed[i] and self.green_line_sugg_speed != None:
                                new_sugg_speed_entry == f"Block {i} suggested speed: {self.green_line_sugg_speed[i]} Km/Hr\n"

                                # Check if sugg speed is passed on as cmd speed
                                if self.green_line_cmd_speed[i] == self.green_line_sugg_speed[i]:
                                        new_sugg_speed_entry += "Suggested speed approved"
                                else:
                                        new_sugg_speed_entry += "Suggested speed rejected"

                                # Add entry to log
                                self.log_entries.append(new_sugg_speed_entry)

                # Traverse through sugg authorities
                for i in range(self.green_line_sugg_auth):

                        # Check if new authority is different from past authority
                        if self.green_line_sugg_auth[i] != self.past_sugg_authority[i] and self.green_line_sugg_auth != None:
                                new_sugg_auth_entry == f"Block {i} suggested authority: {self.green_line_sugg_auth[i]} blocks\n"

                                # Check if sugg authority is passed on as cmd authority
                                if self.green_line_cmd_auth[i] == self.green_line_sugg_auth[i]:
                                        new_sugg_auth_entry += "Suggested authority approved"
                                else:
                                        new_sugg_auth_entry += "Suggested authority rejected"

                                # Add entry to log
                                self.log_entries.append(new_sugg_auth_entry)

                # Traverse through switch commands
                for i in range(self.green_line_sw_cmd):

                        # Check if new switch command is different from past switch command
                        if self.green_line_sw_cmd[i] != self.past_sw_cmd[i]:

                                # Check which switch changed
                                
                                # Switch D
                                if i == 0:
                                        new_sw_cmd_entry == f"Switch D: {"D <-- A" if self.green_line_sw_cmd[i] else "D --> C"}"

                                # Switch F
                                elif i == 1:
                                        new_sw_cmd_entry == f"Switch F: {"F <-- Z" if self.green_line_sw_cmd[i] else "F --> G"}"

                                # Switch I
                                elif i == 2:
                                        new_sw_cmd_entry == f"Switch I: {"I --> J" if self.green_line_sw_cmd[i] else "I --> Yard"}"

                                # Switch K
                                elif i == 3:
                                        new_sw_cmd_entry == f"Switch K: {"K <-- Yard" if self.green_line_sw_cmd[i] else "K <-- J"}"

                                # Switch N1
                                elif i == 4:
                                        new_sw_cmd_entry == f"Switch N1: {"N1 <-- M" if self.green_line_sw_cmd[i] else "N1 --> R"}"

                                # Switch N2
                                elif i == 5:
                                        new_sw_cmd_entry == f"Switch N2: {"N2 <-- Q" if self.green_line_sw_cmd[i] else "N2 --> O"}"

                                # Add entry to log
                                self.log_entries.append(new_sw_cmd_entry)

                # Traverse through signal commands
                for i in range(self.green_line_sig_cmd):

                        # Check if new signal command is different from past signal command
                        if self.green_line_sig_cmd[i] != self.past_sig_cmd[i]:

                                # Check which signal changed
                                
                                # Signal C
                                if i == 0:
                                        new_sig_cmd_entry == f"Signal C: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal D
                                elif i == 1:
                                        new_sig_cmd_entry == f"Signal D: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal F
                                elif i == 2:
                                        new_sig_cmd_entry == f"Signal F: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal G
                                elif i == 3:
                                        new_sig_cmd_entry == f"Signal G: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal J
                                elif i == 4:
                                        new_sig_cmd_entry == f"Signal J: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal K
                                elif i == 5:
                                        new_sig_cmd_entry == f"Signal K: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal N1
                                elif i == 6:
                                        new_sig_cmd_entry == f"Signal N1: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal N2
                                elif i == 7:
                                        new_sig_cmd_entry == f"Signal N2: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal O
                                elif i == 8:
                                        new_sig_cmd_entry == f"Signal O: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal R
                                elif i == 9:
                                        new_sig_cmd_entry == f"Signal R: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Signal Yard
                                elif i == 10:
                                        new_sig_cmd_entry == f"Signal Yard: {"Red" if self.green_line_sig_cmd[i] else "Green"}"

                                # Add entry to log
                                self.log_entries.append(new_sig_cmd_entry)

                # Traverse through crossing commands
                for i in range(self.green_line_cross_cmd):

                        # Check if new crossing command is different from past crossing command
                        if self.green_line_cross_cmd[i] != self.past_cross_cmd[i]:

                                # Check which crossing changed
                                
                                # Crossing E
                                if i == 0:
                                        new_cross_cmd_entry == f"Crossing E: {"Closed" if self.green_line_cross_cmd[i] else "Open"}"

                                # Crossing T
                                elif i == 1:
                                        new_cross_cmd_entry == f"Crossing T: {"Closed" if self.green_line_cross_cmd[i] else "Open"}"

                                # Add entry to log
                                self.log_entries.append(new_cross_cmd_entry)


        # Add log entry to Update Log
        def update_log_entries(self):

                # Clear log table
                self.UpdateLog.clear()

                # Add log entries to log table
                for entry in reversed(self.log_entries):
                        self.UpdateLog.addItem(entry)
                
                


        ###################################
        #       Upload PLC Program
        ###################################

        # Open file manager to select PLC programs
        def open_file_dialog(self):

                # Open a file dialog to select Python files
                file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open Python files', '', 'Python Files (*.py)')

                # Run PLC programs in separate processes
                self.execute_files(file_paths)
    
        # Execute the selected Python files
        def execute_files(self, file_paths):

                # Start each file in a separate process
                for file_path in file_paths:

                        # Start subprocess
                        process = subprocess.Popen(['python', file_path])

                        # Add the process to the list of running processes
                        self.processes.append(process)
                        print(f"Running {file_path}")

        

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
"""