# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module: Wayside Controller (Software)
# PyQt Version: 6.7.1
#
# Last Update: 10/11/2024
# Last Updated by: Zachary McPherson
#
# Notes: Functionality is not yet refined but organization is complete.


#######################################################################################################################
#
#                                                      Libraries
#
#######################################################################################################################

import sys
from PyQt6 import QtCore, QtGui, QtWidgets


#######################################################################################################################
#
#                                                      Classes
#
#######################################################################################################################

# Main UI Class
class Ui_MainWindow(object):


        #######################################################################################################################
        #
        #
        #                                                   QT Designer Translation
        #
        #
        #######################################################################################################################

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
                self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1401, 161))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.ControllerHeader_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.ControllerHeader_layout.setContentsMargins(0, 0, 0, 0)
                self.ControllerHeader_layout.setObjectName("ControllerHeader_layout")
                self.ControllerHeader = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
                self.ControllerHeader.setStyleSheet("background-color: rgb(43, 120, 228);\n"
                "font: 36pt \"Times New Roman\";\n"
                "color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.ControllerHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ControllerHeader.setIndent(0)
                self.ControllerHeader.setObjectName("ControllerHeader")
                self.ControllerHeader_layout.addWidget(self.ControllerHeader)
                self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.Controller)
                self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(400, 160, 601, 831))
                self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
                self.dataTable_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
                self.dataTable_layout.setContentsMargins(0, 0, 0, 0)
                self.dataTable_layout.setObjectName("dataTable_layout")
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
                self.dataTable_layout.addWidget(self.DataTable)
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
                self.tabWidget.addTab(self.Controller, "")
                self.PLCUpload = QtWidgets.QWidget()
                self.PLCUpload.setObjectName("PLCUpload")
                self.verticalLayoutWidget_7 = QtWidgets.QWidget(parent=self.PLCUpload)
                self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(0, 0, 1401, 161))
                self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
                self.PLCHeader_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
                self.PLCHeader_layout.setContentsMargins(0, 0, 0, 0)
                self.PLCHeader_layout.setObjectName("PLCHeader_layout")
                self.PLCHeader = QtWidgets.QLabel(parent=self.verticalLayoutWidget_7)
                self.PLCHeader.setStyleSheet("background-color: rgb(43, 120, 228);\n"
                "font: 36pt \"Times New Roman\";\n"
                "color: rgb(255, 255, 255);\n"
                "border: 2px solid black;\n"
                "font-weight: bold;")
                self.PLCHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.PLCHeader.setIndent(0)
                self.PLCHeader.setObjectName("PLCHeader")
                self.PLCHeader_layout.addWidget(self.PLCHeader)
                self.frame = QtWidgets.QFrame(parent=self.PLCUpload)
                self.frame.setGeometry(QtCore.QRect(370, 290, 721, 521))
                self.frame.setStyleSheet("border: 5px dashed rgb(159, 197, 248);")
                self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
                self.frame.setObjectName("frame")
                self.LoadSelectedFileButton = QtWidgets.QPushButton(parent=self.frame)
                self.LoadSelectedFileButton.setGeometry(QtCore.QRect(390, 370, 251, 51))
                self.LoadSelectedFileButton.setStyleSheet("border: 2px solid;\n"
                "color: rgb(255, 255, 255);\n"
                "border-color: rgb(0, 170, 255);\n"
                "background-color: rgb(0, 170, 255);\n"
                "border-radius: 20px;\n"
                "font: 75 15pt \"Times New Roman\";")
                self.LoadSelectedFileButton.setIconSize(QtCore.QSize(20, 20))
                self.LoadSelectedFileButton.setFlat(True)
                self.LoadSelectedFileButton.setObjectName("LoadSelectedFileButton")
                self.LoadedFile = QtWidgets.QLineEdit(parent=self.frame)
                self.LoadedFile.setGeometry(QtCore.QRect(290, 90, 351, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                self.LoadedFile.setFont(font)
                self.LoadedFile.setStyleSheet("border: none;")
                self.LoadedFile.setReadOnly(True)
                self.LoadedFile.setObjectName("LoadedFile")
                self.LoadedFileLabel = QtWidgets.QLabel(parent=self.frame)
                self.LoadedFileLabel.setGeometry(QtCore.QRect(110, 90, 161, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.LoadedFileLabel.setFont(font)
                self.LoadedFileLabel.setStyleSheet("border: none;")
                self.LoadedFileLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.LoadedFileLabel.setObjectName("LoadedFileLabel")
                self.selectedFile = QtWidgets.QLineEdit(parent=self.frame)
                self.selectedFile.setGeometry(QtCore.QRect(290, 240, 351, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                self.selectedFile.setFont(font)
                self.selectedFile.setStyleSheet("border: none;")
                self.selectedFile.setReadOnly(True)
                self.selectedFile.setObjectName("selectedFile")
                self.SelectedFileLabel = QtWidgets.QLabel(parent=self.frame)
                self.SelectedFileLabel.setGeometry(QtCore.QRect(110, 240, 161, 41))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.SelectedFileLabel.setFont(font)
                self.SelectedFileLabel.setStyleSheet("border: none;")
                self.SelectedFileLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.SelectedFileLabel.setObjectName("SelectedFileLabel")
                self.SelectNewFileButton = QtWidgets.QPushButton(parent=self.frame)
                self.SelectNewFileButton.setGeometry(QtCore.QRect(80, 370, 251, 51))
                self.SelectNewFileButton.setStyleSheet("border: 2px solid;\n"
                "color: rgb(255, 255, 255);\n"
                "border-color: rgb(0, 170, 255);\n"
                "background-color: rgb(0, 170, 255);\n"
                "border-radius: 20px;\n"
                "font: 75 15pt \"Times New Roman\";")
                self.SelectNewFileButton.setIconSize(QtCore.QSize(20, 20))
                self.SelectNewFileButton.setFlat(True)
                self.SelectNewFileButton.setObjectName("SelectNewFileButton")
                self.tabWidget.addTab(self.PLCUpload, "")
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
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
                self.ControllerHeader.setText(_translate("MainWindow", "Wayside Controller"))
                self.DataTable.setSortingEnabled(False)
                __sortingEnabled = self.DataTable.isSortingEnabled()
                self.DataTable.setSortingEnabled(False)
                self.DataTable.setSortingEnabled(__sortingEnabled)
                self.UpdateHeader.setText(_translate("MainWindow", "Updates"))
                item = self.UpdateLog.horizontalHeaderItem(0)
                item.setText(_translate("MainWindow", "UpdateLog"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.Controller), _translate("MainWindow", "Controller"))
                self.PLCHeader.setText(_translate("MainWindow", "Upload PLC Program"))
                self.LoadSelectedFileButton.setText(_translate("MainWindow", "Load Selected File"))
                self.LoadedFile.setText(_translate("MainWindow", "None"))
                self.LoadedFileLabel.setText(_translate("MainWindow", "Loaded File:"))
                self.selectedFile.setText(_translate("MainWindow", "None"))
                self.SelectedFileLabel.setText(_translate("MainWindow", "Selected File:"))
                self.SelectNewFileButton.setText(_translate("MainWindow", "Select New File"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.PLCUpload), _translate("MainWindow", "PLC Upload"))
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


        #######################################################################################################################
        #
        #
        #                                                       Test Bench Setup
        #
        #
        #######################################################################################################################

        ##########################################
        #       Selection Comboboxes
        ##########################################

        # CTC, TRK Input
        def testBenchSelectionOptions(self):
                self.CTCInputSelection.addItems(["", "Switch", "Speed", "Authority"])
                self.TRKInputSelection.addItems(["", "Occupancy", "Switch", "Signal", "Crossing"])


        ##########################################
        #       Enable / Disable Combo Boxes
        ##########################################
        
        # CTC Input
        def testBenchCTCInputEnableDisable(self):
                if self.CTCInputSelection.currentIndex() == 0:
                        self.CTCInputBlockIndex.setEnabled(True)
                        self.CTCInputSuggSW.setEnabled(True)
                        self.CTCInputSuggSpeed.setEnabled(True)
                        self.CTCInputSuggAuth.setEnabled(True)
                elif self.CTCInputSelection.currentIndex() == 1:
                        self.CTCInputBlockIndex.setDisabled(True)
                        self.CTCInputBlockIndex.setCurrentIndex(0)
                        self.CTCInputSuggSW.setEnabled(True)
                        self.CTCInputSuggSpeed.setDisabled(True)
                        self.CTCInputSuggSpeed.clear()
                        self.CTCInputSuggAuth.setDisabled(True)
                        self.CTCInputSuggAuth.clear()
                elif self.CTCInputSelection.currentIndex() == 2:
                        self.CTCInputBlockIndex.setEnabled(True)
                        self.CTCInputSuggSW.setDisabled(True)
                        self.CTCInputSuggSW.setCurrentIndex(0)
                        self.CTCInputSuggSpeed.setEnabled(True)
                        self.CTCInputSuggAuth.setDisabled(True)
                        self.CTCInputSuggAuth.clear()
                elif self.CTCInputSelection.currentIndex() == 3:
                        self.CTCInputBlockIndex.setEnabled(True)
                        self.CTCInputSuggSW.setDisabled(True)
                        self.CTCInputSuggSW.setCurrentIndex(0)
                        self.CTCInputSuggSpeed.setDisabled(True)
                        self.CTCInputSuggSpeed.clear()
                        self.CTCInputSuggAuth.setEnabled(True)

        
        # TRK Input
        def testBenchTRKInputEnableDisable(self):
                if self.TRKInputSelection.currentIndex() == 0:
                        self.TRKInputBlockIndex.setEnabled(True)
                        self.TRKInputOcc.setEnabled(True)
                        self.TRKInputSWStatus.setEnabled(True)
                        self.TRKInputSigStatus.setEnabled(True)
                        self.TRKInputCrossStatus.setEnabled(True)
                elif self.TRKInputSelection.currentIndex() == 1:
                        self.TRKInputBlockIndex.setEnabled(True)
                        self.TRKInputOcc.setEnabled(True)
                        self.TRKInputSWStatus.setEnabled(False)
                        self.TRKInputSWStatus.setCurrentIndex(0)
                        self.TRKInputSigStatus.setEnabled(False)
                        self.TRKInputSigStatus.setCurrentIndex(0)
                        self.TRKInputCrossStatus.setEnabled(False)
                        self.TRKInputCrossStatus.setCurrentIndex(0)
                elif self.TRKInputSelection.currentIndex() == 2:
                        self.TRKInputBlockIndex.setEnabled(False)
                        self.TRKInputBlockIndex.setCurrentIndex(0)
                        self.TRKInputOcc.setEnabled(False)
                        self.TRKInputOcc.setCurrentIndex(0)
                        self.TRKInputSWStatus.setEnabled(True)
                        self.TRKInputSigStatus.setEnabled(False)
                        self.TRKInputSigStatus.setCurrentIndex(0)
                        self.TRKInputCrossStatus.setEnabled(False)
                        self.TRKInputCrossStatus.setCurrentIndex(0)
                elif self.TRKInputSelection.currentIndex() == 3:
                        self.TRKInputBlockIndex.setEnabled(True)
                        self.TRKInputOcc.setEnabled(False)
                        self.TRKInputOcc.setCurrentIndex(0)
                        self.TRKInputSWStatus.setEnabled(False)
                        self.TRKInputSWStatus.setCurrentIndex(0)
                        self.TRKInputSigStatus.setEnabled(True)
                        self.TRKInputCrossStatus.setEnabled(False)
                        self.TRKInputCrossStatus.setCurrentIndex(0)
                elif self.TRKInputSelection.currentIndex() == 4:
                        self.TRKInputBlockIndex.setEnabled(True)
                        self.TRKInputOcc.setEnabled(False)
                        self.TRKInputOcc.setCurrentIndex(0)
                        self.TRKInputSWStatus.setEnabled(False)
                        self.TRKInputSWStatus.setCurrentIndex(0)
                        self.TRKInputSigStatus.setEnabled(False)
                        self.TRKInputSigStatus.setCurrentIndex(0)
                        self.TRKInputCrossStatus.setEnabled(True)


        ##########################################
        #       Section Index Comboboxes
        ##########################################

        # CTC, TRK Input Output
        def testBenchSetSectionIndexOptions(self):
                self.CTCInputSecIndex.addItems(["", "A", "B", "C"])
                self.TRKInputSecIndex.addItems(["", "A", "B", "C"])
                self.CTCOutputSecIndex.addItems(["", "A", "B", "C"])
                self.TRKOutputSecIndex.addItems(["", "A", "B", "C"])


        ##########################################
        #       Block Index Comboboxes
        ##########################################
        
        # CTC Input
        def testBenchCTCInputSetBlockIndexOptions(self):
                self.CTCInputBlockIndex.clear()
                if self.CTCInputSecIndex.currentIndex() == 1:
                        self.CTCInputBlockIndex.addItems(["", "1", "2", "3", "4", "5"])
                elif self.CTCInputSecIndex.currentIndex() == 2:
                        self.CTCInputBlockIndex.addItems(["", "6", "7", "8", "9", "10", "11"])
                elif self.CTCInputSecIndex.currentIndex() == 3:
                        self.CTCInputBlockIndex.addItems(["", "12", "13", "14", "15", "16"])

        # TRK Input
        def testBenchTRKInputSetBlockIndexOptions(self):
                self.TRKInputBlockIndex.clear()
                if self.TRKInputSecIndex.currentIndex() == 1:
                        self.TRKInputBlockIndex.addItems(["", "1", "2", "3", "4", "5"])
                elif self.TRKInputSecIndex.currentIndex() == 2:
                        self.TRKInputBlockIndex.addItems(["", "6", "7", "8", "9", "10", "11"])
                elif self.TRKInputSecIndex.currentIndex() == 3:
                        self.TRKInputBlockIndex.addItems(["", "12", "13", "14", "15", "16"])

        # CTC Output
        def testBenchCTCOutputSetBlockIndexOptions(self):
                self.CTCOutputBlockIndex.clear()
                if self.CTCOutputSecIndex.currentIndex() == 1:
                        self.CTCOutputBlockIndex.addItems(["", "1", "2", "3", "4", "5"])
                elif self.CTCOutputSecIndex.currentIndex() == 2:
                        self.CTCOutputBlockIndex.addItems(["", "6", "7", "8", "9", "10", "11"])
                elif self.CTCOutputSecIndex.currentIndex() == 3:
                        self.CTCOutputBlockIndex.addItems(["", "12", "13", "14", "15", "16"])

        # TRK Output
        def testBenchTRKOutputSetBlockIndexOptions(self):
                self.TRKOutputBlockIndex.clear()
                if self.TRKOutputSecIndex.currentIndex() == 1:
                        self.TRKOutputBlockIndex.addItems(["", "1", "2", "3", "4", "5"])
                elif self.TRKOutputSecIndex.currentIndex() == 2:
                        self.TRKOutputBlockIndex.addItems(["", "6", "7", "8", "9", "10", "11"])
                elif self.TRKOutputSecIndex.currentIndex() == 3:
                        self.TRKOutputBlockIndex.addItems(["", "12", "13", "14", "15", "16"])

        
        ##########################################
        #       Switch Comboboxes
        ##########################################

        # CTC Input
        def testBenchCTCInputSetSuggSwitchOptions(self):
                if self.CTCInputSecIndex.currentIndex() == 1:
                        self.CTCInputSuggSW.addItems(['', '0', '1'])
                else:
                        self.CTCInputSuggSW.clear()

        # TRK Input
        def testBenchTRKInputSetSWStatusOptions(self):
                if self.TRKInputSecIndex.count() != 0 and self.TRKInputSWStatus.count() == 0:
                        self.TRKInputSWStatus.addItems(['', '0', '1'])
                elif self.TRKInputSWStatus.count() != 0:
                        pass
                else:
                        self.TRKInputSWStatus.clear()

        # CTC Output
        def testBenchCTCOutputSetSWStatus(self):
                SecIndex = self.CTCOutputSecIndex.currentIndex()-1
                BlockIndex = self.CTCOutputBlockIndex.currentIndex()-1

                if (SecIndex != -1) and (BlockIndex != -1):
                        if SecIndex == 0 and BlockIndex == 4:
                                self.CTCOutputSWStatus.setText(str(self.Sec[SecIndex][6][BlockIndex]))
                        else:
                                self.CTCOutputSWStatus.setText('N/A')

        # TRK Output
        def testBenchTRKOutputSetSWCmd(self):
                SecIndex = self.TRKOutputSecIndex.currentIndex()-1
                BlockIndex = self.TRKOutputBlockIndex.currentIndex()-1
                        
                if (SecIndex != -1) and (BlockIndex != -1):
                        if SecIndex == 0 and BlockIndex == 4:
                                self.TRKOutputSWCmd.setText(str(self.CmdSWCmd))
                        else:
                                self.TRKOutputSWCmd.setText('N/A')


        ##########################################
        #       Signal Comboboxes
        ##########################################

        # TRK Input
        def testBenchTRKInputSetSigStatusOptions(self):
                if self.TRKInputSecIndex.count() != 0 and self.TRKInputSigStatus.count() == 0:
                        self.TRKInputSigStatus.addItems(['', 'Green', 'Yellow', 'Red'])
                elif self.TRKInputSigStatus.count() != 0:
                        pass
                else:
                        self.TRKInputSigStatus.clear()

        # CTC Output
        def testBenchCTCOutputSetSigStatus(self):
                SecIndex = self.CTCOutputSecIndex.currentIndex()-1
                BlockIndex = self.CTCOutputBlockIndex.currentIndex()-1

                if (SecIndex != -1) and (BlockIndex != -1):
                        if (SecIndex == 1 and BlockIndex == 0) or (SecIndex == 2 and BlockIndex == 0):
                                self.CTCOutputSigStatus.setText(str(self.Sec[SecIndex][3][BlockIndex]) + str(self.Sec[SecIndex][4][BlockIndex]))
                        else:
                                self.CTCOutputSigStatus.setText('N/A')

        # TRK Output
        def testBenchTRKOutputSetSigCmd(self):
                SecIndex = self.TRKOutputSecIndex.currentIndex()-1
                BlockIndex = self.TRKOutputBlockIndex.currentIndex()-1
                        
                if (SecIndex != -1) and (BlockIndex != -1):
                        if (SecIndex == 1 and BlockIndex == 0) or (SecIndex == 2 and BlockIndex ==0):
                                if SecIndex == 1:
                                        self.TRKOutputSigCmd.setText(self.TRKOutputSecBSignalCmd)
                                elif SecIndex == 2:
                                        self.TRKOutputSigCmd.setText(self.TRKOutputSecCSignalCmd)
                        else:
                                self.TRKOutputSigCmd.setText('N/A')


        ##########################################
        #       Crossing Comboboxes
        ##########################################

        # TRK Input
        def testBenchTRKInputSetCrossStatusOptions(self):
                if self.TRKInputSecIndex.count() != 0 and self.TRKInputCrossStatus.count() == 0:
                        self.TRKInputCrossStatus.addItems(['', 'Open', 'Closed'])
                elif self.TRKInputCrossStatus.count() != 0:
                        pass
                else:
                        self.TRKInputCrossStatus.clear()


        # CTC Output
        def testBenchCTCOutputSetCrossStatus(self):
                SecIndex = self.CTCOutputSecIndex.currentIndex()-1
                BlockIndex = self.CTCOutputBlockIndex.currentIndex()-1

                if (SecIndex != -1) and (BlockIndex != -1):
                        if SecIndex == 0:
                                if BlockIndex == 2:
                                        self.CTCOutputCrossStatus.setText(str(self.Sec[SecIndex][2][BlockIndex]))
                                else:
                                        self.CTCOutputCrossStatus.setText('N/A')
                        else:
                                self.CTCOutputCrossStatus.setText('N/A')

        # TRK Output
        def testBenchTRKOutputSetCrossCmd(self):
                SecIndex = self.TRKOutputSecIndex.currentIndex()-1
                BlockIndex = self.TRKOutputBlockIndex.currentIndex()-1
                        
                if (SecIndex != -1) and (BlockIndex != -1):
                        if SecIndex == 0 and BlockIndex == 2:
                                self.TRKOutputCrossCmd.setText(self.TRKOutputCrossCmd)
                        else:
                                self.TRKOutputCrossCmd.setText('N/A')

        ##########################################
        #       Occupancy Comboboxes
        ##########################################

        # TRK Input
        def testBenchTRKInputSetOccupancyOptions(self):
                if self.TRKInputSecIndex.count() != 0 and self.TRKInputOcc.count() == 0:
                        
                        self.TRKInputOcc.addItems(['', 'Unoccupied', 'Occupied'])
                elif self.TRKInputOcc.count() != 0:
                        pass
                else:
                        self.TRKInputOcc.clear()

        # CTC Output
        def testBenchCTCOutputSetOccupancyStatus(self):
                SecIndex = self.CTCOutputSecIndex.currentIndex()-1
                BlockIndex = self.CTCOutputBlockIndex.currentIndex()-1

                if (SecIndex != -1) and (BlockIndex != -1):
                        self.CTCOutputOcc.setText(str(self.Sec[SecIndex][5][BlockIndex]))


        ##########################################
        #       Speed Comboboxes
        ##########################################

        # TRK Output
        def testBenchTRKOutputSetSpeedCmd(self):
                SecIndex = self.TRKOutputSecIndex.currentIndex()-1
                BlockIndex = self.TRKOutputBlockIndex.currentIndex()-1
                        
                if (SecIndex != -1) and (BlockIndex != -1):
                        if SecIndex == self.TRKOutputCmdSpeedSecIndex and BlockIndex == self.TRKOutputCmdSpeedBlockIndex:
                                self.TRKOutputCmdSpeed.setText(self.TRKOutputCmdSpeedValue)
                        else:
                                self.TRKOutputCmdSpeed.setText('N/A')


        ##########################################
        #       Authority Comboboxes
        ##########################################

        # TRK Output
        def testBenchTRKOutputSetAuthCmd(self):
                SecIndex = self.TRKOutputSecIndex.currentIndex()-1
                BlockIndex = self.TRKOutputBlockIndex.currentIndex()-1

                if SecIndex == self.TRKOutputCmdAuthSecIndex and BlockIndex == self.TRKOutputCmdAuthBlockIndex:
                        self.TRKOutputCmdAuth.setText(self.TRKOutputCmdAuthValue)
                else:
                        self.TRKOutputCmdAuth.setText('N/A')


        #######################################################################################################################
        #
        #
        #                                                       Test Bench Functions
        #
        #
        #######################################################################################################################

        ##########################################
        #       Retrieve Test Bench Inputs
        ##########################################

        # CTC Input
        def testBenchRetrieveCTCInput(self):

                # Suggested Switch Cmd
                if self.CTCInputSelection.currentIndex() == 1:
                        self.SecIndex = self.CTCInputSecIndex.currentIndex()-1
                        self.SuggSWCmd = self.CTCInputSuggSW.currentIndex()-1

                # Suggested Speed
                elif self.CTCInputSelection.currentIndex() == 2:
                        self.SecIndex = self.CTCInputSecIndex.currentIndex()-1
                        self.BlockIndex = self.CTCInputBlockIndex.currentIndex()-1
                        self.SuggSpeed = f"{int(self.CTCInputSuggSpeed.text()):07b}"

                # Suggested Authority
                elif self.CTCInputSelection.currentIndex() == 3:
                        self.SecIndex = self.CTCInputSecIndex.currentIndex()-1
                        self.BlockIndex = self.CTCInputBlockIndex.currentIndex()-1
                        self.SuggAuth = f"{int(self.CTCInputSuggAuth.text()):010b}"

        # TRK Input
        def testBenchRetrieveTRKInput(self):

                # Occupancy
                if self.TRKInputSelection.currentIndex() == 1:
                        self.SecIndex = self.TRKInputSecIndex.currentIndex()-1
                        self.BlockIndex = self.TRKInputBlockIndex.currentIndex()-1
                        self.Occ = self.TRKInputOcc.currentIndex()-1
                        
                # Switch Status
                elif self.TRKInputSelection.currentIndex() == 2:
                        self.SecIndex = self.TRKInputSecIndex.currentIndex()-1
                        self.SWStatus = self.TRKInputSWStatus.currentIndex()-1

                # Signal Status
                elif self.TRKInputSelection.currentIndex() == 3:
                        self.SecIndex = self.TRKInputSecIndex.currentIndex()-1
                        if self.TRKInputSigStatus.currentText() == 'Green':
                                self.SigStatus1 = 0
                                self.SigStatus0 = 1
                        elif self.TRKInputSigStatus.currentText() == 'Yellow':
                                self.SigStatus1 = 1
                                self.SigStatus0 = 0
                        elif self.TRKInputSigStatus.currentText() == 'Red':
                                self.SigStatus1 = 1
                                self.SigStatus0 = 1

                # Crossing Status
                elif self.TRKInputSelection.currentIndex() == 4:
                        self.SecIndex = self.TRKInputSecIndex.currentIndex()-1
                        self.CrossStatus = self.TRKInputCrossStatus.currentIndex()-1


        ##########################################
        #       Save Buttons
        ##########################################

        # CTC Input
        def testBenchSaveCTCInput(self):
                # Retrieve CTC Inputs
                self.testBenchRetrieveCTCInput()

                # Update properties

                # Switch Command
                if self.CTCInputSelection.currentIndex() == 1:
                        self.UpdateSwitchCmd()

                # Speed Command
                elif self.CTCInputSelection.currentIndex() == 2:
                        self.UpdateSpeedCmd()

                # Authority Command
                elif self.CTCInputSelection.currentIndex() == 3:
                        self.UpdateAuthCmd()

        # TRK Input
        def testBenchSaveTRKInput(self):
                # Retrieve TRK Inputs
                self.testBenchRetrieveTRKInput()

                # Update properties

                # Block and Section Occupancy
                if self.TRKInputSelection.currentIndex() == 1:
                        self.UpdateBlockOccupancies()

                # Switch Status
                elif self.TRKInputSelection.currentIndex() == 2:
                        self.UpdateSwitchStatus()

                # Signal Status
                elif self.TRKInputSelection.currentIndex() == 3:
                        self.UpdateSignalStatus()

                # Crossing Status
                elif self.TRKInputSelection.currentIndex() == 4:
                        self.UpdateCrossingStatus()


        ##########################################
        #       Reset Test Bench Inputs
        ##########################################

        # CTC Input
        def testBenchResetCTCInput(self):
                self.CTCInputSecIndex.setCurrentIndex(0)
                self.CTCInputBlockIndex.setCurrentIndex(0)
                self.CTCInputSuggSW.setCurrentIndex(0)
                self.CTCInputSuggSpeed.clear()
                self.CTCInputSuggAuth.clear()

        # TRK Input
        def testBenchResetTRKInput(self):
                self.TRKInputSecIndex.setCurrentIndex(0)
                self.TRKInputBlockIndex.setCurrentIndex(0)
                self.TRKInputOcc.setCurrentIndex(0)
                self.TRKInputSWStatus.setCurrentIndex(0)
                self.TRKInputSigStatus.setCurrentIndex(0)
                self.TRKInputCrossStatus.setCurrentIndex(0)


        #######################################################################################################################
        #
        #
        #                                                       Test Bench Signals
        #
        #
        #######################################################################################################################

        def TestBenchSignals(self):

        ##########################################
        #       Selection Comboboxes
        ##########################################

                # CTC, TRK Input
                self.testBenchSetSectionIndexOptions()


        ##########################################
        #       Enable / Disable Combo Boxes
        ##########################################

                # CTC Input
                self.CTCInputSelection.currentIndexChanged.connect(self.testBenchCTCInputEnableDisable)

                # TRK Input
                self.TRKInputSelection.currentIndexChanged.connect(self.testBenchTRKInputEnableDisable)


        ##########################################
        #       Block Index Comboboxes
        ##########################################

                # CTC Input
                self.CTCInputSecIndex.currentIndexChanged.connect(self.testBenchCTCInputSetBlockIndexOptions)

                # TRK Input
                self.TRKInputSecIndex.currentIndexChanged.connect(self.testBenchTRKInputSetBlockIndexOptions)

                # CTC Output
                self.CTCOutputSecIndex.currentIndexChanged.connect(self.testBenchCTCOutputSetBlockIndexOptions)

                # TRK Output
                self.TRKOutputSecIndex.currentIndexChanged.connect(self.testBenchTRKOutputSetBlockIndexOptions)


        ##########################################
        #       Switch Comboboxes
        ##########################################

                # CTC Input
                self.CTCInputSecIndex.currentIndexChanged.connect(self.testBenchCTCInputSetSuggSwitchOptions)

                # TRK Input
                self.TRKInputSecIndex.currentIndexChanged.connect(self.testBenchTRKInputSetSWStatusOptions)

                # CTC Output
                self.CTCOutputSecIndex.currentIndexChanged.connect(self.testBenchCTCOutputSetSWStatus)

                # TRK Output
                self.TRKOutputSecIndex.currentIndexChanged.connect(self.testBenchTRKOutputSetSWCmd)


        ##########################################
        #       Signal Comboboxes
        ##########################################

                # TRK Input
                self.TRKInputSecIndex.currentIndexChanged.connect(self.testBenchTRKInputSetSigStatusOptions)


        ##########################################
        #       Crossing Comboboxes
        ##########################################

                # TRK Input
                self.TRKInputSecIndex.currentIndexChanged.connect(self.testBenchTRKInputSetCrossStatusOptions)


        ##########################################
        #       Occupancy Comboboxes
        ##########################################

                # TRK Input
                self.TRKInputSecIndex.currentIndexChanged.connect(self.testBenchTRKInputSetOccupancyOptions)


        ##########################################
        #       Speed Comboboxes
        ##########################################

                # TRK Output
                self.TRKOutputBlockIndex.currentIndexChanged.connect(self.testBenchTRKOutputSetSpeedCmd)


        ##########################################
        #       Authority Comboboxes
        ##########################################

                # TRK Output
                self.TRKOutputBlockIndex.currentIndexChanged.connect(self.testBenchTRKOutputSetAuthCmd)


        ##########################################
        #       Save Buttons
        ##########################################
                
                # CTC Input
                self.CTCInputSaveButton.clicked.connect(self.testBenchRetrieveCTCInput)
                self.CTCInputSaveButton.clicked.connect(self.testBenchSaveCTCInput)
                self.CTCInputSaveButton.clicked.connect(self.testBenchResetCTCInput)

                # TRK Input
                self.TRKInputSaveButton.clicked.connect(self.testBenchRetrieveTRKInput)
                self.TRKInputSaveButton.clicked.connect(self.testBenchSaveTRKInput)
                self.TRKInputSaveButton.clicked.connect(self.testBenchResetTRKInput)


        #######################################################################################################################
        #
        #
        #                                                       Variables
        #
        #
        #######################################################################################################################

        ##########################################
        #       Track Layout
        ##########################################

        # Individual Sections

        # Block:   1,  2,  3,  4,  5
        A =     [[ 0,  0,  1,  0,  0 ],       # Has Crossing
                 [ 0,  0,  0,  0,  0 ],       # Has Signal
                 [ 0,  0,  0,  0,  0 ],       # Crossing Status
                 [ 0,  0,  0,  0,  0 ],       # Signal Status 1
                 [ 0,  0,  0,  0,  0 ],       # Signal Status 0
                 [ 0,  0,  0,  0,  0 ],       # Occupancy
                 [ 0,  0,  0,  0,  0 ],]      # Switch Status

        # Block:   6,  7,  8,  9, 10, 11
        B =     [[ 0,  0,  0,  0,  0,  0 ],   # Has Crossing
                 [ 1,  0,  0,  0,  0,  0 ],   # Has Signal
                 [ 0,  0,  0,  0,  0,  0 ],   # Crossing Status
                 [ 0,  0,  0,  0,  0,  0 ],   # Signal Status 1
                 [ 1,  0,  0,  0,  0,  0 ],   # Signal Status 0
                 [ 0,  0,  0,  0,  0,  0 ],   # Occupancy
                 [ 0,  0,  0,  0,  0,  0 ],]  # Switch Status

        # Block:  12, 13, 14, 15, 16
        C =     [[ 0,  0,  0,  0,  0 ],       # Has Crossing
                 [ 1,  0,  0,  0,  0 ],       # Has Signal
                 [ 0,  0,  0,  0,  0 ],       # Crossing Status
                 [ 0,  0,  0,  0,  0 ],       # Signal Status 1
                 [ 1,  0,  0,  0,  0 ],       # Signal Status 0
                 [ 0,  0,  0,  0,  0 ],       # Occupancy
                 [ 0,  0,  0,  0,  0 ],]      # Switch Status

        # Overall Track
        Sec = [A, B, C]


        ##########################################
        #       Section Arrays
        ##########################################
        
        # Overall Occupancy
        SecOcc = [0, 0, 0]

        # First Two Thirds Occupancy
        SecOccRest = [0, 0, 0]

        # Last Third Occupancy
        SecOccLastThird = [0, 0, 0]


        ##########################################
        #       Indexes
        ##########################################

        # Section
        SecIndex = 0

        # Block
        BlockIndex = 0

        ##########################################
        #       Placeholders
        ##########################################
        
        # Switch Commands
        SWStatus = 0
        SuggSWCmd = 0
        CmdSWCmd = 0

        # Signal Status & Commands
        SigStatus1 = 0
        SigStatus0 = 0
        TRKOutputSecBSignalCmd = '01'
        TRKOutputSecCSignalCmd = '01'

        # Crossing Status & Commands
        CrossStatus = 0
        TRKOutputCrossingCmd = 0

        # Occupancy Status
        Occ = 0

        # Speed Commands
        SuggSpeed = ''
        TRKOutputCmdSpeedValue = '0000000000'
        TRKOutputCmdSpeedSecIndex = 0
        TRKOutputCmdSpeedBlockIndex = 0

        # Authority Commands
        SuggAuth = ''
        TRKOutputCmdAuthValue = '0000000000'
        TRKOutputCmdAuthSecIndex = 0
        TRKOutputCmdAuthBlockIndex = 0


        #######################################################################################################################
        #
        #
        #                                                       Internal Functions
        #
        #
        #######################################################################################################################

        ##########################################
        #       Update Occupancies
        ##########################################
    
        # Individual Block
        def UpdateBlockOccupancy(self):
                # Update specific block Occupancy
                self.Sec[self.SecIndex][5][self.BlockIndex] = self.Occ

                # Counters to keep track of overall, rest, and last third occupancy
                OverallOccupancy = 0
                RestOccupancy = 0
                LastThirdOccupancy = 0

                # Update Section Occupancy
                for i in range(len(self.Sec)):               # iterates through section A, B, C
                        for j in range(len(self.Sec[i][5])): # iterates through row 5 (Occupancy) columns
                                if self.Sec[i][5][j] == 1:
                                        self.SecOcc[i] = 1
                                        OverallOccupancy += 1
                                        # Update Section Thirds Occupancy Status
                                        if j <= int((len(self.Sec[i][5])-1)*0.67):
                                                self.SecOccRest[i] = 1
                                                RestOccupancy += 1
                                        if j > int((len(self.Sec[i][5])-1)*0.67):
                                                self.SecOccLastThird[i] = 1
                                                LastThirdOccupancy += 1
                                # Reset Section Occupancy
                                if j == (len(self.Sec[i][5])-1):
                                        if OverallOccupancy == 0:
                                                self.SecOcc[i] = 0
                                        if RestOccupancy == 0:
                                                self.SecOccRest[i] = 0
                                        if LastThirdOccupancy == 0:
                                                self.SecOccLastThird[i] = 0

        # Overall Section
        def UpdateSectionOccupancy(self):
                pass

        # First Two Thirds of Section
        def UpdateFirstTwoThirdsOccupancy(self):
                pass

        # Last Third of Section
        def UpdateLastThirdOccupancy(self):
                pass

        
        ##########################################
        #       Update Switch Status
        ##########################################

        # Switch of Section
        def UpdateSwitchStatus(self):
                if self.SecIndex == 0:
                        self.SwitchStatus = self.TRKInputSWStatus.currentIndex()-1

                        self.Sec[self.SecIndex][6][4] = self.SwitchStatus
    

        ##########################################
        #       Update Signal Status
        ##########################################
                                        
        # Signal of Section
        def UpdateSignalStatus(self):
                if self.TRKInputSigStatus.currentText() == 'Green':
                        self.SigStatus1 = 0
                        self.SigStatus0 = 1
                elif self.TRKInputSigStatus.currentText() == 'Yellow':
                        self.SigStatus1 = 1
                        self.SigStatus0 = 0
                elif self.TRKInputSigStatus.currentText() == 'Red':
                        self.SigStatus1 = 1
                        self.SigStatus0 = 1

                if self.SecIndex == 1:
                        self.Sec[1][3][0] = self.SigStatus1
                        self.Sec[1][4][0] = self.SigStatus0
                elif self.SecIndex == 2:
                        self.Sec[2][3][0] = self.SigStatus1
                        self.Sec[2][4][0] = self.SigStatus0


        ##########################################
        #       Update Crossing Status
        ##########################################

        # Individual Crossing
        def UpdateCrossingStatus(self):
                self.CrossStatus = self.TRKInputCrossStatus.currentIndex()-1

                if self.SecIndex == 0:
                        self.Sec[self.SecIndex][2][0] = self.CrossStatus
                

        ##########################################
        #       Update Switch Command
        ##########################################
                
        # Section Switch Command
        def UpdateSwitchCmd(self):
                if self.SecIndex == 0:
                        if self.SuggSWCmd == 0:  # Switching from section A to B
                                if self.Sec[self.SecIndex][6][4] == 0:
                                        pass # Switch is already in the correct position
                                else:
                                        if self.SecOcc[self.SecIndex+1] == 0:
                                                self.CmdSWCmd = self.SuggSWCmd
                                        else:
                                                if self.SecOccLastThird[self.SecIndex+1] == 1 and self.SecOccRest[self.SecIndex+1] == 0:
                                                        self.CmdSwCmd = self.SuggSWCmd
                                                else:
                                                        self.CmdSwCmd = not(self.SuggSWCmd)

                        elif self.SuggSWCmd == 1: # Switching from section A to C
                                if self.Sec[self.SecIndex][6][4] == 1:
                                        pass # Switch is already in the correct position
                                else:
                                        if self.SecOcc[self.SecIndex+2] == 0:
                                                self.CmdSwCmd = self.SuggSWCmd
                                        else:
                                                if self.SecOccLastThird[self.SecIndex+1] == 1 and self.SecOccRest[self.SecIndex+1] == 0:
                                                        self.CmdSwCmd = self.SuggSWCmd
                                                else:
                                                        self.CmdSwCmd = not(self.SuggSWCmd)   


        ##########################################
        #       Update Signal Command
        ##########################################
        
        # Section Signal Command
        def UpdateSignalCmd(self):
                SecBSig1Cmd = 0
                SecBSig0Cmd = 0   
                SecCSig1Cmd = 0
                SecCSig0Cmd = 0

                # Section B Signal
                if self.SecOcc[1] == 1:
                        if self.SecOccRest[1] == 1:        # Signal is RED
                                SecBSig1Cmd = 1
                                SecBSig0Cmd = 1
                        elif self.SecOccLastThird[1] == 1: # Signal is YELLOW
                                SecBSig1Cmd = 1
                                SecBSig0Cmd = 0
                else:                                      # Signal is GREEN
                        SecBSig1Cmd = 0
                        SecBSig0Cmd = 1
                
                # Section C Signal
                if self.SecOcc[2] == 1:
                        if self.SecOccRest[2] == 1:        # Signal is RED
                                SecCSig1Cmd = 1
                                SecCSig0Cmd = 1
                        elif self.SecOccLastThird[2] == 1: # Signal is YELLOW
                                SecCSig1Cmd = 1
                                SecCSig0Cmd = 0
                else:                                      # Signal is GREEN
                        SecCSig1Cmd = 0
                        SecCSig0Cmd = 1

                # Convert SigCmd to Strings
                self.TRKOutputSecBSignalCmd = str(SecBSig1Cmd) + str(SecBSig0Cmd)
                self.TRKOutputSecCSignalCmd = str(SecCSig1Cmd) + str(SecCSig0Cmd)


        ##########################################
        #       Update Crossing Command
        ##########################################
        
        # Section Crossing Command
        def UpdateCrossingCmd(self):
                if self.SecOcc[0] == 1:
                        self.TRKOutputCrossCmd = 1
                else:
                        self.TRKOutputCrossCmd = 0


        ##########################################
        #       Update Speed Command
        ##########################################

        # Individual Block Speed Command
        def UpdateSpeedCmd(self):
                self.TRKOutputCmdSpeedBlockIndex = self.BlockIndex
                self.TRKOutputCmdSpeedSecIndex = self.SecIndex

                OccupiedBlockInFront = 0
                for i in range(self.BlockIndex+1, len(self.Sec[self.SecIndex][5])):
                        if self.Sec[self.SecIndex][5][i] == 1:
                                OccupiedBlockInFront = 1
                                break

                if OccupiedBlockInFront == 0: # Check if another occupancy is in front of train
                        # Section A
                        if self.SecIndex == 0:
                                if 3 <= self.BlockIndex <= 4: # Train is approaching switch
                                        if self.Sec[0][6][4] == 0 and self.SecOccRest[1] == 1: # Trying to move onto Occupied Track
                                                self.TRKOutputCmdSpeedValue = '0000000' + str(self.Sec[0][6][4]) + '10'
                                        
                                        elif self.Sec[0][6][4] == 0 and self.SecOccRest[1] == 0: # Trying to move onto Unoccupied Track
                                                self.TRKOutputCmdSpeedValue = self.SuggSpeed + str(self.Sec[0][6][4]) + '10'
                                elif self.BlockIndex < 3: # Train is not approaching switch
                                        self.TRKOutputCmdSpeedValue = self.SuggSpeed + str(self.Sec[0][6][4]) + '00'
                        
                        # Section B
                        elif self.SecIndex == 1:
                                self.TRKOutputCmdSpeedValue = self.SuggSpeed + str(self.Sec[1][6][5]) + '00'
                        
                        # Section C
                        elif self.SecIndex == 2:
                                self.TRKOutputCmdSpeedValue = self.SuggSpeed + str(self.Sec[2][6][4]) + '00'
                else:
                        self.TRKOutputCmdSpeedValue = '0000000000'


        ##########################################
        #       Update Authority Command
        ##########################################

        # Individual Block Authority Command
        def UpdateAuthCmd(self):
                self.TRKOutputCmdAuthBlockIndex = self.BlockIndex
                self.TRKOutputCmdAuthSecIndex = self.SecIndex

                OccupiedBlockInFront = 0
                for i in range(self.BlockIndex+1, len(self.Sec[self.SecIndex][5])):
                        if self.Sec[self.SecIndex][5][i] == 1:
                                OccupiedBlockInFront = 1
                                break

                if OccupiedBlockInFront == 0: # Check if another occupancy is in front of train
                        # Section A
                        if self.SecIndex == 0:
                                if 3 <= self.BlockIndex <= 4: # Train is approaching switch
                                        if self.Sec[0][6][4] == 0 and self.SecOccRest[1] == 1: # Trying to move onto Occupied Track
                                                self.TRKOutputCmdAuthValue = '0000000' + str(self.Sec[0][6][4]) + '10'
                                        
                                        elif self.Sec[0][6][4] == 0 and self.SecOccRest[1] == 0: # Trying to move onto Unoccupied Track
                                                self.TRKOutputCmdAuthValue = self.SuggAuth + str(self.Sec[0][6][4]) + '10'
                                elif self.BlockIndex < 3: # Train is not approaching switch
                                        self.TRKOutputCmdAuthValue = self.SuggAuth + str(self.Sec[0][6][4]) + '00'
                        
                        # Section B
                        elif self.SecIndex == 1:
                                self.TRKOutputCmdAuthValue = self.SuggAuth + str(self.Sec[1][6][5]) + '00'
                        
                        # Section C
                        elif self.SecIndex == 2:
                                self.TRKOutputCmdAuthValue = self.SuggAuth + str(self.Sec[2][6][4]) + '00'
                else:
                        self.TRKOutputCmdAuthValue = '0000000000'                      


#######################################################################################################################
#
#
#                                                       Main Execution
#
#
#######################################################################################################################

# Create the application object
app = QtWidgets.QApplication(sys.argv)

# Create main window instance
MainWindow = QtWidgets.QMainWindow()

# Create the UI object
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.retranslateUi(MainWindow)
MainWindow.show()

# Start application
sys.exit(app.exec())
