from PySide6 import QtWidgets
from indusmes.user_profile.ui_profile_dialog import Ui_profile_dialog

class profile_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(profile_dialog, self).__init__()
        self.ui = Ui_profile_dialog()
        self.ui.setupUi(self)
        self.show()

        self.user_name_text = self.ui.user_name_text
        self.logout_button = self.ui.logout_button