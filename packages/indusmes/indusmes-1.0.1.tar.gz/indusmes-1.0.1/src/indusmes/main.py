#!/usr/bin/env python3
import os
os.environ["QT_LOGGING_RULES"] = "qt.accessibility.atspi*=false"
import sys
from PySide6.QtCore import QThread, Signal                                      
import multiprocessing
from PySide6 import QtWidgets
from indusmes.backend.sensor import Sensor
from indusmes.home.home import home


class DataReceiver(QThread):
    data_received = Signal(object)

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.recv()
            self.data_received.emit(data)

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, app, parent_conn, child_conn):
        super().__init__()
        self.home = home(app)
        self.home.showMaximized()
        self.parent_conn = parent_conn
        self.child_conn = child_conn
        self.data_receiver = DataReceiver(parent_conn)
        self.data_receiver.data_received.connect(self.update_gui)
        self.data_receiver.start()
        self.start_sensor_process()

    def start_sensor_process(self):
        self.sensor_process = multiprocessing.Process(target=Sensor().run, args=(self.child_conn,))
        self.sensor_process.start()

    def close_sensor_process(self):
        self.sensor_process.terminate()

    def update_gui(self, new_data):
        if isinstance(new_data, str):  
                self.home.show_downtime(DATA=new_data)
        elif isinstance(new_data, float):
            latest_current_value = new_data
            self.home.current_value_text.setText(f'Current Value: {str(latest_current_value)} Amps')

def main():
    app = QtWidgets.QApplication(sys.argv)
    parent_conn, child_conn = multiprocessing.Pipe()  
    main_app = MainApp(app, parent_conn, child_conn)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()