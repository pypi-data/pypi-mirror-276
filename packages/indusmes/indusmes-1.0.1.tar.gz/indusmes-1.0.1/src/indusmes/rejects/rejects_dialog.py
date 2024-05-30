from PySide6 import QtWidgets
from indusmes.rejects.ui_rejects_dialog import Ui_report_rejects_dialog

class rejects_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(rejects_dialog, self).__init__()
        self.ui = Ui_report_rejects_dialog()
        self.ui.setupUi(self)
        self.show()
        
        self.current_reject_qty_text = self.ui.current_reject_qty_text
        self.add_reject_qty_text = self.ui.add_reject_qty_text
        self.msg_text = self.ui.msg_text
        self.reason_dropdown = self.ui.reason_dropdown
        self.submit_btn = self.ui.submit_btn
        