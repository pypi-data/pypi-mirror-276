# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rejects_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_report_rejects_dialog(object):
    def setupUi(self, report_rejects_dialog):
        if not report_rejects_dialog.objectName():
            report_rejects_dialog.setObjectName(u"report_rejects_dialog")
        report_rejects_dialog.setWindowModality(Qt.WindowModal)
        report_rejects_dialog.resize(400, 400)
        report_rejects_dialog.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        report_rejects_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(report_rejects_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.update_rejects_layout = QWidget(report_rejects_dialog)
        self.update_rejects_layout.setObjectName(u"update_rejects_layout")
        self.verticalLayout_2 = QVBoxLayout(self.update_rejects_layout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.current_reject_qty_label = QLabel(self.update_rejects_layout)
        self.current_reject_qty_label.setObjectName(u"current_reject_qty_label")
        self.current_reject_qty_label.setMinimumSize(QSize(220, 60))
        self.current_reject_qty_label.setMaximumSize(QSize(220, 60))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(16)
        self.current_reject_qty_label.setFont(font)
        self.current_reject_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.current_reject_qty_label)

        self.current_reject_qty_text = QLabel(self.update_rejects_layout)
        self.current_reject_qty_text.setObjectName(u"current_reject_qty_text")
        self.current_reject_qty_text.setMinimumSize(QSize(120, 60))
        self.current_reject_qty_text.setMaximumSize(QSize(120, 60))
        self.current_reject_qty_text.setFont(font)
        self.current_reject_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.current_reject_qty_text.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.current_reject_qty_text.setWordWrap(True)
        self.current_reject_qty_text.setMargin(4)

        self.horizontalLayout.addWidget(self.current_reject_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_reject_qty_label = QLabel(self.update_rejects_layout)
        self.add_reject_qty_label.setObjectName(u"add_reject_qty_label")
        self.add_reject_qty_label.setMinimumSize(QSize(220, 60))
        self.add_reject_qty_label.setMaximumSize(QSize(220, 60))
        self.add_reject_qty_label.setFont(font)
        self.add_reject_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.add_reject_qty_label)

        self.add_reject_qty_text = QSpinBox(self.update_rejects_layout)
        self.add_reject_qty_text.setObjectName(u"add_reject_qty_text")
        self.add_reject_qty_text.setMinimumSize(QSize(120, 60))
        self.add_reject_qty_text.setMaximumSize(QSize(120, 60))
        self.add_reject_qty_text.setFont(font)
        self.add_reject_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.add_reject_qty_text.setMaximum(1000000)

        self.horizontalLayout_2.addWidget(self.add_reject_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.reason_label = QLabel(self.update_rejects_layout)
        self.reason_label.setObjectName(u"reason_label")
        self.reason_label.setMinimumSize(QSize(0, 60))
        self.reason_label.setMaximumSize(QSize(16777215, 60))
        self.reason_label.setFont(font)
        self.reason_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.reason_label.setMargin(4)

        self.horizontalLayout_3.addWidget(self.reason_label)

        self.reason_dropdown = QComboBox(self.update_rejects_layout)
        self.reason_dropdown.setObjectName(u"reason_dropdown")
        self.reason_dropdown.setMinimumSize(QSize(240, 60))
        self.reason_dropdown.setMaximumSize(QSize(240, 60))
        self.reason_dropdown.setFont(font)
        self.reason_dropdown.setLayoutDirection(Qt.LeftToRight)
        self.reason_dropdown.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.reason_dropdown.setIconSize(QSize(16, 16))

        self.horizontalLayout_3.addWidget(self.reason_dropdown)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.msg_text = QLabel(self.update_rejects_layout)
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

        self.submit_btn = QPushButton(self.update_rejects_layout)
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


        self.verticalLayout.addWidget(self.update_rejects_layout)


        self.retranslateUi(report_rejects_dialog)

        QMetaObject.connectSlotsByName(report_rejects_dialog)
    # setupUi

    def retranslateUi(self, report_rejects_dialog):
        report_rejects_dialog.setWindowTitle(QCoreApplication.translate("report_rejects_dialog", u"Dialog", None))
        self.current_reject_qty_label.setText(QCoreApplication.translate("report_rejects_dialog", u"Current Reject Quantity:", None))
        self.current_reject_qty_text.setText("")
        self.add_reject_qty_label.setText(QCoreApplication.translate("report_rejects_dialog", u"Add Reject Quantity:", None))
        self.reason_label.setText(QCoreApplication.translate("report_rejects_dialog", u"Reason:", None))
        self.msg_text.setText("")
        self.submit_btn.setText(QCoreApplication.translate("report_rejects_dialog", u"Submit", None))
    # retranslateUi

