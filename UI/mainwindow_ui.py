# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle("AREA")
        MainWindow.setToolTip("")
        MainWindow.setStyleSheet("QDialog{\n"
"background-color: rgb(254, 254, 254);\n"
"}\n"
"/* Панель заголовка */\n"
"TitleBar {\n"
"    background-color: rgb(32, 178, 170);\n"
"}\n"
"/* Минимизировать кнопку `Максимальное выключение` Общий фон по умолчанию */\n"
"#buttonMinimum, #buttonMaximum, #buttonClose, #buttonConnect {\n"
"    border: none;\n"
"    background-color: rgb(32, 178, 170);\n"
"    color: white;\n"
"}\n"
"/* Зависание */\n"
"#buttonMinimum:hover,#buttonMaximum:hover, #buttonConnect:hover {\n"
"    color: rgb(32, 178, 170);\n"
"    background-color: rgb(41, 229, 217);\n"
"}\n"
"#buttonClose:hover {\n"
"    color: rgb(32, 178, 170);\n"
"    background-color: rgb(41, 229, 217);\n"
"}\n"
"/* Мышь удерживать */\n"
"#buttonMinimum:pressed,#buttonMaximum:pressed {\n"
"    background-color: rgb(44, 125, 144);\n"
"}\n"
"#buttonClose:pressed {\n"
"    color: white;\n"
"    background-color: rgb(161, 73, 92);\n"
"}")
        MainWindow.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.header = TitleBar(MainWindow)
        self.header.setMinimumSize(QtCore.QSize(0, 30))
        self.header.setObjectName("header")
        self.horizontalLayout_4.addWidget(self.header)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 9)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo_label = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_label.sizePolicy().hasHeightForWidth())
        self.logo_label.setSizePolicy(sizePolicy)
        self.logo_label.setMinimumSize(QtCore.QSize(60, 60))
        self.logo_label.setMaximumSize(QtCore.QSize(60, 60))
        self.logo_label.setStyleSheet("")
        self.logo_label.setText("")
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.horizontalLayout_2.addWidget(self.logo_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.main_label_2 = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label_2.sizePolicy().hasHeightForWidth())
        self.main_label_2.setSizePolicy(sizePolicy)
        self.main_label_2.setStyleSheet("QLabel {\n"
"font: 75 20pt \"IBM Plex Sans\";\n"
"}")
        self.main_label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.main_label_2.setObjectName("main_label_2")
        self.horizontalLayout_2.addWidget(self.main_label_2)
        self.main_label = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        self.main_label.setStyleSheet("QLabel {\n"
"font: 75 20pt \"IBM Plex Sans\";\n"
"}")
        self.main_label.setText("")
        self.main_label.setTextFormat(QtCore.Qt.AutoText)
        self.main_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.main_label.setObjectName("main_label")
        self.horizontalLayout_2.addWidget(self.main_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.quit_btn = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quit_btn.sizePolicy().hasHeightForWidth())
        self.quit_btn.setSizePolicy(sizePolicy)
        self.quit_btn.setMinimumSize(QtCore.QSize(150, 40))
        self.quit_btn.setStyleSheet("QPushButton {\n"
"font: 57 14pt \"IBM Plex Sans\";\n"
"    color: rgb(254, 254, 254);\n"
"background-color: rgb(60, 78, 68);\n"
"border-radius: 20px;\n"
"}")
        self.quit_btn.setObjectName("quit_btn")
        self.horizontalLayout_2.addWidget(self.quit_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.calendar_2 = Calendar(MainWindow)
        self.calendar_2.setStyleSheet("QCalnedarWidget {\n"
"color: rgb(0, 170, 0);}")
        self.calendar_2.setGridVisible(True)
        self.calendar_2.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendar_2.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar_2.setDateEditEnabled(True)
        self.calendar_2.setObjectName("calendar_2")
        self.horizontalLayout_3.addWidget(self.calendar_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tasks_label_2 = QtWidgets.QLabel(MainWindow)
        self.tasks_label_2.setStyleSheet("QLabel {\n"
"font: 75 14pt \"IBM Plex Sans\";\n"
"}")
        self.tasks_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.tasks_label_2.setObjectName("tasks_label_2")
        self.verticalLayout_3.addWidget(self.tasks_label_2)
        self.tasks_list_2 = QtWidgets.QListWidget(MainWindow)
        self.tasks_list_2.setObjectName("tasks_list_2")
        self.verticalLayout_3.addWidget(self.tasks_list_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_task_btn = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_task_btn.sizePolicy().hasHeightForWidth())
        self.add_task_btn.setSizePolicy(sizePolicy)
        self.add_task_btn.setMinimumSize(QtCore.QSize(181, 50))
        self.add_task_btn.setStyleSheet("QPushButton {\n"
"background-color: rgb(136, 89, 84);\n"
"color: rgb(254, 254, 254);\n"
"border-radius: 20px;\n"
"font: 57 14pt \"IBM Plex Sans\";\n"
"}")
        self.add_task_btn.setObjectName("add_task_btn")
        self.horizontalLayout.addWidget(self.add_task_btn)
        self.add_task_btn_2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_task_btn_2.sizePolicy().hasHeightForWidth())
        self.add_task_btn_2.setSizePolicy(sizePolicy)
        self.add_task_btn_2.setMinimumSize(QtCore.QSize(181, 50))
        self.add_task_btn_2.setStyleSheet("QPushButton {\n"
"font: 57 14pt \"IBM Plex Sans\";\n"
"background-color: rgb(61, 79, 69);\n"
"color: rgb(254, 254, 254);\n"
"border-radius: 20px;\n"
"}")
        self.add_task_btn_2.setObjectName("add_task_btn_2")
        self.horizontalLayout.addWidget(self.add_task_btn_2)
        self.give_task_btn = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.give_task_btn.sizePolicy().hasHeightForWidth())
        self.give_task_btn.setSizePolicy(sizePolicy)
        self.give_task_btn.setMinimumSize(QtCore.QSize(151, 50))
        self.give_task_btn.setStyleSheet("QPushButton {\n"
"background-color: rgb(71, 118, 93);\n"
"color: rgb(254, 254, 254);\n"
"border-radius: 20px;\n"
"font: 57 14pt \"IBM Plex Sans\";\n"
"}")
        self.give_task_btn.setObjectName("give_task_btn")
        self.horizontalLayout.addWidget(self.give_task_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.main_label_2.setText(_translate("MainWindow", "AREA"))
        self.quit_btn.setText(_translate("MainWindow", "Выйти"))
        self.tasks_label_2.setText(_translate("MainWindow", "Задания"))
        self.add_task_btn.setText(_translate("MainWindow", "Добавить задание"))
        self.add_task_btn_2.setText(_translate("MainWindow", "Изменить задание"))
        self.give_task_btn.setText(_translate("MainWindow", "Сдать задание"))
from redefined_widgets import Calendar, TitleBar
