from PySide6 import QtWidgets
from indusmes.ongoing_job_alert.ui_ongoing_job_alert_dialog import Ui_ongoing_job_dialog

class ongoing_job_alert_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(ongoing_job_alert_dialog, self).__init__()
        self.ui = Ui_ongoing_job_dialog()
        self.ui.setupUi(self)
        self.show()
        
        self.job_id_text = self.ui.job_id_text