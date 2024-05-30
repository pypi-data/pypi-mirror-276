from PySide6 import QtWidgets
from indusmes.complete.ui_complete_dialog import Ui_complete_dialog

class complete_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(complete_dialog, self).__init__()
        self.ui = Ui_complete_dialog()
        self.ui.setupUi(self)
        self.show()
        
        self.current_good_qty_text = self.ui.current_good_qty_text
        self.current_reject_qty_text = self.ui.current_reject_qty_text
        self.submit_btn = self.ui.submit_btn