import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.CTC_logic import CTC_logic
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.CTCTrain import CTCTrain
from Resources.ClockComm import ClockComm
from Resources.ClockComm import ClockComm

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog

import datetime as dt

class CTC_frontend(object):
    def __init__(self, ctc_train_communicate: CTCTrain, wayside_communicate: CTCWaysideControllerComm, clock_communicate: ClockComm):
        self.ctc = CTC_logic(ctc_train_communicate, wayside_communicate)
        self.wayside_communicate = wayside_communicate
        self.ctc_train_communicate = ctc_train_communicate
        self.wayside_communicate.block_occupancy_signal.connect(self.update_block_occupancies)
        self.clock_communicate = clock_communicate
        self.clock_communicate.elapsed_seconds.connect(self.time_step)

        self.start_time = dt.datetime.now()
        self.current_time = self.start_time.time()
        self.selected_block = 0
        self.selected_train = 1

        self.stations = []
        


    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(848, 666)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainwindow.sizePolicy().hasHeightForWidth())
        mainwindow.setSizePolicy(sizePolicy)
        mainwindow.setMaximumSize(QtCore.QSize(900000, 1000))
        font = QtGui.QFont()
        font.setFamily("Arial")
        mainwindow.setFont(font)
        mainwindow.setStyleSheet("background-color: lightgray;")
        self.centralwidget = QtWidgets.QWidget(parent=mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pagetab = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.pagetab.setMaximumSize(QtCore.QSize(10000000, 750))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pagetab.setFont(font)
        self.pagetab.setStyleSheet("color: black;")
        self.pagetab.setObjectName("pagetab")
        self.TrainTab = QtWidgets.QWidget()
        self.TrainTab.setStyleSheet("color: black;")
        self.TrainTab.setObjectName("TrainTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.TrainTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.train_table = QtWidgets.QTableWidget(parent=self.TrainTab)
        self.train_table.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.train_table.sizePolicy().hasHeightForWidth())
        self.train_table.setSizePolicy(sizePolicy)
        self.train_table.setMinimumSize(QtCore.QSize(750, 100))
        self.train_table.setMaximumSize(QtCore.QSize(800, 200))
        self.train_table.setStyleSheet("font: 13pt \"Arial\";\n"
"background-color: lightgray;\n"
"color:black;")
        self.train_table.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.train_table.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.train_table.setLineWidth(2)
        self.train_table.setMidLineWidth(0)
        self.train_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.train_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.train_table.setAlternatingRowColors(False)
        self.train_table.setShowGrid(False)
        self.train_table.setRowCount(0)
        self.train_table.setObjectName("train_table")
        self.train_table.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(160, 160, 160))
        self.train_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(160, 160, 160))
        self.train_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(160, 160, 160))
        self.train_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(160, 160, 160))
        self.train_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(160, 160, 160))
        #self.train_table.setHorizontalHeaderItem(4, item)
        self.train_table.horizontalHeader().setCascadingSectionResizes(True)
        self.train_table.horizontalHeader().setDefaultSectionSize(190)
        self.train_table.horizontalHeader().setHighlightSections(True)
        self.train_table.horizontalHeader().setMinimumSectionSize(22)
        self.train_table.horizontalHeader().setSortIndicatorShown(True)
        self.train_table.horizontalHeader().setStretchLastSection(False)
        self.train_table.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.train_table, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.InfoLayout = QtWidgets.QGridLayout()
        self.InfoLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.InfoLayout.setContentsMargins(-1, 0, -1, -1)
        self.InfoLayout.setObjectName("InfoLayout")
        self.automatic_manual_toggle = QtWidgets.QPushButton(parent=self.TrainTab)
        self.automatic_manual_toggle.setMinimumSize(QtCore.QSize(130, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.automatic_manual_toggle.setFont(font)
        self.automatic_manual_toggle.setStyleSheet("background-color: rgb(255, 143, 27);\n"
"color:black;")
        self.automatic_manual_toggle.setObjectName("automatic_manual_toggle")
        self.automatic_manual_toggle.clicked.connect(self.auto_manual_toggle)
        self.InfoLayout.addWidget(self.automatic_manual_toggle, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ScheduleFrame = QtWidgets.QFrame(parent=self.TrainTab)
        self.ScheduleFrame.setMinimumSize(QtCore.QSize(570, 200))
        self.ScheduleFrame.setMaximumSize(QtCore.QSize(600, 16777215))
        self.ScheduleFrame.setStyleSheet("border: 2px solid #000000;")
        self.ScheduleFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ScheduleFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ScheduleFrame.setObjectName("ScheduleFrame")
        self.ScheduleTitle = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.ScheduleTitle.setGeometry(QtCore.QRect(10, 10, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.ScheduleTitle.setFont(font)
        self.ScheduleTitle.setStyleSheet("border: 0px;\n"
"color:black;")
        self.ScheduleTitle.setObjectName("ScheduleTitle")
        self.DepartureSelector = QtWidgets.QTimeEdit(parent=self.ScheduleFrame)
        self.DepartureSelector.setGeometry(QtCore.QRect(370, 60, 101, 24))
        self.DepartureSelector.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.DepartureSelector.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.DepartureSelector.setCalendarPopup(True)
        self.DepartureSelector.setObjectName("DepartureSelector")
        self.destinationLabel = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.destinationLabel.setGeometry(QtCore.QRect(200, 100, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.destinationLabel.setFont(font)
        self.destinationLabel.setStyleSheet("border: 0px;\n"
"color:black;")
        self.destinationLabel.setObjectName("destinationLabel")
        self.departureLabel = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.departureLabel.setGeometry(QtCore.QRect(200, 50, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.departureLabel.setFont(font)
        self.departureLabel.setStyleSheet("border: 0px;\n"
"color:black;")
        self.departureLabel.setObjectName("departureLabel")
        self.StationSelector = QtWidgets.QComboBox(parent=self.ScheduleFrame)
        self.StationSelector.setGeometry(QtCore.QRect(370, 110, 191, 26))
        self.StationSelector.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.StationSelector.setObjectName("StationSelector")
        self.ArrivalLabel = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.ArrivalLabel.setGeometry(QtCore.QRect(200, 150, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.ArrivalLabel.setFont(font)
        self.ArrivalLabel.setStyleSheet("border: 0px;\n"
"color:black;")
        self.ArrivalLabel.setObjectName("ArrivalLabel")
        self.ArrivalSelector = QtWidgets.QTimeEdit(parent=self.ScheduleFrame)
        self.ArrivalSelector.setEnabled(True)
        self.ArrivalSelector.setGeometry(QtCore.QRect(310, 160, 101, 24))
        self.ArrivalSelector.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.ArrivalSelector.setObjectName("ArrivalSelector")
        self.DispatchButton = QtWidgets.QPushButton(parent=self.ScheduleFrame)
        self.DispatchButton.setGeometry(QtCore.QRect(370, 10, 151, 32))
        self.DispatchButton.setStyleSheet("background-color: rgb(70, 158, 49);\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
        self.DispatchButton.setCheckable(False)
        self.DispatchButton.setObjectName("DispatchButton")
        self.DispatchButton.clicked.connect(self.dispatch_train)
        self.train_label = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.train_label.setGeometry(QtCore.QRect(10, 50, 60, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.train_label.setFont(font)
        self.train_label.setStyleSheet("border: 0px;\n"
"color:black;")
        self.train_label.setObjectName("train_label")
        self.Train_view_train_selector = QtWidgets.QSpinBox(parent=self.ScheduleFrame)
        self.Train_view_train_selector.setEnabled(True)
        self.Train_view_train_selector.setRange(1, 1)
        self.Train_view_train_selector.setGeometry(QtCore.QRect(80, 50, 100, 40))
        self.Train_view_train_selector.setMinimumSize(QtCore.QSize(90, 0))
        self.Train_view_train_selector.setMaximumSize(QtCore.QSize(100, 40))
        self.Train_view_train_selector.setStyleSheet("font: 18pt \"Arial\";\n"
"color:black;")
        self.Train_view_train_selector.setObjectName("Train_view_train_selector")
        self.Train_view_train_selector.valueChanged.connect(self.select_train )
        self.add_destination_button = QtWidgets.QPushButton(parent=self.ScheduleFrame)
        self.add_destination_button.setEnabled(True)
        self.add_destination_button.setGeometry(QtCore.QRect(420, 160, 141, 32))
        self.add_destination_button.setStyleSheet("background-color: rgb(133, 239, 128);\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
        self.add_destination_button.setCheckable(False)
        self.add_destination_button.setObjectName("add_destination_button")
        self.add_destination_button.clicked.connect(self.add_destination)
        self.destination_list_label = QtWidgets.QLabel(parent=self.ScheduleFrame)
        self.destination_list_label.setGeometry(QtCore.QRect(10, 100, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.destination_list_label.setFont(font)
        self.destination_list_label.setStyleSheet("border: 0px;\n"
"color:black;")
        self.destination_list_label.setObjectName("destination_list_label")
        self.destination_scroll_area = QtWidgets.QScrollArea(parent=self.ScheduleFrame)
        self.destination_scroll_area.setGeometry(QtCore.QRect(10, 130, 171, 61))
        self.destination_scroll_area.setWidgetResizable(True)
        self.destination_scroll_area.setObjectName("destination_scroll_area")
        self.destination_scroll_area.setDisabled(False)
        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 167, 57))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.destination_list = QtWidgets.QListWidget(parent=self.scroll_area_contents)
        self.destination_list.setEnabled(False)
        self.destination_list.setGeometry(QtCore.QRect(-10, -10, 181, 71))
        self.destination_list.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.destination_list.setObjectName("destination_list")
        self.destination_scroll_area.setWidget(self.scroll_area_contents)
        self.InfoLayout.addWidget(self.ScheduleFrame, 2, 0, 2, 1)
        self.HeaderFrame = QtWidgets.QFrame(parent=self.TrainTab)
        self.HeaderFrame.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.HeaderFrame.setFont(font)
        self.HeaderFrame.setStyleSheet("background-color: rgb(75, 120, 228);")
        self.HeaderFrame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.HeaderFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.HeaderFrame.setObjectName("HeaderFrame")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.HeaderFrame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 761, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.HeaderLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.HeaderLayout.setContentsMargins(0, 0, 0, 0)
        self.HeaderLayout.setObjectName("HeaderLayout")
        self.HeaderLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.HeaderLabel.setFont(font)
        self.HeaderLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.HeaderLabel.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.HeaderLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HeaderLabel.setObjectName("HeaderLabel")
        self.HeaderLayout.addWidget(self.HeaderLabel)
        self.InfoLayout.addWidget(self.HeaderFrame, 0, 0, 2, 2)
        self.ThroughputFrame = QtWidgets.QFrame(parent=self.TrainTab)
        self.ThroughputFrame.setMinimumSize(QtCore.QSize(170, 170))
        self.ThroughputFrame.setMaximumSize(QtCore.QSize(170, 170))
        self.ThroughputFrame.setStyleSheet("border-color: rgb(0, 0, 0);\n"
"border: 2px solid;\n"
"")
        self.ThroughputFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ThroughputFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ThroughputFrame.setObjectName("ThroughputFrame")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.ThroughputFrame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 171, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.ThroughputLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.ThroughputLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.ThroughputLayout.setContentsMargins(10, 10, 10, 10)
        self.ThroughputLayout.setSpacing(5)
        self.ThroughputLayout.setObjectName("ThroughputLayout")
        self.TimeLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.TimeLabel.setMaximumSize(QtCore.QSize(120, 60))
        self.TimeLabel.setStyleSheet("font: 36pt \"Arial\";\n"
"color:black;")
        self.TimeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TimeLabel.setObjectName("TimeLabel")
        self.ThroughputLayout.addWidget(self.TimeLabel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.ThroughputDisplay = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.ThroughputDisplay.setMinimumSize(QtCore.QSize(150, 40))
        self.ThroughputDisplay.setMaximumSize(QtCore.QSize(160, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ThroughputDisplay.setFont(font)
        self.ThroughputDisplay.setStyleSheet("border: 2px;\n"
"border-color: rgb(0, 0, 0);\n"
"font: 18pt \"Arial\";\n"
"background-color: rgb(43, 120, 228);\n"
"color:black;")
        self.ThroughputDisplay.setLineWidth(4)
        self.ThroughputDisplay.setMidLineWidth(4)
        self.ThroughputDisplay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ThroughputDisplay.setObjectName("ThroughputDisplay")
        self.ThroughputLayout.addWidget(self.ThroughputDisplay, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.UploadScheduleButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.UploadScheduleButton.setMinimumSize(QtCore.QSize(150, 30))
        self.UploadScheduleButton.setMaximumSize(QtCore.QSize(200, 40))
        self.UploadScheduleButton.setStyleSheet("background-color: lightgray;\n"
"border: 1px solid;\n"
"font: 18pt \"Arial\";\n"
"\n"
"color:black;")

        self.UploadScheduleButton.setObjectName("UploadScheduleButton")
        self.UploadScheduleButton.clicked.connect(self.upload_schedule)
        self.ThroughputLayout.addWidget(self.UploadScheduleButton)
        self.InfoLayout.addWidget(self.ThroughputFrame, 2, 1, 1, 1)
        self.gridLayout_3.addLayout(self.InfoLayout, 0, 0, 2, 1)
        self.pagetab.addTab(self.TrainTab, "")
        self.BlockTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.BlockTab.setFont(font)
        self.BlockTab.setStyleSheet("color: black;")
        self.BlockTab.setObjectName("BlockTab")
        self.frame = QtWidgets.QFrame(parent=self.BlockTab)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 811, 691))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(parent=self.frame)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(1, 0, 801, 691))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.InfoLayout_pg2 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.InfoLayout_pg2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.InfoLayout_pg2.setContentsMargins(5, 5, 5, 5)
        self.InfoLayout_pg2.setHorizontalSpacing(10)
        self.InfoLayout_pg2.setObjectName("InfoLayout_pg2")
        self.upload_layout_button = QtWidgets.QPushButton(parent=self.gridLayoutWidget_5)
        self.upload_layout_button.setMinimumSize(QtCore.QSize(180, 0))
        self.upload_layout_button.setMaximumSize(QtCore.QSize(180, 16777215))
        self.upload_layout_button.setStyleSheet("background-color: pink;\n"
"color:black;")
        self.upload_layout_button.setObjectName("upload_layout_button")
        self.upload_layout_button.clicked.connect(self.upload_layout)
        self.InfoLayout_pg2.addWidget(self.upload_layout_button, 2, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.MaintenanceFrame = QtWidgets.QFrame(parent=self.gridLayoutWidget_5)
        self.MaintenanceFrame.setMinimumSize(QtCore.QSize(300, 170))
        self.MaintenanceFrame.setMaximumSize(QtCore.QSize(350, 180))
        self.MaintenanceFrame.setStyleSheet("border-color: rgb(0, 0, 0);\n"
"border: 2px solid #000000;")
        self.MaintenanceFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.MaintenanceFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.MaintenanceFrame.setObjectName("MaintenanceFrame")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.MaintenanceFrame)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 351, 181))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.MaintenanceLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.MaintenanceLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.MaintenanceLayout.setContentsMargins(0, 0, 0, 10)
        self.MaintenanceLayout.setSpacing(0)
        self.MaintenanceLayout.setObjectName("MaintenanceLayout")
        self.MaintenanceTitle = QtWidgets.QLabel(parent=self.verticalLayoutWidget_5)
        self.MaintenanceTitle.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.MaintenanceTitle.setFont(font)
        self.MaintenanceTitle.setStyleSheet("border: 0px;\n"
"color:black;")
        self.MaintenanceTitle.setObjectName("MaintenanceTitle")
        self.MaintenanceLayout.addWidget(self.MaintenanceTitle, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.departureLabel_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_5)
        self.departureLabel_2.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.departureLabel_2.setFont(font)
        self.departureLabel_2.setStyleSheet("font: 30pt \"Arial\";\n"
"border: 0px;\n"
"color:black;")
        self.departureLabel_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.departureLabel_2.setLineWidth(2)
        self.departureLabel_2.setObjectName("departureLabel_2")
        self.MaintenanceLayout.addWidget(self.departureLabel_2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.MaintenanceButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        self.MaintenanceButton.setMinimumSize(QtCore.QSize(0, 30))
        self.MaintenanceButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.MaintenanceButton.setFont(font)
        self.MaintenanceButton.setStyleSheet("background-color: #b88804;\n"
"border: 1px solid;\n"
"\n"
"color:black;")
        self.MaintenanceButton.setObjectName("MaintenanceButton")
        self.MaintenanceButton.clicked.connect(self.maintenance_mode)
        self.MaintenanceLayout.addWidget(self.MaintenanceButton, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.InfoLayout_pg2.addWidget(self.MaintenanceFrame, 1, 0, 2, 1)
        self.ThroughputFrame_pg2 = QtWidgets.QFrame(parent=self.gridLayoutWidget_5)
        self.ThroughputFrame_pg2.setMinimumSize(QtCore.QSize(175, 130))
        self.ThroughputFrame_pg2.setMaximumSize(QtCore.QSize(200, 142))
        self.ThroughputFrame_pg2.setStyleSheet("border: 2px solid #000000;\n"
"")
        self.ThroughputFrame_pg2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ThroughputFrame_pg2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ThroughputFrame_pg2.setObjectName("ThroughputFrame_pg2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.ThroughputFrame_pg2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 201, 141))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.ThroughputLayout_pg2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.ThroughputLayout_pg2.setContentsMargins(10, 10, 10, 10)
        self.ThroughputLayout_pg2.setSpacing(10)
        self.ThroughputLayout_pg2.setObjectName("ThroughputLayout_pg2")
        self.TimeLabel_pg2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.TimeLabel_pg2.setMaximumSize(QtCore.QSize(120, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.TimeLabel_pg2.setFont(font)
        self.TimeLabel_pg2.setStyleSheet("color:black;")
        self.TimeLabel_pg2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TimeLabel_pg2.setObjectName("TimeLabel_pg2")
        self.ThroughputLayout_pg2.addWidget(self.TimeLabel_pg2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.ThroughputDisplay_pg2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.ThroughputDisplay_pg2.setMinimumSize(QtCore.QSize(150, 40))
        self.ThroughputDisplay_pg2.setMaximumSize(QtCore.QSize(160, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ThroughputDisplay_pg2.setFont(font)
        self.ThroughputDisplay_pg2.setStyleSheet("border: 2px;\n"
"border-color: rgb(0, 0, 0);\n"
"font: 18pt \"Arial\";\n"
"background-color: rgb(43, 120, 228);\n"
"color: rgb(0, 0, 0);")
        self.ThroughputDisplay_pg2.setLineWidth(4)
        self.ThroughputDisplay_pg2.setMidLineWidth(4)
        self.ThroughputDisplay_pg2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ThroughputDisplay_pg2.setObjectName("ThroughputDisplay_pg2")
        self.ThroughputLayout_pg2.addWidget(self.ThroughputDisplay_pg2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.InfoLayout_pg2.addWidget(self.ThroughputFrame_pg2, 1, 2, 1, 1)
        self.HeaderFrame_pg2 = QtWidgets.QFrame(parent=self.gridLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeaderFrame_pg2.sizePolicy().hasHeightForWidth())
        self.HeaderFrame_pg2.setSizePolicy(sizePolicy)
        self.HeaderFrame_pg2.setMinimumSize(QtCore.QSize(600, 0))
        self.HeaderFrame_pg2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.HeaderFrame_pg2.setFont(font)
        self.HeaderFrame_pg2.setStyleSheet("background-color: rgb(75, 120, 228);")
        self.HeaderFrame_pg2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.HeaderFrame_pg2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.HeaderFrame_pg2.setObjectName("HeaderFrame_pg2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.HeaderFrame_pg2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, -5, 791, 71))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.HeaderLayout_pg2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.HeaderLayout_pg2.setContentsMargins(0, 0, 0, 0)
        self.HeaderLayout_pg2.setObjectName("HeaderLayout_pg2")
        self.HeaderLabel_pg2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeaderLabel_pg2.sizePolicy().hasHeightForWidth())
        self.HeaderLabel_pg2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.HeaderLabel_pg2.setFont(font)
        self.HeaderLabel_pg2.setStyleSheet("color: rgb(255, 255, 255);")
        self.HeaderLabel_pg2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HeaderLabel_pg2.setObjectName("HeaderLabel_pg2")
        self.HeaderLayout_pg2.addWidget(self.HeaderLabel_pg2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.InfoLayout_pg2.addWidget(self.HeaderFrame_pg2, 0, 0, 1, 3)
        self.SearchFrame = QtWidgets.QFrame(parent=self.gridLayoutWidget_5)
        self.SearchFrame.setMinimumSize(QtCore.QSize(200, 0))
        self.SearchFrame.setMaximumSize(QtCore.QSize(200, 191))
        self.SearchFrame.setStyleSheet("border-color: rgb(0, 0, 0);\n"
"border: 2px solid #000000;")
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.SearchFrame.setLineWidth(2)
        self.SearchFrame.setObjectName("SearchFrame")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.SearchFrame)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(-1, -1, 201, 191))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.SearchLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.SearchLayout.setContentsMargins(0, 5, 0, 10)
        self.SearchLayout.setSpacing(5)
        self.SearchLayout.setObjectName("SearchLayout")
        self.SearchLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_6)
        self.SearchLabel.setMaximumSize(QtCore.QSize(200, 30))
        self.SearchLabel.setStyleSheet("font: 24pt \"Arial\";\n"
"border: 0px;\n"
"color:black;")
        self.SearchLabel.setObjectName("SearchLabel")
        self.SearchLayout.addWidget(self.SearchLabel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.BlockSearchSubLayout = QtWidgets.QGridLayout()
        self.BlockSearchSubLayout.setObjectName("BlockSearchSubLayout")
        self.LineSelectorComboBox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget_6)
        self.LineSelectorComboBox.setEnabled(False)
        self.LineSelectorComboBox.setMinimumSize(QtCore.QSize(90, 0))
        self.LineSelectorComboBox.setMaximumSize(QtCore.QSize(100, 40))
        self.LineSelectorComboBox.setStyleSheet("font: 18pt \"Arial\";\n"
"color:black;")
        self.LineSelectorComboBox.setObjectName("LineSelectorComboBox")
        self.LineSelectorComboBox.addItem("")
        self.LineSelectorComboBox.addItem("")
        self.LineSelectorComboBox.addItem("")
        self.BlockSearchSubLayout.addWidget(self.LineSelectorComboBox, 0, 1, 1, 1)
        self.SearchLineLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_6)
        self.SearchLineLabel.setMaximumSize(QtCore.QSize(70, 40))
        self.SearchLineLabel.setStyleSheet("color:black;\n"
"font: 24pt \"Arial\";\n"
"border: 0px;\n"
"")
        self.SearchLineLabel.setObjectName("SearchLineLabel")
        self.BlockSearchSubLayout.addWidget(self.SearchLineLabel, 0, 0, 1, 1)
        self.BlockSelectorLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_6)
        self.BlockSelectorLabel.setMaximumSize(QtCore.QSize(70, 40))
        self.BlockSelectorLabel.setStyleSheet("font: 24pt \"Arial\";\n"
"border: 0px;\n"
"color:black;")
        self.BlockSelectorLabel.setObjectName("BlockSelectorLabel")
        self.BlockSearchSubLayout.addWidget(self.BlockSelectorLabel, 1, 0, 1, 1)
        self.block_page_block_selector = QtWidgets.QSpinBox(parent=self.verticalLayoutWidget_6)
        self.block_page_block_selector.setMaximumSize(QtCore.QSize(80, 16777215))
        self.block_page_block_selector.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.block_page_block_selector.setObjectName("block_page_block_selector")
        self.BlockSearchSubLayout.addWidget(self.block_page_block_selector, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.block_page_block_selector.valueChanged.connect(self.select_block)
        self.SearchLayout.addLayout(self.BlockSearchSubLayout)
        self.block_maintenance_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_6)
        self.block_maintenance_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.block_maintenance_button.setStyleSheet("font: 18pt \"Arial\";\n"
"background-color: rgb(0, 209, 41);\n"
"border: 1px solid;\n"
"color:black;")
        self.block_maintenance_button.setObjectName("block_maintenance_button")
        self.block_maintenance_button.clicked.connect(self.toggle_block_maintenance)
        self.SearchLayout.addWidget(self.block_maintenance_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.InfoLayout_pg2.addWidget(self.SearchFrame, 1, 1, 2, 1)
        self.block_table = QtWidgets.QTableWidget(parent=self.gridLayoutWidget_5)
        self.block_table.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.block_table.sizePolicy().hasHeightForWidth())
        self.block_table.setSizePolicy(sizePolicy)
        self.block_table.setMinimumSize(QtCore.QSize(775, 0))
        self.block_table.setMaximumSize(QtCore.QSize(16777215, 300))
        self.block_table.setStyleSheet("font: 13pt \"Arial\";\n"
"color:black;")
        self.block_table.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.block_table.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.block_table.setLineWidth(2)
        self.block_table.setMidLineWidth(0)
        self.block_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.block_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.block_table.setAutoScroll(True)
        self.block_table.setShowGrid(True)
        self.block_table.setRowCount(0)
        self.block_table.setObjectName("block_table")
        self.block_table.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table.setHorizontalHeaderItem(3, item)
        self.block_table.horizontalHeader().setCascadingSectionResizes(True)
        self.block_table.horizontalHeader().setDefaultSectionSize(193)
        self.block_table.horizontalHeader().setHighlightSections(True)
        self.block_table.horizontalHeader().setMinimumSectionSize(22)
        self.block_table.horizontalHeader().setSortIndicatorShown(True)
        self.block_table.horizontalHeader().setStretchLastSection(False)
        self.block_table.verticalHeader().setVisible(False)
        self.InfoLayout_pg2.addWidget(self.block_table, 3, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.InfoLayout_pg2.setColumnStretch(0, 1)
        self.InfoLayout_pg2.setRowStretch(0, 1)
        self.pagetab.addTab(self.BlockTab, "")
        self.TestTab = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.TestTab.setFont(font)
        self.TestTab.setStyleSheet("color: black;")
        self.TestTab.setObjectName("TestTab")
        self.TestBenchFrame = QtWidgets.QFrame(parent=self.TestTab)
        self.TestBenchFrame.setGeometry(QtCore.QRect(0, 0, 821, 711))
        self.TestBenchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.TestBenchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.TestBenchFrame.setObjectName("TestBenchFrame")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.TestBenchFrame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 818, 701))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.TestBenchLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.TestBenchLayout.setContentsMargins(5, 5, 10, 5)
        self.TestBenchLayout.setObjectName("TestBenchLayout")
        self.block_table_test_bench = QtWidgets.QTableWidget(parent=self.gridLayoutWidget)
        self.block_table_test_bench.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.block_table_test_bench.sizePolicy().hasHeightForWidth())
        self.block_table_test_bench.setSizePolicy(sizePolicy)
        self.block_table_test_bench.setMinimumSize(QtCore.QSize(0, 100))
        self.block_table_test_bench.setMaximumSize(QtCore.QSize(800, 300))
        self.block_table_test_bench.setStyleSheet("font: 13pt \"Arial\";\n"
"color: black;")
        self.block_table_test_bench.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.block_table_test_bench.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.block_table_test_bench.setLineWidth(2)
        self.block_table_test_bench.setMidLineWidth(0)
        self.block_table_test_bench.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.block_table_test_bench.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.block_table_test_bench.setShowGrid(True)
        self.block_table_test_bench.setRowCount(0)
        self.block_table_test_bench.setObjectName("block_table_test_bench")
        self.block_table_test_bench.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table_test_bench.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table_test_bench.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table_test_bench.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table_test_bench.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        item.setFont(font)
        item.setBackground(QtGui.QColor(159, 159, 159))
        self.block_table_test_bench.setHorizontalHeaderItem(4, item)
        self.block_table_test_bench.horizontalHeader().setCascadingSectionResizes(True)
        self.block_table_test_bench.horizontalHeader().setDefaultSectionSize(158)
        self.block_table_test_bench.horizontalHeader().setHighlightSections(True)
        self.block_table_test_bench.horizontalHeader().setMinimumSectionSize(22)
        self.block_table_test_bench.horizontalHeader().setSortIndicatorShown(True)
        self.block_table_test_bench.horizontalHeader().setStretchLastSection(False)
        self.block_table_test_bench.verticalHeader().setVisible(False)
        self.TestBenchLayout.addWidget(self.block_table_test_bench, 3, 0, 1, 2)
        self.HeaderFrame_pg3 = QtWidgets.QFrame(parent=self.gridLayoutWidget)
        self.HeaderFrame_pg3.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.HeaderFrame_pg3.setFont(font)
        self.HeaderFrame_pg3.setStyleSheet("background-color: rgb(75, 120, 228);")
        self.HeaderFrame_pg3.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.HeaderFrame_pg3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.HeaderFrame_pg3.setObjectName("HeaderFrame_pg3")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(parent=self.HeaderFrame_pg3)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(-1, -1, 801, 61))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.HeaderLayout_pg3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.HeaderLayout_pg3.setContentsMargins(0, 0, 0, 0)
        self.HeaderLayout_pg3.setObjectName("HeaderLayout_pg3")
        self.HeaderLabel_pg3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_8)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(48)
        self.HeaderLabel_pg3.setFont(font)
        self.HeaderLabel_pg3.setStyleSheet("color: rgb(255, 255, 255);")
        self.HeaderLabel_pg3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HeaderLabel_pg3.setObjectName("HeaderLabel_pg3")
        self.HeaderLayout_pg3.addWidget(self.HeaderLabel_pg3)
        self.TestBenchLayout.addWidget(self.HeaderFrame_pg3, 0, 0, 1, 2)
        self.train_outputs_frame = QtWidgets.QFrame(parent=self.gridLayoutWidget)
        self.train_outputs_frame.setMinimumSize(QtCore.QSize(572, 0))
        self.train_outputs_frame.setMaximumSize(QtCore.QSize(610, 100))
        self.train_outputs_frame.setStyleSheet("border: 2px solid #000000")
        self.train_outputs_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.train_outputs_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.train_outputs_frame.setLineWidth(2)
        self.train_outputs_frame.setObjectName("train_outputs_frame")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(parent=self.train_outputs_frame)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(-1, -1, 611, 101))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.train_outputs_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.train_outputs_layout.setContentsMargins(10, 10, 10, 10)
        self.train_outputs_layout.setObjectName("train_outputs_layout")
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        self.label_2.setStyleSheet("border: 0px;\n"
"font: 18pt \"Arial\";\n"
"color: black;")
        self.label_2.setObjectName("label_2")
        self.train_outputs_layout.addWidget(self.label_2, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.suggested_speed_display = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        self.suggested_speed_display.setStyleSheet("border: 2px solid #000000;\n"
"font: 13pt \"Arial\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;")
        self.suggested_speed_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.suggested_speed_display.setObjectName("suggested_speed_display")
        self.train_outputs_layout.addWidget(self.suggested_speed_display, 1, 1, 1, 1)
        self.train_number_selector = QtWidgets.QSpinBox(parent=self.gridLayoutWidget_6)
        self.train_number_selector.setEnabled(True)
        self.train_number_selector.setStyleSheet("font: 13pt \"Arial\";\n"
"color: black;")
        self.train_number_selector.setObjectName("train_number_selector")
        self.train_outputs_layout.addWidget(self.train_number_selector, 0, 1, 1, 1)
        self.train_number_label = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        self.train_number_label.setStyleSheet("font: 18pt \"Arial\";\n"
"border: 0px;\n"
"color: black;")
        self.train_number_label.setObjectName("train_number_label")
        self.train_outputs_layout.addWidget(self.train_number_label, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("border: 0px;\n"
"font: 18pt \"Arial\";\n"
"color: black;")
        self.label.setObjectName("label")
        self.train_outputs_layout.addWidget(self.label, 1, 0, 1, 1)
        self.authority_display = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        self.authority_display.setMaximumSize(QtCore.QSize(130, 16777215))
        self.authority_display.setStyleSheet("border: 2px solid #000000;\n"
"font: 13pt \"Arial\";\n"
"background-color: rgb(255, 255, 255);\n"
"color: black;")
        self.authority_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.authority_display.setObjectName("authority_display")
        self.train_outputs_layout.addWidget(self.authority_display, 1, 3, 1, 1)
        self.train_outputs_label = QtWidgets.QLabel(parent=self.gridLayoutWidget_6)
        self.train_outputs_label.setMinimumSize(QtCore.QSize(200, 50))
        self.train_outputs_label.setMaximumSize(QtCore.QSize(275, 16777215))
        self.train_outputs_label.setStyleSheet("font: 24pt \"Arial\";\n"
"border: 0px;\n"
"color: black;")
        self.train_outputs_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.train_outputs_label.setObjectName("train_outputs_label")
        self.train_outputs_layout.addWidget(self.train_outputs_label, 0, 2, 1, 2)
        self.TestBenchLayout.addWidget(self.train_outputs_frame, 1, 1, 1, 1)
        self.BlockSelectorFrame = QtWidgets.QFrame(parent=self.gridLayoutWidget)
        self.BlockSelectorFrame.setMinimumSize(QtCore.QSize(150, 100))
        self.BlockSelectorFrame.setMaximumSize(QtCore.QSize(170, 100))
        font = QtGui.QFont()
        self.BlockSelectorFrame.setFont(font)
        self.BlockSelectorFrame.setStyleSheet("border: 2px solid black;")
        self.BlockSelectorFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.BlockSelectorFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.BlockSelectorFrame.setLineWidth(2)
        self.BlockSelectorFrame.setObjectName("BlockSelectorFrame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.BlockSelectorFrame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 171, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(70, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border: 0px solid black;\n"
"color: black;")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spinBox = QtWidgets.QSpinBox(parent=self.horizontalLayoutWidget)
        self.spinBox.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spinBox.setStyleSheet("color: black;")
        self.spinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.valueChanged.connect(self.select_block)
        self.horizontalLayout.addWidget(self.spinBox)
        self.TestBenchLayout.addWidget(self.BlockSelectorFrame, 1, 0, 1, 1)
        self.HeaderFrame_pg3.raise_()
        self.train_outputs_frame.raise_()
        self.block_table_test_bench.raise_()
        self.BlockSelectorFrame.raise_()
        self.pagetab.addTab(self.TestTab, "")
        self.gridLayout.addWidget(self.pagetab, 0, 0, 1, 1)
        mainwindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainwindow)
        self.pagetab.setCurrentIndex(0)
        self.LineSelectorComboBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)
        #self.updateUI()

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "MainWindow"))
        self.train_table.setSortingEnabled(True)
        item = self.train_table.horizontalHeaderItem(0)
        item.setText(_translate("mainwindow", "Train #"))
        item = self.train_table.horizontalHeaderItem(1)
        item.setText(_translate("mainwindow", "Current Block"))
        item = self.train_table.horizontalHeaderItem(2)
        item.setText(_translate("mainwindow", "Next Destination"))
        item = self.train_table.horizontalHeaderItem(3)
        item.setText(_translate("mainwindow", "Arrival Time"))
        #item = self.train_table.horizontalHeaderItem(4)
        #item.setText(_translate("mainwindow", "Yard Departure Time"))
        self.automatic_manual_toggle.setText(_translate("mainwindow", "Auto Mode"))
        self.ScheduleTitle.setText(_translate("mainwindow", "Schedule New Train"))
        self.DepartureSelector.setDisplayFormat(_translate("mainwindow", "hh:mm"))
        self.destinationLabel.setText(_translate("mainwindow", "Destination Station:"))
        self.departureLabel.setText(_translate("mainwindow", "Departure Time:"))
        self.ArrivalLabel.setText(_translate("mainwindow", "Arrival Time:"))
        self.ArrivalSelector.setDisplayFormat(_translate("mainwindow", "hh:mm"))
        self.DispatchButton.setText(_translate("mainwindow", "Dispatch Train"))
        self.train_label.setText(_translate("mainwindow", "Train #"))
        self.add_destination_button.setText(_translate("mainwindow", "Add Destination"))
        self.destination_list_label.setText(_translate("mainwindow", "Destinations:"))
        self.HeaderLabel.setText(_translate("mainwindow", "CTC"))
        self.TimeLabel.setText(_translate("mainwindow", self.current_time.strftime("%H:%M")))
        self.ThroughputDisplay.setText(_translate("mainwindow", "X Trains/hr/line"))
        self.UploadScheduleButton.setText(_translate("mainwindow", "Upload Schedule"))
        self.pagetab.setTabText(self.pagetab.indexOf(self.TrainTab), _translate("mainwindow", "Train View"))
        self.pagetab.setTabToolTip(self.pagetab.indexOf(self.TrainTab), _translate("mainwindow", "Schedule new trains & view existing train information"))
        self.upload_layout_button.setText(_translate("mainwindow", "Upload Layout"))
        self.MaintenanceTitle.setText(_translate("mainwindow", "Place Block in Maintanence Mode"))
        self.departureLabel_2.setText(_translate("mainwindow", "No Block Selected"))
        self.MaintenanceButton.setText(_translate("mainwindow", "Maintenance Mode"))
        self.TimeLabel_pg2.setText(_translate("mainwindow", self.current_time.strftime("%H:%M")))
        self.ThroughputDisplay_pg2.setText(_translate("mainwindow", "X Trains/hr/line"))
        self.HeaderLabel_pg2.setText(_translate("mainwindow", "CTC"))
        self.SearchLabel.setText(_translate("mainwindow", "Search Blocks"))
        self.LineSelectorComboBox.setItemText(0, _translate("mainwindow", "Blue"))
        self.LineSelectorComboBox.setItemText(1, _translate("mainwindow", "Red"))
        self.LineSelectorComboBox.setItemText(2, _translate("mainwindow", "Green"))
        self.SearchLineLabel.setText(_translate("mainwindow", "Line:"))
        self.BlockSelectorLabel.setText(_translate("mainwindow", "Block:"))
        self.block_maintenance_button.setText(_translate("mainwindow", "Block Maintenance"))
        self.block_table.setSortingEnabled(True)
        item = self.block_table.horizontalHeaderItem(0)
        item.setText(_translate("mainwindow", "Block #"))
        item = self.block_table.horizontalHeaderItem(1)
        item.setText(_translate("mainwindow", "Section ID"))
        item = self.block_table.horizontalHeaderItem(2)
        item.setText(_translate("mainwindow", "Occupied"))
        item = self.block_table.horizontalHeaderItem(3)
        item.setText(_translate("mainwindow", "Maintenance"))
        self.pagetab.setTabText(self.pagetab.indexOf(self.BlockTab), _translate("mainwindow", "Block View"))
        self.pagetab.setTabToolTip(self.pagetab.indexOf(self.BlockTab), _translate("mainwindow", "View the status of blocks"))
        self.block_table_test_bench.setSortingEnabled(True)
        item = self.block_table_test_bench.horizontalHeaderItem(0)
        item.setText(_translate("mainwindow", "Block #"))
        item = self.block_table_test_bench.horizontalHeaderItem(1)
        item.setText(_translate("mainwindow", "Section ID"))
        item = self.block_table_test_bench.horizontalHeaderItem(2)
        item.setText(_translate("mainwindow", "Occupied"))
        item = self.block_table_test_bench.horizontalHeaderItem(3)
        item.setText(_translate("mainwindow", "Maintenance Mode"))
        item = self.block_table_test_bench.horizontalHeaderItem(4)
        item.setText(_translate("mainwindow", "Switch State"))
        self.HeaderLabel_pg3.setText(_translate("mainwindow", "CTC"))
        self.label_2.setText(_translate("mainwindow", "Authority:"))
        self.suggested_speed_display.setText(_translate("mainwindow", "0 mph"))
        self.train_number_label.setText(_translate("mainwindow", "Train #:"))
        self.label.setText(_translate("mainwindow", "Suggested Speed:"))
        self.authority_display.setText(_translate("mainwindow", "0 blocks"))
        self.train_outputs_label.setText(_translate("mainwindow", "Outputs to Train"))
        self.label_3.setText(_translate("mainwindow", "Block #:"))
        self.pagetab.setTabText(self.pagetab.indexOf(self.TestTab), _translate("mainwindow", "Test Bench"))
        self.pagetab.setTabToolTip(self.pagetab.indexOf(self.TestTab), _translate("mainwindow", "Test I/O operation"))

        self.DepartureSelector.setTime(QtCore.QTime.currentTime())
        self.ArrivalSelector.setTime(QtCore.QTime.currentTime())



    def updateUI(self):

        _translate = QtCore.QCoreApplication.translate
        
        self.TimeLabel.setText(self.current_time.strftime("%H:%M"))
        self.TimeLabel_pg2.setText(self.current_time.strftime("%H:%M"))

        curr_time = dt.datetime.combine(dt.date.today(), self.current_time)

        if (self.ctc.line.train_list):
                train_index = [train.train_id for train in self.ctc.line.train_list].index(self.Train_view_train_selector.value())
                earliest_arrival = curr_time + dt.timedelta(seconds=self.ctc.line.arrival_time_between(self.ctc.line.train_list[train_index].location, self.ctc.line.train_list[train_index].destinations[0]))
                if (dt.time(hour=self.ArrivalSelector.time().hour(), minute=self.ArrivalSelector.time().minute()) < earliest_arrival.time()):
                        self.ArrivalSelector.setTime(QtCore.QTime(earliest_arrival.time().hour, earliest_arrival.time().minute, earliest_arrival.time().second))

        through = str(self.ctc.line.throughput) + " Trains/hr/line"
        self.ThroughputDisplay.setText(through)
        self.ThroughputDisplay_pg2.setText(through)

        self.train_table.clear()
        self.train_table.setRowCount(len(self.ctc.line.train_list))

        if len(self.ctc.line.train_list):
            for index, train in enumerate(self.ctc.line.train_list):

                self.train_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(train.train_id)))
                self.train_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(train.location)))
                self.train_table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(train.destination_strings[0])))
                if train.arrival_times[0] != None: 
                        #curr_time = dt.datetime.combine(dt.date.today(), self.current_time)
                        #time = curr_time + dt.timedelta(seconds=train.arrival_times[0])
                        self.train_table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(train.arrival_times[0].strftime("%H:%M"))))

                #self.train_table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(train.departure_time.strftime("%H:%M"))))
        
                for col in range(4):
                    item1 = self.train_table.item(index, col)
                    item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.train_table.setColumnCount(4)

            headers = ["Train #", "Current Block", "Next Destination", "Arrival Time", "Yard Departure Time"]
            for col, header in enumerate(headers):
                item = self.train_table.horizontalHeaderItem(col)
                if item is None:
                    item = QtWidgets.QTableWidgetItem()
                    self.train_table.setHorizontalHeaderItem(col, item)
                item.setText(_translate("mainwindow", header))

            self.train_table.setShowGrid(True)

        self.block_table.setRowCount(len(self.ctc.line.layout))
        self.block_table_test_bench.setRowCount(len(self.ctc.line.layout))

        for index, block in enumerate(self.ctc.line.layout):
            self.block_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(block.block_number)))
            self.block_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(block.section)))
            self.block_table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(block.occupied)))
            self.block_table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(block.maintenance)))

            self.block_table_test_bench.setItem(index, 0, QtWidgets.QTableWidgetItem(str(block.block_number)))
            self.block_table_test_bench.setItem(index, 1, QtWidgets.QTableWidgetItem(str(block.section)))
            self.block_table_test_bench.setItem(index, 2, QtWidgets.QTableWidgetItem(str(block.occupied)))
            self.block_table_test_bench.setItem(index, 3, QtWidgets.QTableWidgetItem(str(block.maintenance)))
            if block.switch_positions:
                self.block_table_test_bench.setItem(index, 4, QtWidgets.QTableWidgetItem(str(block.switch_positions[block.curr_switch_position])))
            else:
                self.block_table_test_bench.setItem(index, 4, QtWidgets.QTableWidgetItem(""))

            for col in range(4):
                item1 = self.block_table.item(index, col)
                item1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            for col2 in range(5):
                item2 = self.block_table_test_bench.item(index, col2)
                item2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        headers = ["Block #", "Section ID", "Occupied", "Maintenance"]
        for col, header in enumerate(headers):
            item = self.block_table.horizontalHeaderItem(col)
            if item is None:
                item = QtWidgets.QTableWidgetItem()
                self.block_table.setHorizontalHeaderItem(col, item)
            _translate = QtCore.QCoreApplication.translate
            item.setText(_translate("mainwindow", header))

        headers = ["Block #", "Section ID", "Occupied", "Maintenance Mode", "Switch State"]
        for col, header in enumerate(headers):
            item = self.block_table_test_bench.horizontalHeaderItem(col)
            if item is None:
                item = QtWidgets.QTableWidgetItem()
                self.block_table_test_bench.setHorizontalHeaderItem(col, item)
            _translate = QtCore.QCoreApplication.translate
            item.setText(_translate("mainwindow", header))

        if self.ctc.line.layout:
            self.block_page_block_selector.setRange(0, len(self.ctc.line.layout)-1)
            self.spinBox.setRange(0, len(self.ctc.line.layout)-1)
        else:
            self.block_page_block_selector.setRange(0, 0)
            self.spinBox.setRange(0, 0)

        if self.ctc.num_trains > 0:
            self.train_number_selector.setRange(1, self.ctc.num_trains)
            self.Train_view_train_selector.setRange(1, self.ctc.num_trains)
        else:
            self.train_number_selector.setRange(1, 1)
            self.Train_view_train_selector.setRange(1, 1)

        if len(self.ctc.line.train_list):
            
            train_index = [train.train_id for train in self.ctc.line.train_list].index(self.train_number_selector.value())
            self.suggested_speed_display.setText(str(self.ctc.line.train_list[train_index].suggested_speed))
            self.authority_display.setText(str(self.ctc.line.train_list[train_index].authority))

            selector_index = [train.train_id for train in self.ctc.line.train_list].index(self.Train_view_train_selector.value())
            self.destination_list.clear()
            self.destination_list.addItems(self.ctc.line.train_list[selector_index].destination_strings)


    def update_block_occupancies(self, blocks: list):
        # Connected to CTC-Wayside Communication - gets block occupancies from signal

        # Updates Block Occupancies and Updates: Train Locations, Authorities, Speeds, Throughput
        self.ctc.update_blocks_on_line(blocks)

        # Time based updates
        self.check_departures()

        # Once calculations have been made, update the UI
        self.updateUI()

    def dispatch_train(self):

        if self.ctc.automatic:
            return

        station_name = self.StationSelector.currentText()
        # print(f"Selected Station = {station}")

        #print(f"Selected Station = {station_name}")

        station_names = [station[0] for station in self.stations]

        #print(f"Station Names = {station_names}")

        if station_names.count(station_name) > 1:
            #print("MULTIPLE STATIONS")
            indicies = [index for index, _ in enumerate(self.stations) if _[0] == station_name]
            #print(f"Indicies = {indicies}")
            if self.stations[indicies[0]][1] != self.stations[indicies[1]][1]:
                # multiple blocks with the same station
                destination = self.stations[self.StationSelector.currentIndex()][1]
                #print("MULTIPLE BLOCKS SAME DESTINATION")
            else: 
                # one block that is traversed twice
                destination = self.stations[indicies[0]][1]
                #print("ONE BLOCK TRAVERSED TWICE")

                if self.StationSelector.currentIndex() > indicies[0]:
                    # second instance of station
                    #print("SECOND INSTANCE")
                    destination *= -1
        else:
            destination = self.ctc.find_destination(station_name)
            
        arrival_time = self.ArrivalSelector.time()
        arrive_time = dt.time(hour=arrival_time.hour(),minute=arrival_time.minute(),second=0)
            
        # Dispatch immediately if departure time is current time
        #if self.departure_ready(destination):
        #    self.ctc.add_new_train_to_line(destination, arrive_time, station_name)

        # Otherwise, add to pending dispatches
        #else:
        self.ctc.add_new_pending_train(destination, arrive_time, station_name)


        self.ctc_train_communicate.dispatch_train_signal.emit(self.ctc.num_trains)

        #self.updateUI()

    def check_departures(self):
        for train in self.ctc.line.pending_trains:
            if self.departure_ready(train.train_id):
                self.ctc.dispatch_pending_train(train.train_id)
                print(f"Dispatching Scheduled Train {train.train_id}")
                print(f"Num Trains = {self.ctc.num_trains}")
                self.ctc_train_communicate.dispatch_train_signal.emit(self.ctc.num_trains)

    #def departure_ready(self, curr, depart):
        #if curr.hour >= depart.hour and curr.minute >= depart.minute:
        #    return True
        #else:
        #    return False
        
    def departure_ready(self, train_id):
        train_index = [train.train_id for train in self.ctc.line.pending_trains].index(train_id)
        # Departure is ready if the arrival time < current_time + time to reach destination
        time_to_reach_destination = self.ctc.line.arrival_time_between(0, self.ctc.line.pending_trains[train_index].destinations[0])

        curr_time = dt.datetime.combine(dt.date.today(), self.current_time)
        time = (curr_time + dt.timedelta(seconds=time_to_reach_destination)).time()
        #print("Train Arrival Time = ", self.ctc.line.pending_trains[train_index].arrival_times[0])
        #print("Time to be able to reach destination = ", time)
        #print("Current Time = ", curr_time.time())
        if self.ctc.line.pending_trains[train_index].arrival_times[0].hour <= time.hour and self.ctc.line.pending_trains[train_index].arrival_times[0].minute <= time.minute:
            return True
        else:
            return False

        
    def remove_train(self, train_id):
        self.ctc.remove_train_from_line(train_id)
        self.updateUI()
           
    def add_destination(self):

        if self.ctc.automatic:
            return

        station_name = self.StationSelector.currentText()

        station_names = [station[0] for station in self.stations]

        if station_names.count(station_name) > 1:
            #print("MULTIPLE STATIONS")
            indicies = [index for index, _ in enumerate(self.stations) if _[0] == station_name]
            #print(f"Indicies = {indicies}")
            if self.stations[indicies[0]][1] != self.stations[indicies[1]][1]:
                # multiple blocks with the same station
                destination = self.stations[self.StationSelector.currentIndex()][1]
                #print("MULTIPLE BLOCKS SAME DESTINATION")
            else: 
                # one block that is traversed twice
                destination = self.stations[indicies[0]][1]
                #print("ONE BLOCK TRAVERSED TWICE")

                if self.StationSelector.currentIndex() > indicies[0]:
                    # second instance of station
                    #print("SECOND INSTANCE")
                    destination *= -1
        else:
            destination = self.ctc.find_destination(station_name)
            

        train_id = self.Train_view_train_selector.value()
        arrival_time = self.ArrivalSelector.time()
        arrival_time_formatted = dt.time(hour=arrival_time.hour(),minute=arrival_time.minute(),second=arrival_time.second())
        
        self.ctc.add_train_destination_on_line(train_id, destination, arrival_time_formatted, station_name)
        self.updateUI()

    def select_block(self):
        self.selected_block = self.block_page_block_selector.value()

    def select_train(self):
        self.selected_train = self.Train_view_train_selector.value()
    
    def maintenance_mode(self):
        self.ctc.toggle_maintenance_mode()
        if self.ctc.maintenance_mode:
            self.MaintenanceButton.setText("Exit Maintenance Mode")
        else:
            self.MaintenanceButton.setText("Enter Maintenance Mode")

    def toggle_block_maintenance(self):
        if self.ctc.maintenance_mode:
            self.ctc.select_line_for_maintenance(self.selected_block)
            self.updateUI()
    
    def auto_manual_toggle(self):
        self.ctc.toggle_automatic_manual()
        _translate = QtCore.QCoreApplication.translate
        if self.ctc.automatic:
            self.automatic_manual_toggle.setText(_translate("mainwindow", "Manual Mode"))
            #TODO - Disable UI Elements only available in Manual Mode
            self.add_destination_button.setEnabled(False)
            self.add_destination_button.setStyleSheet("background-color: lightgray;\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
            self.DispatchButton.setEnabled(False)
            self.DispatchButton.setStyleSheet("background-color: lightgray;\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
            self.UploadScheduleButton.setEnabled(True)
            self.UploadScheduleButton.setStyleSheet("background-color: rgb(230, 0, 230);\n"
"border: 1px solid;\n"
"font: 18pt \"Arial\";\n"
"\n"
"color:black;")
           

        else:
            self.automatic_manual_toggle.setText(_translate("mainwindow", "Auto Mode"))
            #TODO - Enable UI Elements only available in Manual Mode
            self.add_destination_button.setEnabled(True)
            self.add_destination_button.setStyleSheet("background-color: rgb(133, 239, 128);\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
            self.DispatchButton.setEnabled(True)
            self.DispatchButton.setStyleSheet("background-color: rgb(70, 158, 49);\n"
"font: 18pt \"Arial\";\n"
"border: 1px solid;\n"
"color:black;")
            self.UploadScheduleButton.setEnabled(False)
            self.UploadScheduleButton.setStyleSheet("background-color: lightgray;\n"
"border: 1px solid;\n"
"font: 18pt \"Arial\";\n"
"\n"
"color:black;")

    
    def upload_schedule(self):
        if self.ctc.automatic:
            filename,_ = QFileDialog.getOpenFileName(None, "Select Schedule File", os.getcwd(), "Excel File (*.xlsx *.xls)")
            if filename:
                self.ctc.upload_schedule_to_line(filename, self.current_time)
                self.updateUI()
    
    def upload_layout(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Select Layout File", os.getcwd(), "Excel File (*.xlsx *.xls)")
        if filename:
        #     print("filename = ", filename)
            self.ctc.upload_layout_to_line(filename)

        # Update Lines Selector
        self.LineSelectorComboBox.clear()
        self.LineSelectorComboBox.addItem("Green")

        # Update Station Selector
        self.StationSelector.clear()
        self.stations = self.ctc.get_stations()
        print("Stations = ", self.stations)
        self.StationSelector.addItems([station[0] for station in self.stations])

        self.updateUI()

    def time_step(self, elapsed_seconds):
        self.current_time = (self.start_time + dt.timedelta(seconds=elapsed_seconds)).time()


if __name__ == "__main__":
    
    """"Main"""
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    comm = CTCTrain()
    comm2 = CTCWaysideControllerComm()

    ui = CTC_frontend(comm, comm2)
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec())