import platform
import time
import math
import json
import requests
import os
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class Sensor:
    def __init__(self):
        self.downtime_reasons_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downtime_reasons.json')
        self.config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
        #self.downtime_reasons_file = os.path.expanduser("~/indusmes/src/indusmes/backend/downtime_reasons.json")
        #self.config_file = os.path.expanduser("~/indusmes/src/indusmes/backend/config.json")
        with open(self.config_file, 'r') as f:
            self.config_data = json.load(f)
        self.site = self.config_data['site']
        self.asset_id = self.config_data['asset_id']
        self.device_id = self.config_data['device_id']
        self.api_key = self.config_data['api_key']
        self.api_secret = self.config_data['api_secret']
        self.ct_sensitivity = float(self.config_data['ct_sensitivity'])
        self.idle_current_threshold = float(self.config_data['idle_current_threshold'])
        self.idle_time_threshold = float(self.config_data['idle_time_threshold'])
        self.downtime_counter = float(0.0)
        self.platform = platform.machine()
        print(f"Platform: {self.platform}")
        if self.platform != 'x86_64':
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(self.i2c)
            self.sensor = AnalogIn(self.ads, ADS.P0)
            print('Sensor Initialized')
        else:
            self.sensor = None

    def update_downtime_reasons(self):
        url = f"{self.site}/api/v2/document/Downtime Reasons?fields=[\"name\", \"reason\"]"
        headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            with open(self.downtime_reasons_file, 'w') as f:
                json.dump(data, f)
            print("Downtime reasons updated successfully")
        else:
            print("Failed to update downtime reasons")
    
    
    def get_latest_current_value(self):
        num_samples = 10
        sum_squared_currents = 0
        for _ in range(num_samples):
            if self.sensor is None:
                voltage = 0
            else:
                voltage = self.sensor.voltage
            instantaneous_current = voltage * self.ct_sensitivity
            sum_squared_currents += instantaneous_current ** 2
        mean_squared_current = sum_squared_currents / num_samples
        latest_current_value = round(math.sqrt(mean_squared_current), 3)
        return latest_current_value

    def check_asset_working(self, latest_current_value):
        if latest_current_value > self.idle_current_threshold:
            return True
        else:
            return False

    def get_active_job(self):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
            active_job_id: str = config_data['active_job_id']
        return active_job_id

    def get_downtime_record(self):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
            downtime_record = config_data['active_downtime_id']
        if downtime_record:
            return downtime_record
        else:
            return None

    def create_downtime_record(self, asset_name):
        url = f"{self.site}/api/v2/method/indusworks.api.create_downtime?asset_name={asset_name}"
        headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}"
        }
        response = requests.post(url, headers=headers)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            data = response.text
            name = json.loads(data)['data']['name']
            print(f"Name: {name}")
            with open(self.config_file, 'r+') as f:
                config_data = json.load(f)
                config_data['active_downtime_id'] = name
                f.seek(0)
                json.dump(config_data, f)
                f.truncate()
            return data
            
    def close_downtime_record(self, downtime_record):
        url = f"{self.site}/api/v2/method/indusworks.api.close_downtime?downtime_name={downtime_record}"
        headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            with open(self.config_file, 'r+') as f:
                config_data = json.load(f)
                config_data['active_downtime_id'] = ""
                f.seek(0)
                json.dump(config_data, f)
                f.truncate()
        print("Downtime record closed successfully")
        
    def run(self, conn):
        self.update_downtime_reasons()
        while True:
            latest_current_value = self.get_latest_current_value()
            print(f"Latest Current Value: {latest_current_value}")
            conn.send(latest_current_value)
            asset_working = self.check_asset_working(latest_current_value)
            if asset_working:
                downtime_record = self.get_downtime_record()
                if downtime_record:
                    self.close_downtime_record(downtime_record)
                    self.downtime_counter = 0.0
                else:
                    pass
            else:
                downtime_record = self.get_downtime_record()
                if downtime_record:
                    pass
                else:
                    self.downtime_counter += 1
                    print(f"Downtime Counter: {self.downtime_counter}")
                    if self.downtime_counter > self.idle_time_threshold:
                        print("Triggering downtime record")
                        data = self.create_downtime_record(self.asset_id)
                        conn.send(data)
                    else:
                        pass
            time.sleep(1)