from PySide6 import QtWidgets
from indusmes.settings.ui_settings_dialog import Ui_settings_dialog

class settings_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(settings_dialog, self).__init__()
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        self.show()

        self.site_name_text = self.ui.site_name_text
        self.asset_id_text = self.ui.asset_id_text
        self.device_id_text = self.ui.device_id_text
        self.ct_sensitivity_text = self.ui.ct_sensitivity_text
        self.idle_current_threshold_text = self.ui.idle_current_threshold_text
        self.idle_time_threshold_text = self.ui.idle_time_threshold_text
        self.api_key_text = self.ui.api_key_text
        self.api_secret_text = self.ui.api_secret_text
        self.error_message_text = self.ui.error_message_text
        self.submit_button = self.ui.submit_button