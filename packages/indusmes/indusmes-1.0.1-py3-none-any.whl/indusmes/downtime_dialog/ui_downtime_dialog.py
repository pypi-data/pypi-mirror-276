# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downtime_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_downtime_reasons_dialog(object):
    def setupUi(self, downtime_reasons_dialog):
        if not downtime_reasons_dialog.objectName():
            downtime_reasons_dialog.setObjectName(u"downtime_reasons_dialog")
        downtime_reasons_dialog.setWindowModality(Qt.ApplicationModal)
        downtime_reasons_dialog.resize(400, 400)
        downtime_reasons_dialog.setMinimumSize(QSize(400, 400))
        downtime_reasons_dialog.setMaximumSize(QSize(400, 400))
        downtime_reasons_dialog.setContextMenuPolicy(Qt.NoContextMenu)
        downtime_reasons_dialog.setSizeGripEnabled(False)
        downtime_reasons_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(downtime_reasons_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(downtime_reasons_dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(391, 71))
        self.textBrowser.setMaximumSize(QSize(391, 71))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(16)
        self.textBrowser.setFont(font)

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.downtime_start_time_text = QLabel(self.widget)
        self.downtime_start_time_text.setObjectName(u"downtime_start_time_text")
        self.downtime_start_time_text.setMinimumSize(QSize(0, 40))
        self.downtime_start_time_text.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(18)
        self.downtime_start_time_text.setFont(font1)
        self.downtime_start_time_text.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.downtime_start_time_text)

        self.msg_text = QLabel(self.widget)
        self.msg_text.setObjectName(u"msg_text")
        self.msg_text.setMinimumSize(QSize(0, 20))
        self.msg_text.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.msg_text)

        self.downtime_reasons_combo = QComboBox(self.widget)
        self.downtime_reasons_combo.setObjectName(u"downtime_reasons_combo")
        self.downtime_reasons_combo.setMinimumSize(QSize(40, 60))
        self.downtime_reasons_combo.setMaximumSize(QSize(16777215, 60))
        self.downtime_reasons_combo.setFont(font)
        self.downtime_reasons_combo.setStyleSheet(u"background-color: rgb(119, 118, 123);")

        self.verticalLayout_2.addWidget(self.downtime_reasons_combo)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 60))
        self.pushButton.setMaximumSize(QSize(16777215, 60))
        font2 = QFont()
        font2.setFamilies([u"Roboto"])
        font2.setPointSize(18)
        font2.setBold(False)
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"background-color: rgb(28, 113, 216);")

        self.verticalLayout_2.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(downtime_reasons_dialog)

        QMetaObject.connectSlotsByName(downtime_reasons_dialog)
    # setupUi

    def retranslateUi(self, downtime_reasons_dialog):
        downtime_reasons_dialog.setWindowTitle(QCoreApplication.translate("downtime_reasons_dialog", u"Downtime", None))
        self.textBrowser.setHtml(QCoreApplication.translate("downtime_reasons_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please Update Reason for Downtime Started At:</p></body></html>", None))
        self.downtime_start_time_text.setText("")
        self.msg_text.setText("")
        self.pushButton.setText(QCoreApplication.translate("downtime_reasons_dialog", u"SUBMIT", None))
    # retranslateUi

