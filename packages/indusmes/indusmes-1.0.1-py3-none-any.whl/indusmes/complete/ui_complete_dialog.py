# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'complete_dialog.ui'
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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_complete_dialog(object):
    def setupUi(self, complete_dialog):
        if not complete_dialog.objectName():
            complete_dialog.setObjectName(u"complete_dialog")
        complete_dialog.setWindowModality(Qt.WindowModal)
        complete_dialog.resize(400, 400)
        complete_dialog.setStyleSheet(u"background-color: rgb(36, 31, 49);")
        complete_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(complete_dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.complete_layout = QWidget(complete_dialog)
        self.complete_layout.setObjectName(u"complete_layout")
        self.verticalLayout_2 = QVBoxLayout(self.complete_layout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.msg_text = QLabel(self.complete_layout)
        self.msg_text.setObjectName(u"msg_text")
        self.msg_text.setMinimumSize(QSize(0, 40))
        self.msg_text.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(16)
        font.setBold(False)
        self.msg_text.setFont(font)
        self.msg_text.setStyleSheet(u"")
        self.msg_text.setAlignment(Qt.AlignCenter)
        self.msg_text.setMargin(8)

        self.verticalLayout_2.addWidget(self.msg_text)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.current_good_qty_label = QLabel(self.complete_layout)
        self.current_good_qty_label.setObjectName(u"current_good_qty_label")
        self.current_good_qty_label.setMinimumSize(QSize(220, 60))
        self.current_good_qty_label.setMaximumSize(QSize(220, 60))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(16)
        self.current_good_qty_label.setFont(font1)
        self.current_good_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.current_good_qty_label)

        self.current_good_qty_text = QLabel(self.complete_layout)
        self.current_good_qty_text.setObjectName(u"current_good_qty_text")
        self.current_good_qty_text.setMinimumSize(QSize(120, 60))
        self.current_good_qty_text.setMaximumSize(QSize(120, 60))
        self.current_good_qty_text.setFont(font1)
        self.current_good_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.current_good_qty_text.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.current_good_qty_text.setWordWrap(True)
        self.current_good_qty_text.setMargin(4)

        self.horizontalLayout.addWidget(self.current_good_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.current_reject_qty_label = QLabel(self.complete_layout)
        self.current_reject_qty_label.setObjectName(u"current_reject_qty_label")
        self.current_reject_qty_label.setMinimumSize(QSize(220, 60))
        self.current_reject_qty_label.setMaximumSize(QSize(220, 60))
        self.current_reject_qty_label.setFont(font1)
        self.current_reject_qty_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.current_reject_qty_label)

        self.current_reject_qty_text = QLabel(self.complete_layout)
        self.current_reject_qty_text.setObjectName(u"current_reject_qty_text")
        self.current_reject_qty_text.setMinimumSize(QSize(120, 60))
        self.current_reject_qty_text.setMaximumSize(QSize(120, 60))
        self.current_reject_qty_text.setFont(font1)
        self.current_reject_qty_text.setStyleSheet(u"background-color: rgb(119, 118, 123);")
        self.current_reject_qty_text.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.current_reject_qty_text.setWordWrap(True)
        self.current_reject_qty_text.setMargin(4)

        self.horizontalLayout_2.addWidget(self.current_reject_qty_text)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.submit_btn = QPushButton(self.complete_layout)
        self.submit_btn.setObjectName(u"submit_btn")
        self.submit_btn.setMinimumSize(QSize(200, 60))
        self.submit_btn.setMaximumSize(QSize(400, 60))
        self.submit_btn.setFont(font)
        self.submit_btn.setStyleSheet(u"background-color: rgb(28, 113, 216);\n"
"color: rgb(36, 31, 49);")

        self.verticalLayout_2.addWidget(self.submit_btn)


        self.verticalLayout.addWidget(self.complete_layout)


        self.retranslateUi(complete_dialog)

        QMetaObject.connectSlotsByName(complete_dialog)
    # setupUi

    def retranslateUi(self, complete_dialog):
        complete_dialog.setWindowTitle(QCoreApplication.translate("complete_dialog", u"Dialog", None))
        self.msg_text.setText(QCoreApplication.translate("complete_dialog", u"Please Confirm Job Output", None))
        self.current_good_qty_label.setText(QCoreApplication.translate("complete_dialog", u"Good Quantity:", None))
        self.current_good_qty_text.setText("")
        self.current_reject_qty_label.setText(QCoreApplication.translate("complete_dialog", u"Reject Quantity:", None))
        self.current_reject_qty_text.setText("")
        self.submit_btn.setText(QCoreApplication.translate("complete_dialog", u"Submit", None))
    # retranslateUi

