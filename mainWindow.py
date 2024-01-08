# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1420, 882)
        mainWindow.setMinimumSize(QtCore.QSize(1420, 874))
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(268, 0))
        self.frame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(58, 25))
        self.label.setMaximumSize(QtCore.QSize(158, 16))
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_4.setMidLineWidth(1)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_4)
        self.tabWidget.setObjectName("tabWidget")
        self.video_tab = QtWidgets.QWidget()
        self.video_tab.setObjectName("video_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.video_tab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.video_tree_widget = QtWidgets.QTreeWidget(self.video_tab)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        self.video_tree_widget.setFont(font)
        self.video_tree_widget.setObjectName("video_tree_widget")
        self.video_tree_widget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.video_tree_widget.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.video_tree_widget.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.video_tree_widget.headerItem().setTextAlignment(3, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.video_tree_widget.header().setCascadingSectionResizes(False)
        self.video_tree_widget.header().setStretchLastSection(False)
        self.verticalLayout_5.addWidget(self.video_tree_widget)
        self.tabWidget.addTab(self.video_tab, "")
        self.picture_tab = QtWidgets.QWidget()
        self.picture_tab.setObjectName("picture_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.picture_tab)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.picture_tree_widget = QtWidgets.QTreeWidget(self.picture_tab)
        self.picture_tree_widget.setObjectName("picture_tree_widget")
        self.picture_tree_widget.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.picture_tree_widget.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.picture_tree_widget.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.picture_tree_widget.headerItem().setTextAlignment(3, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.picture_tree_widget.header().setStretchLastSection(False)
        self.verticalLayout_7.addWidget(self.picture_tree_widget)
        self.tabWidget.addTab(self.picture_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addButton = QtWidgets.QPushButton(self.frame_4)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QPushButton(self.frame_4)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_2.addWidget(self.deleteButton)
        self.clearButton = QtWidgets.QPushButton(self.frame_4)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_2.addWidget(self.clearButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_8.addWidget(self.frame_4)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(81, 25))
        self.label_2.setMaximumSize(QtCore.QSize(181, 16))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_8.addWidget(self.label_2)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_5.setMidLineWidth(1)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        self.label_3.setMinimumSize(QtCore.QSize(141, 16))
        self.label_3.setMaximumSize(QtCore.QSize(290, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 38, 0)")
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.treeWidget_5 = QtWidgets.QTreeWidget(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        self.treeWidget_5.setFont(font)
        self.treeWidget_5.setObjectName("treeWidget_5")
        self.treeWidget_5.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeWidget_5.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeWidget_5.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeWidget_5.headerItem().setTextAlignment(3, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeWidget_5.header().setCascadingSectionResizes(False)
        self.treeWidget_5.header().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.treeWidget_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.pushButton = QtWidgets.QPushButton(self.frame_5)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_13.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_13.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_13.addWidget(self.pushButton_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_13)
        self.verticalLayout_8.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(640, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setMidLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setMinimumSize(QtCore.QSize(58, 25))
        self.label_7.setMaximumSize(QtCore.QSize(158, 16))
        self.label_7.setObjectName("label_7")
        self.verticalLayout_11.addWidget(self.label_7)
        self.frame_9 = QtWidgets.QFrame(self.frame_2)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_9.setMidLineWidth(1)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.picture_label = QtWidgets.QLabel(self.frame_9)
        self.picture_label.setMinimumSize(QtCore.QSize(640, 480))
        self.picture_label.setStyleSheet("QLabel {  \n"
"    background-color: black;  \n"
"}")
        self.picture_label.setText("")
        self.picture_label.setObjectName("picture_label")
        self.verticalLayout_10.addWidget(self.picture_label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_9)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_3.addWidget(self.checkBox_2)
        self.pushButton_15 = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_15.setObjectName("pushButton_15")
        self.horizontalLayout_3.addWidget(self.pushButton_15)
        self.verticalLayout_10.addLayout(self.horizontalLayout_3)
        self.verticalLayout_11.addWidget(self.frame_9)
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setMinimumSize(QtCore.QSize(81, 40))
        self.label_11.setMaximumSize(QtCore.QSize(181, 16))
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 196))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_6.setMidLineWidth(1)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.checkBox = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox.setMinimumSize(QtCore.QSize(101, 20))
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_14.addWidget(self.checkBox)
        self.comboBox = QtWidgets.QComboBox(self.frame_6)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_14.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem)
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_6)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_14.addWidget(self.checkBox_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_12 = QtWidgets.QLabel(self.frame_6)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame_6)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_4.addWidget(self.lineEdit_4)
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_6)
        self.pushButton_7.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_4.addWidget(self.pushButton_7)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_6)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_5.addWidget(self.pushButton_8)
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_6)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_5.addWidget(self.pushButton_9)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.label_14 = QtWidgets.QLabel(self.frame_6)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("color: rgb(255, 38, 0)")
        self.label_14.setObjectName("label_14")
        self.verticalLayout_9.addWidget(self.label_14)
        self.progressBar = QtWidgets.QProgressBar(self.frame_6)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_9.addWidget(self.progressBar)
        self.verticalLayout_11.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(450, 0))
        self.frame_3.setMaximumSize(QtCore.QSize(450, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setMidLineWidth(1)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setMinimumSize(QtCore.QSize(58, 25))
        self.label_9.setMaximumSize(QtCore.QSize(158, 16))
        self.label_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_14.addWidget(self.label_9)
        self.player = VideoPlayer(self.frame_3)
        self.player.setMinimumSize(QtCore.QSize(0, 376))
        self.player.setMaximumSize(QtCore.QSize(16777215, 398))
        self.player.setStyleSheet("QWidget {  \n"
"    background-color: black;  \n"
"}")
        self.player.setObjectName("player")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.player)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_14.addWidget(self.player)
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 74))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_7.setMidLineWidth(1)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_15 = QtWidgets.QLabel(self.frame_7)
        self.label_15.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_7.addWidget(self.label_15)
        self.spinBox = QtWidgets.QSpinBox(self.frame_7)
        self.spinBox.setMaximumSize(QtCore.QSize(45, 16777215))
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_7.addWidget(self.spinBox)
        self.label_16 = QtWidgets.QLabel(self.frame_7)
        self.label_16.setMinimumSize(QtCore.QSize(111, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 38, 0)")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_7.addWidget(self.label_16)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_6.addWidget(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_6.addWidget(self.pushButton_11)
        self.pushButton_12 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_6.addWidget(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_6.addWidget(self.pushButton_13)
        self.pushButton_14 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_6.addWidget(self.pushButton_14)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.verticalLayout_14.addWidget(self.frame_7)
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setMinimumSize(QtCore.QSize(58, 40))
        self.label_17.setMaximumSize(QtCore.QSize(158, 16))
        self.label_17.setObjectName("label_17")
        self.verticalLayout_14.addWidget(self.label_17)
        self.frame_8 = QtWidgets.QFrame(self.frame_3)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 140))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_8.setMidLineWidth(1)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_18 = QtWidgets.QLabel(self.frame_8)
        self.label_18.setMaximumSize(QtCore.QSize(40, 20))
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_8.addWidget(self.label_18)
        self.frameLineEdit = QtWidgets.QLineEdit(self.frame_8)
        self.frameLineEdit.setObjectName("frameLineEdit")
        self.horizontalLayout_8.addWidget(self.frameLineEdit)
        self.label_20 = QtWidgets.QLabel(self.frame_8)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_8.addWidget(self.label_20)
        self.deepLineEdit = QtWidgets.QLineEdit(self.frame_8)
        self.deepLineEdit.setObjectName("deepLineEdit")
        self.horizontalLayout_8.addWidget(self.deepLineEdit)
        self.pushButton_16 = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_16.setObjectName("pushButton_16")
        self.horizontalLayout_8.addWidget(self.pushButton_16)
        self.verticalLayout_12.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_22 = QtWidgets.QLabel(self.frame_8)
        self.label_22.setMaximumSize(QtCore.QSize(60, 20))
        self.label_22.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_9.addWidget(self.label_22)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_8)
        self.lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_9.addWidget(self.lineEdit)
        self.pushButton_17 = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_17.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton_17.setObjectName("pushButton_17")
        self.horizontalLayout_9.addWidget(self.pushButton_17)
        self.label_24 = QtWidgets.QLabel(self.frame_8)
        self.label_24.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_9.addWidget(self.label_24)
        self.verticalLayout_12.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_15.addWidget(self.label_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame_8)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_15.addWidget(self.lineEdit_5)
        self.label_5 = QtWidgets.QLabel(self.frame_8)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame_8)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_15.addWidget(self.lineEdit_6)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem4)
        self.verticalLayout_12.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_16.addWidget(self.pushButton_4)
        self.label_6 = QtWidgets.QLabel(self.frame_8)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_16.addWidget(self.label_6)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_16.addWidget(self.pushButton_5)
        self.label_8 = QtWidgets.QLabel(self.frame_8)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_16.addWidget(self.label_8)
        self.verticalLayout_12.addLayout(self.horizontalLayout_16)
        self.verticalLayout_14.addWidget(self.frame_8)
        self.label_25 = QtWidgets.QLabel(self.frame_3)
        self.label_25.setMinimumSize(QtCore.QSize(58, 40))
        self.label_25.setMaximumSize(QtCore.QSize(158, 16))
        self.label_25.setObjectName("label_25")
        self.verticalLayout_14.addWidget(self.label_25)
        self.frame_11 = QtWidgets.QFrame(self.frame_3)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_11.setMidLineWidth(1)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout_11.setSpacing(5)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_26 = QtWidgets.QLabel(self.frame_11)
        self.label_26.setMaximumSize(QtCore.QSize(105, 16777215))
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_11.addWidget(self.label_26)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_11)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_11.addWidget(self.lineEdit_2)
        self.pushButton_18 = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_18.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_18.setObjectName("pushButton_18")
        self.horizontalLayout_11.addWidget(self.pushButton_18)
        self.label_28 = QtWidgets.QLabel(self.frame_11)
        self.label_28.setMinimumSize(QtCore.QSize(111, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("color: rgb(255, 38, 0)")
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_11.addWidget(self.label_28)
        self.verticalLayout_13.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(5)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_29 = QtWidgets.QLabel(self.frame_11)
        self.label_29.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_12.addWidget(self.label_29)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_11)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_12.addWidget(self.lineEdit_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.verticalLayout_13.addLayout(self.horizontalLayout_12)
        self.label_31 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("color: rgb(255, 38, 0)")
        self.label_31.setObjectName("label_31")
        self.verticalLayout_13.addWidget(self.label_31)
        self.progressBar_2 = QtWidgets.QProgressBar(self.frame_11)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.verticalLayout_13.addWidget(self.progressBar_2)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pushButton_20 = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_20.setObjectName("pushButton_20")
        self.horizontalLayout_10.addWidget(self.pushButton_20)
        self.pushButton_19 = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_19.setObjectName("pushButton_19")
        self.horizontalLayout_10.addWidget(self.pushButton_19)
        self.verticalLayout_13.addLayout(self.horizontalLayout_10)
        self.verticalLayout_14.addWidget(self.frame_11)
        self.horizontalLayout.addWidget(self.frame_3)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "井下电视图像深度校准工具 V1.0"))
        self.label.setText(_translate("mainWindow", "文件列表"))
        self.video_tree_widget.headerItem().setText(0, _translate("mainWindow", "序号"))
        self.video_tree_widget.headerItem().setText(1, _translate("mainWindow", "文件名称"))
        self.video_tree_widget.headerItem().setText(2, _translate("mainWindow", "文件大小"))
        self.video_tree_widget.headerItem().setText(3, _translate("mainWindow", "文件位置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.video_tab), _translate("mainWindow", "视频"))
        self.picture_tree_widget.headerItem().setText(0, _translate("mainWindow", "序号"))
        self.picture_tree_widget.headerItem().setText(1, _translate("mainWindow", "文件名称"))
        self.picture_tree_widget.headerItem().setText(2, _translate("mainWindow", "文件大小"))
        self.picture_tree_widget.headerItem().setText(3, _translate("mainWindow", "文件位置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.picture_tab), _translate("mainWindow", "图片"))
        self.addButton.setText(_translate("mainWindow", "添加"))
        self.deleteButton.setText(_translate("mainWindow", "删除"))
        self.clearButton.setText(_translate("mainWindow", "清空"))
        self.label_2.setText(_translate("mainWindow", "接箍位置列表"))
        self.label_3.setText(_translate("mainWindow", "列表中选中的文件名称"))
        self.treeWidget_5.headerItem().setText(0, _translate("mainWindow", "序号"))
        self.treeWidget_5.headerItem().setText(1, _translate("mainWindow", "帧号"))
        self.treeWidget_5.headerItem().setText(2, _translate("mainWindow", "帧间隔"))
        self.treeWidget_5.headerItem().setText(3, _translate("mainWindow", "深度"))
        self.pushButton.setText(_translate("mainWindow", "重新排序"))
        self.pushButton_2.setText(_translate("mainWindow", "删除选中行"))
        self.pushButton_3.setText(_translate("mainWindow", "导出"))
        self.label_7.setText(_translate("mainWindow", "图片预览"))
        self.checkBox_2.setText(_translate("mainWindow", "启用图像增强"))
        self.pushButton_15.setText(_translate("mainWindow", "保存"))
        self.label_11.setText(_translate("mainWindow", "视频叠加深度"))
        self.checkBox.setText(_translate("mainWindow", "图像增强叠加"))
        self.comboBox.setItemText(0, _translate("mainWindow", "ESPCN_x2"))
        self.comboBox.setItemText(1, _translate("mainWindow", "ESPCN_x3"))
        self.comboBox.setItemText(2, _translate("mainWindow", "ESPCN_x4"))
        self.comboBox.setItemText(3, _translate("mainWindow", "CUBIC_x2"))
        self.comboBox.setItemText(4, _translate("mainWindow", "CUBIC_x3"))
        self.comboBox.setItemText(5, _translate("mainWindow", "CUBIC_x4"))
        self.checkBox_3.setText(_translate("mainWindow", "全部"))
        self.label_12.setText(_translate("mainWindow", "叠加文件输出位置："))
        self.pushButton_7.setText(_translate("mainWindow", "..."))
        self.pushButton_8.setText(_translate("mainWindow", "开始"))
        self.pushButton_9.setText(_translate("mainWindow", "暂停"))
        self.label_14.setText(_translate("mainWindow", "文件 进度 0%"))
        self.label_9.setText(_translate("mainWindow", "视频预览"))
        self.label_15.setText(_translate("mainWindow", "倍速"))
        self.label_16.setText(_translate("mainWindow", "当前播放帧号 0 总帧数 0"))
        self.pushButton_10.setText(_translate("mainWindow", "播放"))
        self.pushButton_11.setText(_translate("mainWindow", "暂停"))
        self.pushButton_12.setText(_translate("mainWindow", "步进"))
        self.pushButton_13.setText(_translate("mainWindow", "步退"))
        self.pushButton_14.setText(_translate("mainWindow", "倒放"))
        self.label_17.setText(_translate("mainWindow", "接箍对深"))
        self.label_18.setText(_translate("mainWindow", "帧号"))
        self.label_20.setText(_translate("mainWindow", "深度"))
        self.pushButton_16.setText(_translate("mainWindow", "添加"))
        self.label_22.setText(_translate("mainWindow", "跳帧到"))
        self.pushButton_17.setText(_translate("mainWindow", "查找"))
        self.label_24.setText(_translate("mainWindow", "已添加接箍数0"))
        self.label_4.setText(_translate("mainWindow", "x"))
        self.label_5.setText(_translate("mainWindow", "y"))
        self.pushButton_4.setText(_translate("mainWindow", "背景颜色"))
        self.label_6.setText(_translate("mainWindow", "#000000"))
        self.pushButton_5.setText(_translate("mainWindow", "字体颜色"))
        self.label_8.setText(_translate("mainWindow", "#FFFFFF"))
        self.label_25.setText(_translate("mainWindow", "接箍预览"))
        self.label_26.setText(_translate("mainWindow", "接箍号跳转到"))
        self.pushButton_18.setText(_translate("mainWindow", "查找"))
        self.label_28.setText(_translate("mainWindow", "当前接箍号 0 深度 0 M"))
        self.label_29.setText(_translate("mainWindow", "预览速度/间隔(秒)"))
        self.label_31.setText(_translate("mainWindow", "当前接箍编号 0 接箍总数 0"))
        self.pushButton_20.setText(_translate("mainWindow", "从头开始"))
        self.pushButton_19.setText(_translate("mainWindow", "暂停/继续"))
from QT5_VideoPlayer import VideoPlayer