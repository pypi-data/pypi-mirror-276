from PySide6 import QtWidgets
from indusmes.job_card.ui_job_card import Ui_job_card

class job_card(QtWidgets.QWidget):
    def __init__(self):
        super(job_card, self).__init__()
        self.ui = Ui_job_card()
        self.ui.setupUi(self)
        self.show()

        self.job_id = self.ui.id_text
        self.material = self.ui.material_text
        self.quantity = self.ui.quantity_text
        self.date = self.ui.date_text
        self.status = self.ui.status_text
        self.view = self.ui.view_job_detail_button