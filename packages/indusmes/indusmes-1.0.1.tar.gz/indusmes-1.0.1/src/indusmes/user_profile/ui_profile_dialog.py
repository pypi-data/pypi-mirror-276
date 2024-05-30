# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_profile_dialog(object):
    def setupUi(self, profile_dialog):
        if not profile_dialog.objectName():
            profile_dialog.setObjectName(u"profile_dialog")
        profile_dialog.setWindowModality(Qt.ApplicationModal)
        profile_dialog.resize(404, 500)
        profile_dialog.setSizeGripEnabled(False)
        profile_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(profile_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(profile_dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.user_name_label = QLabel(self.widget)
        self.user_name_label.setObjectName(u"user_name_label")
        self.user_name_label.setMinimumSize(QSize(80, 40))
        self.user_name_label.setMaximumSize(QSize(80, 40))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(16)
        self.user_name_label.setFont(font)

        self.horizontalLayout.addWidget(self.user_name_label)

        self.user_name_text = QLabel(self.widget)
        self.user_name_text.setObjectName(u"user_name_text")
        self.user_name_text.setMinimumSize(QSize(280, 40))
        self.user_name_text.setMaximumSize(QSize(280, 40))
        self.user_name_text.setFont(font)
        self.user_name_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.user_name_text.setMargin(4)

        self.horizontalLayout.addWidget(self.user_name_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.logout_button = QPushButton(self.widget)
        self.logout_button.setObjectName(u"logout_button")
        self.logout_button.setMinimumSize(QSize(0, 60))
        self.logout_button.setMaximumSize(QSize(16777215, 60))
        self.logout_button.setFont(font)
        self.logout_button.setStyleSheet(u"background-color: rgb(28, 113, 216);")

        self.verticalLayout_2.addWidget(self.logout_button)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(profile_dialog)

        QMetaObject.connectSlotsByName(profile_dialog)
    # setupUi

    def retranslateUi(self, profile_dialog):
        profile_dialog.setWindowTitle(QCoreApplication.translate("profile_dialog", u"Profile Section", None))
        self.user_name_label.setText(QCoreApplication.translate("profile_dialog", u"Name:", None))
        self.user_name_text.setText("")
        self.logout_button.setText(QCoreApplication.translate("profile_dialog", u"Logout", None))
    # retranslateUi

