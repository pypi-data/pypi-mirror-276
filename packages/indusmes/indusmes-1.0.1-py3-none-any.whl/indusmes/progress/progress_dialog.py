from PySide6 import QtWidgets
from indusmes.progress.ui_progress_dialog import Ui_report_progress_dialog

class progress_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(progress_dialog, self).__init__()
        self.ui = Ui_report_progress_dialog()
        self.ui.setupUi(self)
        self.show()
        
        self.current_good_qty_text = self.ui.current_good_qty_text
        self.add_good_qty_text = self.ui.add_good_qty_text
        self.submit_btn = self.ui.submit_btn
        self.msg_text = self.ui.msg_text