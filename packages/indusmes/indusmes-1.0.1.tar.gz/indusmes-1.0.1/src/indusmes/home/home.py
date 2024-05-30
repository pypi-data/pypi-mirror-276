import os
from tracemalloc import stop
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QMetaMethod
import requests
import json
from datetime import datetime
from indusmes.home.ui_home import Ui_MainWindow
from indusmes.job_card.job_card import job_card
from indusmes.progress.progress_dialog import progress_dialog
from indusmes.rejects.rejects_dialog import rejects_dialog
from indusmes.complete.complete_dialog import complete_dialog
from indusmes.user_profile.profile_dialog import profile_dialog
from indusmes.settings.settings_dialog import settings_dialog
from indusmes.ongoing_job_alert.ongoing_job_alert_dialog import ongoing_job_alert_dialog
from indusmes.downtime_dialog.dowmtime_dialog import downtime_dialog


class home(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        
        #super(home, self).__init__(parent)

        # Load the ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'backend', 'config.json')
        #self.config_file = os.path.expanduser("~/indusmes/src/indusmes/backend/config.json")


        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        self.site = config_data['site']
        self.asset_id = config_data['asset_id']
        self.device_id = config_data['device_id']
        self.api_key = config_data['api_key']
        self.api_secret = config_data['api_secret']
        self.ct_sensitivity_text = config_data['ct_sensitivity']
        self.idle_current_threshold_text = config_data['idle_current_threshold']
        self.idle_time_threshold_text = config_data['idle_time_threshold']
        self.active_job_id = config_data['active_job_id']
        self.active_downtime_id = config_data['active_downtime_id']

        # Code for current values
        self.current_value_text = self.ui.current_value_text
        

        # Code section for init profile functionality
        self.profile = self.ui.profileButton
        self.profile.clicked.connect(self.load_profile_section)

        # Code section for init settings functionality
        self.settings = self.ui.settingsButton
        self.settings.clicked.connect(self.load_settings_section)

        # Code section for init main section
        self.main_section = self.ui.main_section
        self.login_page = self.ui.login
        self.job_list_page = self.ui.job_list
        self.job_card_page = self.ui.job_details

        # Code for login functionality
        self.session = requests.Session()
        self.main_section.setCurrentWidget(self.login_page)
        self.username = self.ui.username_text
        self.password = self.ui.password_text
        #self.username.setText("administrator") # Only for development
        #self.password.setText("Ajspj0844l!@#") # Only for development
        self.message = self.ui.message
        login_btn = self.ui.login_button
        login_btn.clicked.connect(self.login)

        # Code for job list functionality
        self.job_list_area = self.ui.job_area_contents
        self.job_list_area.setLayout(QtWidgets.QVBoxLayout())
        self.job_list_area.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        # Code for job card functionality
        self.job_id_text = self.ui.job_id_text
        self.operation_text = self.ui.operation_text
        self.material_text = self.ui.material_text
        self.date_text = self.ui.date_text
        self.quantity_text = self.ui.quantity_text
        self.status_text = self.ui.status_text
        self.good_quantity_text = self.ui.good_quantity_text
        self.reject_quantity_text = self.ui.reject_quantity_text
        self.job_list_btn = self.ui.job_list_btn
        self.start_job_btn = self.ui.start_job_btn
        self.stop_job_btn = self.ui.stop_job_btn
        self.complete_job_btn = self.ui.complete_job_btn
        self.progress_btn = self.ui.progress_btn
        self.rejects_btn = self.ui.rejects_btn

    #Load Profile Section Code Comes Here:
    def load_profile_section(self):
        layout = profile_dialog()
        if 'sid' in self.session.cookies:
            layout.user_name_text.setText(self.username.text())
            layout.logout_button.clicked.connect(lambda: self.logout(layout))
        else:
            layout.user_name_text.setText("Login to View")
            layout.logout_button.setEnabled(False)
        layout.exec()

    def logout(self, layout):
        self.main_section.setCurrentWidget(self.login_page)
        self.clear_job_list_area()
        self.session.close()
        self.username.clear()
        self.password.clear()
        self.message.clear()
        self.settings.setEnabled(True)
        layout.close()
    
    #Load settings section code comes here:
    def load_settings_section(self):
        layout = settings_dialog()
        layout.site_name_text.setText(str(self.site))
        layout.asset_id_text.setText(str(self.asset_id))
        layout.device_id_text.setText(str(self.device_id))
        layout.ct_sensitivity_text.setText(str(self.ct_sensitivity_text))
        layout.idle_current_threshold_text.setText(str(self.idle_current_threshold_text))
        layout.idle_time_threshold_text.setText(str(self.idle_time_threshold_text))
        layout.api_key_text.setText(str(self.api_key))
        layout.api_secret_text.setText(str(self.api_secret))
        layout.error_message_text.setText("")
        layout.submit_button.clicked.connect(lambda: self.update_settings(layout))
        layout.exec()
    
    def update_settings(self, layout):
        self.site = layout.site_name_text.text()
        self.asset_id = layout.asset_id_text.text()
        self.device_id = layout.device_id_text.text()
        self.ct_sensitivity_text = layout.ct_sensitivity_text.text()
        self.idle_current_threshold_text = layout.idle_current_threshold_text.text()
        self.idle_time_threshold_text = layout.idle_time_threshold_text.text()
        self.api_key = layout.api_key_text.text()
        self.api_secret = layout.api_secret_text.text()

        if self.site == "" or self.asset_id == "" or self.device_id == "" or self.api_key == "" or self.api_secret == "" or self.ct_sensitivity_text == "" or self.idle_current_threshold_text == "" or self.idle_time_threshold_text == "":
            layout.error_message_text.setText("Please Fill All Fields")
        else:
            layout.error_message_text.setText("")
            config_data = {
                'site': self.site,
                'asset_id': self.asset_id,
                'device_id': self.device_id,
                'ct_sensitivity' : self.ct_sensitivity_text,
                'idle_current_threshold': self.idle_current_threshold_text,
                'idle_time_threshold': self.idle_time_threshold_text,
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'active_job_id': self.active_job_id,
                'active_downtime_id': self.active_downtime_id
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f)
            layout.close()
        
    def login(self):
        if self.site == "" or self.asset_id == "" or self.device_id == "":
            self.message.setText("Please Set Up Your Settings")
        else:
            self.message.setText("")
            url = f"{self.site}/api/method/login"
            payload = json.dumps({
                "usr": self.username.text(),
                "pwd": self.password.text()
            })
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = self.session.post(url, headers=headers, data=payload)
                response.raise_for_status()
                self.message.setText("")
                self.view_job_list()
                self.settings.setEnabled(False)
            except requests.exceptions.RequestException as e:
                if e.response is not None:
                    if e.response.status_code == 401:
                        self.message.setText('Invalid Username or Password')
                    elif e.response.status_code == 417:
                        self.message.setText('Please Check Internet Connection')
                    elif e.response.status_code == 500:
                        self.message.setText("Server Error")
                    else:
                        self.message.setText('Unknown Error')
                else:
                    self.message.setText('Server Error')
    
    def view_job_list(self):
        self.main_section.setCurrentWidget(self.job_list_page)
        self.clear_job_list_area()
        self.fetch_latest_job_list()
        jobs = json.loads(self.joblist)['data']
        for job in jobs:
            card = job_card()
            card.job_id.setText(str(job['name']))
            card.material.setText(str(job['material_name']))
            card.date.setText(str(job['planned_start_date_time']))
            card.quantity.setText(str(job['planned_quantity']))
            card.status.setText(str(job['job_status']))
            card.view.clicked.connect(self.card_lambda(card.job_id))
            self.job_list_area.layout().addWidget(card)
    

    def clear_job_list_area(self):
        while self.job_list_area.layout().count() > 0:
            widget = self.job_list_area.layout().itemAt(0).widget()
            self.job_list_area.layout().removeWidget(widget)
            widget.setParent(None)
            del widget
    
    def fetch_latest_job_list(self):
            url = f"{self.site}/api/v2/document/Job Card?fields=[\"*\"]&filters=[[\"asset\", \"=\", \"{self.asset_id}\"],[\"job_status\", \"!=\", \"Cancelled\"],[\"job_status\", \"!=\", \"Completed\"]]&order_by=planned_start_date_time%20asc"
            response = self.session.get(url)
            print(response.text)
            self.joblist = response.text
    
    def card_lambda(self, job_id):
        return lambda: self.view_job_details(job_id.text())
    
    def view_job_details(self, job_id):
        self.main_section.setCurrentWidget(self.job_card_page)
        self.clear_job_details()
        data = self.fetch_latest_job_details(job_id)
        print(data)
        self.operation_text.setText(str(data['operation_name']))
        self.job_id_text.setText(str(data['name']))
        self.material_text.setText(str(data['material_name']))
        self.date_text.setText(str(data['planned_start_date_time']))
        self.quantity_text.setText(str(data['planned_quantity']))
        self.status_text.setText(str(data['job_status']))
        self.good_quantity_text.setText(str(data['actual_good_output']))
        self.reject_quantity_text.setText(str(data['actual_rejected_output']))
        # set buttons
        self.start_job_btn.clicked.connect(lambda: self.start_job_btn_fn(job_id))
        self.stop_job_btn.clicked.connect(lambda: self.stop_job_btn_fn(job_id))
        self.complete_job_btn.clicked.connect(lambda: self.complete_job_btn_fn(job_id))
        self.progress_btn.clicked.connect(lambda: self.progress_job_btn_fn(job_id))
        self.rejects_btn.clicked.connect(lambda: self.rejects_job_btn_fn(job_id))
        self.job_list_btn.clicked.connect(lambda: (self.disconnect_btns(), self.view_job_list()))
        #if else logic for enabling & disabling buttons
        if self.status_text.text() == "Not Started":
            self.start_job_btn.setEnabled(True)
            self.stop_job_btn.setEnabled(False)
            self.complete_job_btn.setEnabled(False)
            self.progress_btn.setEnabled(False)
            self.rejects_btn.setEnabled(False)
        elif self.status_text.text() == "In Progress":
            self.start_job_btn.setEnabled(False)
            self.stop_job_btn.setEnabled(True)
            self.complete_job_btn.setEnabled(True)
            self.progress_btn.setEnabled(True)
            self.rejects_btn.setEnabled(True)
        elif self.status_text.text() == "Stopped":
            self.start_job_btn.setEnabled(True)
            self.stop_job_btn.setEnabled(False)
            self.complete_job_btn.setEnabled(True)
            self.progress_btn.setEnabled(False)
            self.rejects_btn.setEnabled(False)
        elif self.status_text.text() == "Completed":
            self.start_job_btn.setEnabled(False)
            self.stop_job_btn.setEnabled(False)
            self.complete_job_btn.setEnabled(False)
            self.progress_btn.setEnabled(False)
            self.rejects_btn.setEnabled(False)

    def clear_job_details(self):
        self.job_id_text.clear()
        self.operation_text.clear()
        self.material_text.clear()
        self.date_text.clear()
        self.quantity_text.clear()
        self.status_text.clear()
        self.good_quantity_text.clear()
        self.reject_quantity_text.clear()
        self.disconnect_btns()
    
    def fetch_latest_job_details(self, job_id):
        url = f"{self.site}/api/v2/document/Job Card/{job_id}"
        response = self.session.get(url)
        data = {}
        if response.status_code == 200:
            data = json.loads(response.text)['data']
        return data

    def start_job_btn_fn(self, job_id):
        ongoing_job = self.check_ongoing_job()
        if ongoing_job is not None:
            dialog = ongoing_job_alert_dialog()
            dialog.job_id_text.setText(ongoing_job)
            dialog.exec()
        else:
            url = f"{self.site}/api/v2/method/indusworks.api.start_job?name={job_id}&user={self.username.text()}"
            response = self.session.post(url)
            print(response.text)
            if response.status_code == 200:
                with open(self.config_file, 'r+') as f:
                    config_data = json.load(f)
                    config_data['active_job_id'] = job_id
                    f.seek(0)
                    json.dump(config_data, f)
                    f.truncate()
                self.view_job_details(job_id)
            else:
                print("Server Busy Please Try Again Later")

    def check_ongoing_job(self):
        jobs = json.loads(self.joblist)['data']
        for job in jobs:
            if job['job_status'] == "In Progress":
                return job['name']
        return None

    def stop_job_btn_fn(self, job_id):
        url = f"{self.site}/api/v2/method/indusworks.api.stop_job?name={job_id}"
        response = self.session.post(url)
        if response.status_code == 200:
            with open(self.config_file, 'r+') as f:
                config_data = json.load(f)
                config_data['active_job_id'] = ""
                f.seek(0)
                json.dump(config_data, f)
                f.truncate()
            self.view_job_details(job_id)
        else:
            print("Server Busy Please Try Again Later")

    def progress_job_btn_fn(self, job_id):
        dialog = progress_dialog()
        dialog.current_good_qty_text.setText(str(self.good_quantity_text.text()))
        dialog.submit_btn.clicked.connect(lambda: self.send_job_progress(dialog, job_id))
        dialog.exec()
    
    def rejects_job_btn_fn(self, job_id):
        url = f"{self.site}/api/v2/document/Reject Reasons?fields=[\"name\", \"reason\"]"
        response = self.session.get(url)
        options = json.loads(response.text)['data']
        dialog = rejects_dialog()
        dialog.current_reject_qty_text.setText(str(self.reject_quantity_text.text()))
        dialog.submit_btn.clicked.connect(lambda: self.send_job_rejects(dialog, job_id, options))
        for option in options:
            dialog.reason_dropdown.addItem(option['reason'])
        dialog.exec()

    def complete_job_btn_fn(self, job_id):
        dialog = complete_dialog()
        dialog.current_good_qty_text.setText(str(self.good_quantity_text.text()))
        dialog.current_reject_qty_text.setText(str(self.reject_quantity_text.text()))
        dialog.submit_btn.clicked.connect(lambda: self.complete_job(dialog, job_id))
        dialog.exec()
        print("Complete Button Clicked")

    def disconnect_btns(self):
        if self.start_job_btn.isSignalConnected(QMetaMethod.fromSignal(self.start_job_btn.clicked)):
            self.start_job_btn.clicked.disconnect()
        else:
            pass
        if self.complete_job_btn.isSignalConnected(QMetaMethod.fromSignal(self.complete_job_btn.clicked)):
            self.complete_job_btn.clicked.disconnect()
        else:
            pass
        if self.progress_btn.isSignalConnected(QMetaMethod.fromSignal(self.progress_btn.clicked)):
            self.progress_btn.clicked.disconnect()
        else:
            pass
        if self.rejects_btn.isSignalConnected(QMetaMethod.fromSignal(self.rejects_btn.clicked)):
            self.rejects_btn.clicked.disconnect()
        else:
            pass
        if self.stop_job_btn.isSignalConnected(QMetaMethod.fromSignal(self.stop_job_btn.clicked)):
            self.stop_job_btn.clicked.disconnect()
        else:
            pass
    
    def send_job_progress(self, dialog, job_id):
        if dialog.add_good_qty_text.value() == 0:
            dialog.msg_text.setText("Please Enter a Valid Quantity")
        else:
            dialog.msg_text.setText("")
            url = f"{self.site}/api/v2/method/indusworks.api.update_progress?name={job_id}&quantity={dialog.add_good_qty_text.value()}"
            headers = {
                'Content-Type': 'application/json'
            }
            response = self.session.post(url, headers=headers)
            if response.status_code == 200:
                dialog.close()
                self.view_job_details(job_id)
            else:
                dialog.msg_text.setText("Server Busy Please Try Again Later")
    
    def send_job_rejects(self, dialog, job_id, options):
        if dialog.add_reject_qty_text.value() == 0:
            dialog.msg_text.setText("Please Enter a Valid Quantity")
        else:
            dialog.msg_text.setText("")
            reason = dialog.reason_dropdown.currentText()
            name = next((item['name'] for item in options if item['reason'] == reason), None)
            url = f"{self.site}/api/v2/method/indusworks.api.update_rejects?name={job_id}&quantity={dialog.add_reject_qty_text.value()}&reject_reason={name}"
            headers = {
                'Content-Type': 'application/json'
            }
            response = self.session.post(url, headers=headers)
            if response.status_code == 200:
                dialog.close()
                self.view_job_details(job_id)
            else:
                dialog.msg_text.setText("Server Busy Please Try Again Later")
    
    def complete_job(self, dialog, job_id):
        url = f"{self.site}/api/v2/method/indusworks.api.complete_job?name={job_id}"
        headers = {
                'Content-Type': 'application/json'
            }
        response = self.session.post(url, headers=headers)
        if response.status_code == 200:
            with open(self.config_file, 'r+') as f:
                config_data = json.load(f)
                config_data['active_job_id'] = ""
                f.seek(0)
                json.dump(config_data, f)
                f.truncate()
            dialog.close()
            self.view_job_details(job_id)
        else:
            dialog.msg_text.setText("Server Busy Please Try Again Later")
        pass

    def show_downtime(self, DATA) -> None:
        dialog = downtime_dialog()
        start_date_time = json.loads(DATA)['data']['start_date_time']
        dt = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S.%f")
        formatted_time = dt.strftime("%d-%m-%y %H:%M:%S")  # Updated format
        downtime_name = json.loads(DATA)['data']['name']
        dialog.downtime_start_time_text.setText(formatted_time)
        # Load downtime reasons from a file
        #reasons_file = os.path.expanduser("~/src/backend/downtime_reasons.json")
        reasons_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'backend', 'downtime_reasons.json')
        with open(reasons_file, 'r') as f:
            reasons = json.load(f)
        for reason in reasons['data']:
            dialog.downtime_reasons_combo.addItem(reason['reason'])
        dialog.submit_button.clicked.connect(lambda: self.update_downtime_reason(reasons_file, dialog, downtime_name))
        dialog.exec()
    
    def update_downtime_reason(self, reasons_file, dialog, downtime_name):
        
        reason = dialog.downtime_reasons_combo.currentText()
        with open(reasons_file, 'r') as f:
            reasons = json.load(f)
        for r in reasons['data']:
            if r['reason'] == reason:
                reason_name = r['name']
                break
        else:
            reason_name = ""
        
        url = f"{self.site}/api/v2/method/indusworks.api.update_downtime?downtime_name={downtime_name}&reason_name={reason_name}"
        headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}"
        }
        response = self.session.post(url, headers=headers)
        if response.status_code == 200:
            dialog.close()
            print("Downtime Reason Updated Successfully")
        else:
            dialog.msg_text.setText("Server Busy Please Try Again Later")