# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        if not settings_dialog.objectName():
            settings_dialog.setObjectName(u"settings_dialog")
        settings_dialog.setWindowModality(Qt.ApplicationModal)
        settings_dialog.resize(400, 600)
        settings_dialog.setMinimumSize(QSize(400, 600))
        settings_dialog.setMaximumSize(QSize(400, 600))
        self.verticalLayout = QVBoxLayout(settings_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(settings_dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 0, 8, 16)
        self.site_name_label = QLabel(self.widget)
        self.site_name_label.setObjectName(u"site_name_label")
        self.site_name_label.setMinimumSize(QSize(380, 0))
        self.site_name_label.setMaximumSize(QSize(5000, 5000))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(12)
        self.site_name_label.setFont(font)
        self.site_name_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.site_name_label)

        self.site_name_text = QLineEdit(self.widget)
        self.site_name_text.setObjectName(u"site_name_text")
        self.site_name_text.setMinimumSize(QSize(380, 30))
        self.site_name_text.setMaximumSize(QSize(5000, 30))
        self.site_name_text.setFont(font)
        self.site_name_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.site_name_text)

        self.asset_id_label = QLabel(self.widget)
        self.asset_id_label.setObjectName(u"asset_id_label")
        self.asset_id_label.setMinimumSize(QSize(380, 0))
        self.asset_id_label.setMaximumSize(QSize(5000, 30))
        self.asset_id_label.setFont(font)
        self.asset_id_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.asset_id_label)

        self.asset_id_text = QLineEdit(self.widget)
        self.asset_id_text.setObjectName(u"asset_id_text")
        self.asset_id_text.setMinimumSize(QSize(380, 30))
        self.asset_id_text.setMaximumSize(QSize(5000, 30))
        self.asset_id_text.setFont(font)
        self.asset_id_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.asset_id_text)

        self.device_id_label = QLabel(self.widget)
        self.device_id_label.setObjectName(u"device_id_label")
        self.device_id_label.setMinimumSize(QSize(380, 0))
        self.device_id_label.setMaximumSize(QSize(5000, 30))
        self.device_id_label.setFont(font)
        self.device_id_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.device_id_label)

        self.device_id_text = QLineEdit(self.widget)
        self.device_id_text.setObjectName(u"device_id_text")
        self.device_id_text.setMinimumSize(QSize(380, 30))
        self.device_id_text.setMaximumSize(QSize(5000, 30))
        self.device_id_text.setFont(font)
        self.device_id_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.device_id_text)

        self.ct_sensitivity_label = QLabel(self.widget)
        self.ct_sensitivity_label.setObjectName(u"ct_sensitivity_label")
        self.ct_sensitivity_label.setMinimumSize(QSize(380, 0))
        self.ct_sensitivity_label.setMaximumSize(QSize(5000, 30))
        self.ct_sensitivity_label.setFont(font)
        self.ct_sensitivity_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.ct_sensitivity_label)

        self.ct_sensitivity_text = QLineEdit(self.widget)
        self.ct_sensitivity_text.setObjectName(u"ct_sensitivity_text")
        self.ct_sensitivity_text.setMinimumSize(QSize(380, 30))
        self.ct_sensitivity_text.setMaximumSize(QSize(5000, 30))
        self.ct_sensitivity_text.setFont(font)
        self.ct_sensitivity_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.ct_sensitivity_text)

        self.idle_current_threshold_label = QLabel(self.widget)
        self.idle_current_threshold_label.setObjectName(u"idle_current_threshold_label")
        self.idle_current_threshold_label.setMinimumSize(QSize(380, 0))
        self.idle_current_threshold_label.setMaximumSize(QSize(5000, 30))
        self.idle_current_threshold_label.setFont(font)
        self.idle_current_threshold_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.idle_current_threshold_label)

        self.idle_current_threshold_text = QLineEdit(self.widget)
        self.idle_current_threshold_text.setObjectName(u"idle_current_threshold_text")
        self.idle_current_threshold_text.setMinimumSize(QSize(380, 30))
        self.idle_current_threshold_text.setMaximumSize(QSize(5000, 30))
        self.idle_current_threshold_text.setFont(font)
        self.idle_current_threshold_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.idle_current_threshold_text)

        self.idle_time_threshold_label = QLabel(self.widget)
        self.idle_time_threshold_label.setObjectName(u"idle_time_threshold_label")
        self.idle_time_threshold_label.setMinimumSize(QSize(380, 0))
        self.idle_time_threshold_label.setMaximumSize(QSize(5000, 30))
        self.idle_time_threshold_label.setFont(font)
        self.idle_time_threshold_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.idle_time_threshold_label)

        self.idle_time_threshold_text = QLineEdit(self.widget)
        self.idle_time_threshold_text.setObjectName(u"idle_time_threshold_text")
        self.idle_time_threshold_text.setMinimumSize(QSize(380, 30))
        self.idle_time_threshold_text.setMaximumSize(QSize(5000, 30))
        self.idle_time_threshold_text.setFont(font)
        self.idle_time_threshold_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.idle_time_threshold_text)

        self.api_key_label = QLabel(self.widget)
        self.api_key_label.setObjectName(u"api_key_label")
        self.api_key_label.setMinimumSize(QSize(380, 0))
        self.api_key_label.setMaximumSize(QSize(5000, 30))
        self.api_key_label.setFont(font)
        self.api_key_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.api_key_label)

        self.api_key_text = QLineEdit(self.widget)
        self.api_key_text.setObjectName(u"api_key_text")
        self.api_key_text.setMinimumSize(QSize(380, 30))
        self.api_key_text.setMaximumSize(QSize(5000, 30))
        self.api_key_text.setFont(font)
        self.api_key_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.api_key_text)

        self.api_secret_label = QLabel(self.widget)
        self.api_secret_label.setObjectName(u"api_secret_label")
        self.api_secret_label.setMinimumSize(QSize(380, 0))
        self.api_secret_label.setMaximumSize(QSize(5000, 30))
        self.api_secret_label.setFont(font)
        self.api_secret_label.setMargin(2)

        self.verticalLayout_2.addWidget(self.api_secret_label)

        self.api_secret_text = QLineEdit(self.widget)
        self.api_secret_text.setObjectName(u"api_secret_text")
        self.api_secret_text.setMinimumSize(QSize(380, 30))
        self.api_secret_text.setMaximumSize(QSize(5000, 30))
        self.api_secret_text.setFont(font)
        self.api_secret_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.api_secret_text)

        self.error_message_text = QLabel(self.widget)
        self.error_message_text.setObjectName(u"error_message_text")
        self.error_message_text.setFont(font)
        self.error_message_text.setStyleSheet(u"color: rgb(237, 51, 59);")

        self.verticalLayout_2.addWidget(self.error_message_text)

        self.submit_button = QPushButton(self.widget)
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setMinimumSize(QSize(200, 40))
        self.submit_button.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(16)
        self.submit_button.setFont(font1)
        self.submit_button.setStyleSheet(u"background-color: rgb(28, 113, 216);")

        self.verticalLayout_2.addWidget(self.submit_button)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(settings_dialog)

        QMetaObject.connectSlotsByName(settings_dialog)
    # setupUi

    def retranslateUi(self, settings_dialog):
        settings_dialog.setWindowTitle(QCoreApplication.translate("settings_dialog", u"Settings Section", None))
        self.site_name_label.setText(QCoreApplication.translate("settings_dialog", u"Site Name:", None))
        self.site_name_text.setText("")
        self.asset_id_label.setText(QCoreApplication.translate("settings_dialog", u"Asset ID:", None))
        self.asset_id_text.setText("")
        self.device_id_label.setText(QCoreApplication.translate("settings_dialog", u"Device ID:", None))
        self.device_id_text.setText("")
        self.ct_sensitivity_label.setText(QCoreApplication.translate("settings_dialog", u"CT Sensitivty", None))
        self.ct_sensitivity_text.setText("")
        self.idle_current_threshold_label.setText(QCoreApplication.translate("settings_dialog", u"Idle Current Threshold", None))
        self.idle_current_threshold_text.setText("")
        self.idle_time_threshold_label.setText(QCoreApplication.translate("settings_dialog", u"Idle Time Threshold", None))
        self.idle_time_threshold_text.setText("")
        self.api_key_label.setText(QCoreApplication.translate("settings_dialog", u"API Key", None))
        self.api_key_text.setText("")
        self.api_secret_label.setText(QCoreApplication.translate("settings_dialog", u"API Secret", None))
        self.api_secret_text.setText("")
        self.error_message_text.setText("")
        self.submit_button.setText(QCoreApplication.translate("settings_dialog", u"SUBMIT", None))
    # retranslateUi

