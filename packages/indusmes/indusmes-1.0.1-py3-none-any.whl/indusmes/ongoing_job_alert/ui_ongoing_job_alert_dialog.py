# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ongoing_job_alert_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_ongoing_job_dialog(object):
    def setupUi(self, ongoing_job_dialog):
        if not ongoing_job_dialog.objectName():
            ongoing_job_dialog.setObjectName(u"ongoing_job_dialog")
        ongoing_job_dialog.setWindowModality(Qt.ApplicationModal)
        ongoing_job_dialog.resize(400, 160)
        ongoing_job_dialog.setMinimumSize(QSize(400, 160))
        ongoing_job_dialog.setMaximumSize(QSize(400, 160))
        self.verticalLayout = QVBoxLayout(ongoing_job_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ongoing_job_widget = QWidget(ongoing_job_dialog)
        self.ongoing_job_widget.setObjectName(u"ongoing_job_widget")
        self.ongoing_job_widget.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        self.verticalLayout_2 = QVBoxLayout(self.ongoing_job_widget)
        self.verticalLayout_2.setSpacing(24)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 16, -1, -1)
        self.job_id_text = QLabel(self.ongoing_job_widget)
        self.job_id_text.setObjectName(u"job_id_text")
        self.job_id_text.setMinimumSize(QSize(0, 0))
        self.job_id_text.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(24)
        self.job_id_text.setFont(font)
        self.job_id_text.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.job_id_text)

        self.message = QTextBrowser(self.ongoing_job_widget)
        self.message.setObjectName(u"message")

        self.verticalLayout_2.addWidget(self.message)


        self.verticalLayout.addWidget(self.ongoing_job_widget)


        self.retranslateUi(ongoing_job_dialog)

        QMetaObject.connectSlotsByName(ongoing_job_dialog)
    # setupUi

    def retranslateUi(self, ongoing_job_dialog):
        ongoing_job_dialog.setWindowTitle(QCoreApplication.translate("ongoing_job_dialog", u"Dialog", None))
        self.job_id_text.setText("")
        self.message.setHtml(QCoreApplication.translate("ongoing_job_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Fira Sans Semi-Light'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700;\">Job Already In Progress.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700;\">Please Complete it to Start a New Job!</span></p></body></html>", None))
    # retranslateUi

