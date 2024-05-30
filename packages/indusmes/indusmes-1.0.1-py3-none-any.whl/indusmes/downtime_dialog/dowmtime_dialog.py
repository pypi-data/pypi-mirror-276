from PySide6 import QtWidgets, QtCore, QtGui
from indusmes.downtime_dialog.ui_downtime_dialog import Ui_downtime_reasons_dialog


class downtime_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(downtime_dialog, self).__init__()
        self.ui = Ui_downtime_reasons_dialog()
        self.ui.setupUi(self)
        self.textBrowser = self.ui.textBrowser
        self.downtime_start_time_text = self.ui.downtime_start_time_text
        self.downtime_reasons_combo = self.ui.downtime_reasons_combo
        self.msg_text = self.ui.msg_text
        self.submit_button = self.ui.pushButton
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()