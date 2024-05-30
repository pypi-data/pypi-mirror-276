# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'job_card.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_job_card(object):
    def setupUi(self, job_card):
        if not job_card.objectName():
            job_card.setObjectName(u"job_card")
        job_card.setWindowModality(Qt.ApplicationModal)
        job_card.resize(470, 200)
        job_card.setMinimumSize(QSize(470, 200))
        job_card.setMaximumSize(QSize(5000, 200))
        job_card.setStyleSheet(u"job{\n"
"	\n"
"	border-color: rgb(255, 255, 255);\n"
"	border-radius: 10px;\n"
"\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(job_card)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.job_id_section = QHBoxLayout()
        self.job_id_section.setSpacing(0)
        self.job_id_section.setObjectName(u"job_id_section")
        self.id_label = QLabel(job_card)
        self.id_label.setObjectName(u"id_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_label.sizePolicy().hasHeightForWidth())
        self.id_label.setSizePolicy(sizePolicy)
        self.id_label.setMinimumSize(QSize(80, 30))
        self.id_label.setMaximumSize(QSize(80, 30))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(12)
        self.id_label.setFont(font)
        self.id_label.setLayoutDirection(Qt.LeftToRight)

        self.job_id_section.addWidget(self.id_label)

        self.id_text = QLabel(job_card)
        self.id_text.setObjectName(u"id_text")
        sizePolicy.setHeightForWidth(self.id_text.sizePolicy().hasHeightForWidth())
        self.id_text.setSizePolicy(sizePolicy)
        self.id_text.setMinimumSize(QSize(264, 30))
        self.id_text.setMaximumSize(QSize(5000, 30))
        self.id_text.setFont(font)
        self.id_text.setStyleSheet(u"")

        self.job_id_section.addWidget(self.id_text)


        self.verticalLayout.addLayout(self.job_id_section)

        self.material_name_section = QHBoxLayout()
        self.material_name_section.setSpacing(0)
        self.material_name_section.setObjectName(u"material_name_section")
        self.material_label = QLabel(job_card)
        self.material_label.setObjectName(u"material_label")
        sizePolicy.setHeightForWidth(self.material_label.sizePolicy().hasHeightForWidth())
        self.material_label.setSizePolicy(sizePolicy)
        self.material_label.setMinimumSize(QSize(80, 30))
        self.material_label.setMaximumSize(QSize(80, 30))
        self.material_label.setFont(font)
        self.material_label.setLayoutDirection(Qt.LeftToRight)

        self.material_name_section.addWidget(self.material_label)

        self.material_text = QLabel(job_card)
        self.material_text.setObjectName(u"material_text")
        sizePolicy.setHeightForWidth(self.material_text.sizePolicy().hasHeightForWidth())
        self.material_text.setSizePolicy(sizePolicy)
        self.material_text.setMinimumSize(QSize(264, 30))
        self.material_text.setMaximumSize(QSize(5000, 30))
        self.material_text.setFont(font)
        self.material_text.setStyleSheet(u"")

        self.material_name_section.addWidget(self.material_text)


        self.verticalLayout.addLayout(self.material_name_section)

        self.quantity_section = QHBoxLayout()
        self.quantity_section.setSpacing(0)
        self.quantity_section.setObjectName(u"quantity_section")
        self.quantity_label = QLabel(job_card)
        self.quantity_label.setObjectName(u"quantity_label")
        sizePolicy.setHeightForWidth(self.quantity_label.sizePolicy().hasHeightForWidth())
        self.quantity_label.setSizePolicy(sizePolicy)
        self.quantity_label.setMinimumSize(QSize(80, 30))
        self.quantity_label.setMaximumSize(QSize(80, 30))
        self.quantity_label.setFont(font)
        self.quantity_label.setLayoutDirection(Qt.LeftToRight)

        self.quantity_section.addWidget(self.quantity_label)

        self.quantity_text = QLabel(job_card)
        self.quantity_text.setObjectName(u"quantity_text")
        sizePolicy.setHeightForWidth(self.quantity_text.sizePolicy().hasHeightForWidth())
        self.quantity_text.setSizePolicy(sizePolicy)
        self.quantity_text.setMinimumSize(QSize(264, 30))
        self.quantity_text.setMaximumSize(QSize(5000, 30))
        self.quantity_text.setFont(font)
        self.quantity_text.setStyleSheet(u"")

        self.quantity_section.addWidget(self.quantity_text)


        self.verticalLayout.addLayout(self.quantity_section)

        self.date_section = QHBoxLayout()
        self.date_section.setSpacing(0)
        self.date_section.setObjectName(u"date_section")
        self.date_label = QLabel(job_card)
        self.date_label.setObjectName(u"date_label")
        sizePolicy.setHeightForWidth(self.date_label.sizePolicy().hasHeightForWidth())
        self.date_label.setSizePolicy(sizePolicy)
        self.date_label.setMinimumSize(QSize(80, 30))
        self.date_label.setMaximumSize(QSize(80, 30))
        self.date_label.setFont(font)
        self.date_label.setLayoutDirection(Qt.LeftToRight)

        self.date_section.addWidget(self.date_label)

        self.date_text = QLabel(job_card)
        self.date_text.setObjectName(u"date_text")
        sizePolicy.setHeightForWidth(self.date_text.sizePolicy().hasHeightForWidth())
        self.date_text.setSizePolicy(sizePolicy)
        self.date_text.setMinimumSize(QSize(264, 30))
        self.date_text.setMaximumSize(QSize(5000, 30))
        self.date_text.setFont(font)
        self.date_text.setStyleSheet(u"")

        self.date_section.addWidget(self.date_text)


        self.verticalLayout.addLayout(self.date_section)

        self.status_section = QHBoxLayout()
        self.status_section.setSpacing(0)
        self.status_section.setObjectName(u"status_section")
        self.status_label = QLabel(job_card)
        self.status_label.setObjectName(u"status_label")
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setMinimumSize(QSize(80, 30))
        self.status_label.setMaximumSize(QSize(80, 30))
        self.status_label.setFont(font)
        self.status_label.setLayoutDirection(Qt.LeftToRight)

        self.status_section.addWidget(self.status_label)

        self.status_text = QLabel(job_card)
        self.status_text.setObjectName(u"status_text")
        sizePolicy.setHeightForWidth(self.status_text.sizePolicy().hasHeightForWidth())
        self.status_text.setSizePolicy(sizePolicy)
        self.status_text.setMinimumSize(QSize(264, 30))
        self.status_text.setMaximumSize(QSize(5000, 30))
        self.status_text.setFont(font)
        self.status_text.setStyleSheet(u"")

        self.status_section.addWidget(self.status_text)


        self.verticalLayout.addLayout(self.status_section)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.view_job_detail_button = QPushButton(job_card)
        self.view_job_detail_button.setObjectName(u"view_job_detail_button")
        sizePolicy.setHeightForWidth(self.view_job_detail_button.sizePolicy().hasHeightForWidth())
        self.view_job_detail_button.setSizePolicy(sizePolicy)
        self.view_job_detail_button.setMinimumSize(QSize(0, 40))
        self.view_job_detail_button.setMaximumSize(QSize(5000, 40))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(16)
        self.view_job_detail_button.setFont(font1)
        self.view_job_detail_button.setLayoutDirection(Qt.LeftToRight)
        self.view_job_detail_button.setAutoFillBackground(False)
        self.view_job_detail_button.setStyleSheet(u"background-color: rgb(26, 95, 180);")
        self.view_job_detail_button.setAutoDefault(False)
        self.view_job_detail_button.setFlat(False)

        self.verticalLayout_2.addWidget(self.view_job_detail_button)


        self.retranslateUi(job_card)

        self.view_job_detail_button.setDefault(False)


        QMetaObject.connectSlotsByName(job_card)
    # setupUi

    def retranslateUi(self, job_card):
        job_card.setWindowTitle(QCoreApplication.translate("job_card", u"Form", None))
        self.id_label.setText(QCoreApplication.translate("job_card", u"Job ID:", None))
        self.id_text.setText("")
        self.material_label.setText(QCoreApplication.translate("job_card", u"Material:", None))
        self.material_text.setText("")
        self.quantity_label.setText(QCoreApplication.translate("job_card", u"Quantity:", None))
        self.quantity_text.setText("")
        self.date_label.setText(QCoreApplication.translate("job_card", u"Date:", None))
        self.date_text.setText("")
        self.status_label.setText(QCoreApplication.translate("job_card", u"Status:", None))
        self.status_text.setText("")
        self.view_job_detail_button.setText(QCoreApplication.translate("job_card", u"View", None))
    # retranslateUi

