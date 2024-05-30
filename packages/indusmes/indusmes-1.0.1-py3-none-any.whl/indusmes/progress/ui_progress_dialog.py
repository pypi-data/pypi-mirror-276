# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_dialog.ui'
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
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_report_progress_dialog(object):
    def setupUi(self, report_progress_dialog):
        if not report_progress_dialog.objectName():
            report_progress_dialog.setObjectName(u"report_progress_dialog")
        report_progress_dialog.setWindowModality(Qt.WindowModal)
        report_progress_dialog.resize(400, 400)
        report_progress_dialog.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        report_progress_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(report_progress_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.update_progress_layout = QWidget(report_progress_dialog)
        self.update_progress_layout.setObjectName(u"update_progress_layout")
        self.verticalLayout_2 = QVBoxLayout(self.update_progress_layout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 9, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.current_good_qty_label = QLabel(self.update_progress_layout)
        self.current_good_qty_label.setObjectName(u"current_good_qty_label")
        self.current_good_qty_label.setMinimumSize(QSize(220, 60))
        self.current_good_qty_label.setMaximumSize(QSize(220, 60))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(16)
        self.current_good_qty_label.setFont(font)
        self.current_good_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.current_good_qty_label)

        self.current_good_qty_text = QLabel(self.update_progress_layout)
        self.current_good_qty_text.setObjectName(u"current_good_qty_text")
        self.current_good_qty_text.setMinimumSize(QSize(120, 60))
        self.current_good_qty_text.setMaximumSize(QSize(120, 60))
        self.current_good_qty_text.setFont(font)
        self.current_good_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.current_good_qty_text.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.current_good_qty_text.setWordWrap(True)
        self.current_good_qty_text.setMargin(4)

        self.horizontalLayout.addWidget(self.current_good_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_good_qty_label = QLabel(self.update_progress_layout)
        self.add_good_qty_label.setObjectName(u"add_good_qty_label")
        self.add_good_qty_label.setMinimumSize(QSize(220, 60))
        self.add_good_qty_label.setMaximumSize(QSize(220, 60))
        self.add_good_qty_label.setFont(font)
        self.add_good_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.add_good_qty_label)

        self.add_good_qty_text = QSpinBox(self.update_progress_layout)
        self.add_good_qty_text.setObjectName(u"add_good_qty_text")
        self.add_good_qty_text.setMinimumSize(QSize(120, 60))
        self.add_good_qty_text.setMaximumSize(QSize(120, 60))
        self.add_good_qty_text.setFont(font)
        self.add_good_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.add_good_qty_text.setMaximum(1000000)

        self.horizontalLayout_2.addWidget(self.add_good_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.msg_text = QLabel(self.update_progress_layout)
        self.msg_text.setObjectName(u"msg_text")
        self.msg_text.setMinimumSize(QSize(0, 30))
        self.msg_text.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(14)
        self.msg_text.setFont(font1)
        self.msg_text.setStyleSheet(u"color: rgb(237, 51, 59);")
        self.msg_text.setMargin(8)

        self.verticalLayout_2.addWidget(self.msg_text)

        self.submit_btn = QPushButton(self.update_progress_layout)
        self.submit_btn.setObjectName(u"submit_btn")
        self.submit_btn.setMinimumSize(QSize(200, 60))
        self.submit_btn.setMaximumSize(QSize(400, 60))
        font2 = QFont()
        font2.setFamilies([u"Roboto"])
        font2.setPointSize(16)
        font2.setBold(False)
        self.submit_btn.setFont(font2)
        self.submit_btn.setStyleSheet(u"background-color: rgb(28, 113, 216);\n"
"color: rgb(36, 31, 49);")

        self.verticalLayout_2.addWidget(self.submit_btn)


        self.verticalLayout.addWidget(self.update_progress_layout)


        self.retranslateUi(report_progress_dialog)

        QMetaObject.connectSlotsByName(report_progress_dialog)
    # setupUi

    def retranslateUi(self, report_progress_dialog):
        report_progress_dialog.setWindowTitle(QCoreApplication.translate("report_progress_dialog", u"Dialog", None))
        self.current_good_qty_label.setText(QCoreApplication.translate("report_progress_dialog", u"Current Good Quantity:", None))
        self.current_good_qty_text.setText("")
        self.add_good_qty_label.setText(QCoreApplication.translate("report_progress_dialog", u"Add Good Quantity:", None))
        self.msg_text.setText("")
        self.submit_btn.setText(QCoreApplication.translate("report_progress_dialog", u"Submit", None))
    # retranslateUi

