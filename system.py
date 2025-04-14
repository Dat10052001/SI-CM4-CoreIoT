from Serial.serial_setting import Serial
from Serial.serial_communicate import SerialCommunicate
from IrrigationCloud import *
import json
from datetime import datetime
import numpy as np
from constant import *
from mqtt import MQTTHelper
import paho.mqtt.client as mqtt
import json
from IrrigationCloud import cloud
from utils import *

port = Serial.get_serial_port()
baudrate = Serial.get_serial_bandrate()
    
class IrrigationSystem:
  def __init__(self):
    self.serialCom = SerialCommunicate(port, baudrate)
    self.cloud = cloud
    self.cloud.setRecvCallBack(self.socket_callback)
    self.mqttObject = MQTTHelper()
    self.mqttObject.setRecvCallBack(self.mqtt_callback)
    self.sensor_data = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
    # self.sensor_data = self.serialCom.read_sensor()
    self.start_system_time = int(datetime.now().timestamp())
    
    self.user_ID = self.cloud.user_ID
    self.activities = []
    self.current_irrigation = self.cloud.get_current_irrigation()
    if self.current_irrigation:
      self.activities = self.current_irrigation['activities']
    self.current_activity = self.get_next_one(self.activities)
    self.history_sensor = {}
    self.list_sensor = []
    self.isRunning = False
    self.isUpdate = False
    self.count = 0
    self.send_data_status = [False, False, False, False, False, False, False, False, False, False]
    
  def socket_callback(self, msg):
    type = msg['type']
    if type != "sensor": 
      print('Message:', msg)
    if type == 'enable_irrigation':
      self.reload_data_irrigation()
      message = {
        "content": "Kích hoạt lịch tưới thành công",
        "userId": self.user_ID,
      }
      self.cloud.publish('info', message)
    if "disable_irrigation" in type:
      size = len(type)
      skip_size = len("disable_irrigation") + 1
      irrigation_id = type[skip_size:size]
      if int(irrigation_id) == self.current_irrigation['id']:
        self.reload_data_irrigation()
        message = {
          "content": "Hủy hoạt động của lịch tưới thành công",
          "userId": self.user_ID,
        }
        self.cloud.publish('info', message)
    if "change_activity_of_irrigation" in type:
      size = len(type)
      skip_size = len("change_activity_of_irrigation") + 1
      irrigation_id = type[skip_size:size]
      if int(irrigation_id) == self.current_irrigation['id']:
        self.reload_data_irrigation()
    
  def reload_data_irrigation(self):
    self.current_irrigation = self.cloud.get_current_irrigation()
    if self.current_irrigation:
      self.activities = self.current_irrigation['activities']
    else:
      self.activities = []
    self.current_activity = self.get_next_one(self.activities)
  
  def run_irrigation(self):
    current_time = int(datetime.now().timestamp())
    activity = self.current_activity
    # print(activity)
    print("Running: ", self.isRunning)
    if activity:
      if activity['status'] == READY and (current_time > activity['startAt']+1 or current_time > activity['endAt']) and not self.isRunning:
        self.isUpdate = True
        activity_name = activity['name']
        reason = f"Hoạt động tưới - {activity_name} được bỏ qua do có sự cố"
        activity['successNote'] = "Hoạt động tưới được bỏ qua do có sự cố"
        self.proccess_stop_irrigation(activity, reason, RELAY_1)
        
      if (activity['status'] == READY and activity['startAt'] > current_time):
        if activity['startAt'] - current_time == 60:
          activity_name = activity['name']
          message = {
            'content': f"Hoạt động - {activity_name} sắp diễn ra trong 1 phút",
            "userId": self.user_ID,
            'irrigationId': activity['irrigationId']
          }
          self.cloud.publish("info", message)
          
      if (activity['status'] == READY and activity['progressStatus'] <= 100 
          and activity['startAt'] <= current_time):
        
        if self.start_system_time > activity['startAt']:
          self.isUpdate = True
          reason = "Hoạt động tưới được bỏ qua do có sự cố"
          self.proccess_stop_irrigation(activity, reason, RELAY_1)
        
        newEndTime = activity['endAt']
        self.isRunning = True
        
        if activity['type']==1:
          self.check_threshold(self.sensor_data, activity)
          
        if activity['progressStatus'] < 100.0:
          total_time = activity['endAt'] - activity['startAt']
          elapsed_time = current_time - activity['startAt']
          progress = elapsed_time/total_time
          progress_percentage = int(progress * 100)
          if progress_percentage > 100: progress_percentage = 100
          activity['progressStatus'] = progress_percentage
        
        if current_time >= newEndTime:
          activity_name = activity['name']
          message = f"Hoạt động tưới - {activity_name} đã hoàn thành."
          activity['successNote'] = "Hoạt động tưới đã hoàn thành."
          activity['progressStatus'] = 100
          self.proccess_stop_irrigation(activity, message, RELAY_1)
        else:
          if self.count==0 and self.isRunning:
            activity_name = activity['name']
            message = {
              "content": f"Đang thực hiện hoạt động tưới - {activity_name}.",
              "userId": self.user_ID,
              'irrigationId': activity['irrigationId']
            }
            
            self.cloud.publish("info", message)
            self.count = 1
            self.serialCom.control_relay(RELAY_1, ON)
  
    # update
    self.update_data()
    
  def run_activity_irrigation(self):
    # print("Connect: ", self.cloud.socket_status)
    current_time = int(datetime.now().timestamp())
    # self.current_activity = self.get_next_one(self.activities)
    for activity in self.activities:
      if activity['status'] == READY and (current_time > activity['startAt'] or current_time > activity['endAt']) and not self.isRunning:
        self.isUpdate = True
        activity_name = activity['name']
        reason = f"Hoạt động tưới - {activity_name} được bỏ qua do có sự cố"
        activity['successNote'] = "Hoạt động tưới được bỏ qua do có sự cố"
        self.proccess_stop_irrigation(activity, reason, RELAY_1)
        break
      if (activity['status'] == READY and activity['startAt'] > current_time):
        if activity['startAt'] - current_time == 60:
          activity_name = activity['name']
          message = {
            'content': f"Hoạt động - {activity_name} sắp diễn ra trong 1 phút",
            "userId": self.user_ID,
            'irrigationId': activity['irrigationId']
          }
          self.cloud.publish("info", message)
      if (activity['status'] == READY and activity['progressStatus'] <= 100 
          and activity['startAt'] <= current_time):
        
        if self.start_system_time > activity['startAt']:
          self.isUpdate = True
          reason = "Hoạt động tưới được bỏ qua do có sự cố"
          self.proccess_stop_irrigation(activity, reason, RELAY_1)
          break
        
        newEndTime = activity['endAt']  
        self.isRunning = True
        
        if activity['type']==1:
          check_sensor = self.check_threshold(self.sensor_data, activity)
          if check_sensor == True:
            break
          
        if activity['progressStatus'] < 100.0:
          total_time = activity['endAt'] - activity['startAt']
          elapsed_time = newEndTime - current_time
          progress = 1 - (elapsed_time/total_time)
          progress_percentage = int(progress * 100)
          if progress_percentage > 100: progress_percentage = 100
          activity['progressStatus'] = progress_percentage
        
        if current_time >= newEndTime:
          activity_name = activity['name']
          message = f"Hoạt động tưới - {activity_name} đã hoàn thành."
          activity['successNote'] = "Hoạt động tưới đã hoàn thành."
          activity['progressStatus'] = 100
          self.proccess_stop_irrigation(activity, message, RELAY_1)
        else:
          if self.count==0:
            activity_name = activity['name']
            message = {
              "content": f"Đang thực hiện hoạt động tưới - {activity_name}.",
              "userId": self.user_ID,
              'irrigationId': activity['irrigationId']
            }
            
            self.cloud.publish("info", message)
            self.count = 1
          self.serialCom.control_relay(RELAY_1, ON)
    
    # update
    self.update_data()
    
  def update_data(self):
    # print("Running: ", self.isRunning)
    if self.isUpdate:
      activity_id = self.current_activity['id']
      body = {
        'amountWater': self.current_activity['amountWater'],
        'progressStatus': self.current_activity['progressStatus'],
        'status': self.current_activity['status'],
        'successNote': self.current_activity['successNote'],
        'type': self.current_activity['type'],
      }
      self.isUpdate = False
      self.isRunning = False
      self.count = 0
      self.res = self.cloud.update_activity_irrigation(activity_id, body)
      if self.res : self.cloud.publish("update_irrigation", None)
      self.send_data_status = [False, False, False, False, False, False, False, False, False, False]
      self.current_activity = self.get_next_one(self.activities)
      
    elif self.isRunning:
      
      activity_id = self.current_activity['id']
      body = {
        'amountWater': self.current_activity['amountWater'],
        'progressStatus': self.current_activity['progressStatus'],
        'status': self.current_activity['status'],
        'successNote': self.current_activity['successNote'],
        'type': self.current_activity['type'],
      }
      
      current_time = int(datetime.now().timestamp())
      total_time = self.current_activity['endAt'] - self.current_activity['startAt']
      interval = total_time / 10
      elapsed_time = current_time - self.current_activity['startAt']
      running_time = int(elapsed_time / interval)
      
      if ((running_time == 1 and not self.send_data_status[0]) or
          (running_time == 2 and not self.send_data_status[1]) or
          (running_time == 3 and not self.send_data_status[2]) or
          (running_time == 4 and not self.send_data_status[3]) or
          (running_time == 5 and not self.send_data_status[4]) or
          (running_time == 6 and not self.send_data_status[5]) or
          (running_time == 7 and not self.send_data_status[6]) or
          (running_time == 8 and not self.send_data_status[7]) or
          (running_time == 9 and not self.send_data_status[8]) or
          self.current_activity['status'] == DONE) : 
        
        self.res = self.cloud.update_activity_irrigation(activity_id, body)
        if self.res : self.cloud.publish("update_irrigation", None)
        print("Run Update")
        
        match running_time:
          case 1:
            self.send_data_status[0] = True
          case 2:
            self.send_data_status[1] = True
          case 3:
            self.send_data_status[2] = True
          case 4:
            self.send_data_status[3] = True
          case 5:
            self.send_data_status[4] = True
          case 6:
            self.send_data_status[5] = True
          case 7:
            self.send_data_status[6] = True
          case 8:
            self.send_data_status[7] = True
          case 9:
            self.send_data_status[8] = True
      
      if self.current_activity['status'] == DONE:
        self.isRunning = False
        self.send_data_status = [False, False, False, False, False, False, False, False, False, False]
        self.current_activity = self.get_next_one(self.activities)

  def mqtt_callback(self, msg):
    # print(msg)
    data_sensor = [None, None, None, None, None, None, None]
    data = json.loads(msg)
    # print(data)
    station_id = data["station_id"]
    sensors = data["sensors"]
    if station_id == "soil_0001": # soil_0001 SOIL_0001
      for s in sensors:
        if s["sensor_id"] == "temp_0001":
          data_sensor[TEMP] = float(s["sensor_value"])
        if s["sensor_id"] == "humi_0001":
          data_sensor[HUMI] = float(s["sensor_value"])
        if s["sensor_id"] == "ph_0001":
          data_sensor[PH] = float(s["sensor_value"])
        if s["sensor_id"] == "EC_0001":
          data_sensor[EC] = float(s["sensor_value"])
        if s["sensor_id"] == "Nito_0001":
          data_sensor[N] = float(s["sensor_value"])
        if s["sensor_id"] == "Photpho_0001":
          data_sensor[P] = float(s["sensor_value"])
        if s["sensor_id"] == "Kali_0001":
          data_sensor[K] = float(s["sensor_value"])
        
    self.sensor_data = data_sensor
    print(data_sensor)
    
  def readSensorTest(self):
    self.sensor_data = self.serialCom.read_sensor()
    if self.start_system_time:
      response = self.convert_data_to_json(self.sensor_data)
      self.cloud.publish("sensor", response)
      self.history_sensor = {
        "data": self.sensor_data,
        "time": datetime.now()
      }

  def readSensor(self):
    if self.start_system_time:
      response = self.convert_data_to_json(self.sensor_data)
      self.cloud.publish("sensor", response)
    self.history_sensor = {
      "data": self.sensor_data,
      "time": datetime.now()
    }
  
  def readSensor1(self):
    self.sensor_data = self.serialCom.read_sensor()
    self.mqttObject.publish("/innovation/soilmonitoring/", json.dumps(self.convert_data_to_json(self.sensor_data)))
    
    if self.start_system_time:
      # response = self.convert_data_to_json(self.sensor_data)
      # self.cloud.publish("sensor", response)
      self.history_sensor = {
        "data": self.sensor_data,
        "time": datetime.now()
      }
    
  def check_threshold(self, value, activity):
    # print("Check threshold")
    # print(activity)
    # print("Humi: ", value[HUMI])
    # print("Threshold: ", activity['thresholdSoilHumidity'])
    
    if activity['thresholdSoilTemperature'] != None:
      if value[TEMP] <= activity['thresholdSoilTemperature']:
        message = "Hoạt động tưới dừng do đạt điều kiện nhiệt độ đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilHumidity'] != None:
      # print("Check threshold")
      if value[HUMI] >= activity['thresholdSoilHumidity']:
        message = "Hoạt động tưới dừng do đạt điều kiện độ ẩm đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilPH'] != None:
      if value[PH] >= activity['thresholdSoilPH']:
        message = "Hoạt động tưới dừng do đạt độ pH đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilEC'] != None:
      if value[EC] >= activity['thresholdSoilEC']:
        message = "Hoạt động tưới dừng do đạt điều kiện độ dẫn điện đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilN'] != None:
      if value[N] >= activity['thresholdSoilN']:
        message = "Hoạt động tưới dừng do đạt điều kiện nitor đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilP'] != None:
      if value[P] >= activity['thresholdSoilP']:
        message = "Hoạt động tưới dừng do đạt điều kiện photpho đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
    if activity['thresholdSoilK'] != None:
      if value[K] >= activity['thresholdSoilK']:
        message = "Hoạt động tưới dừng do đạt điều kiện kali đất"
        activity['successNote'] = message
        self.proccess_stop_irrigation(activity, message, RELAY_1)
  
  def proccess_stop_irrigation(self, activity, message, relayID):
    activity['status'] = DONE
    # activity['successNote'] = message
    self.serialCom.control_relay(relayID, OFF)
    # self.isRunning = False
    self.isUpdate = True
    message_info = {
      'content': message,
      "userId": self.user_ID,
      'irrigationId': activity['irrigationId']
    }
    self.cloud.publish("info", message_info)
    # self.count=0
  
  def control_pump(self):
    distance = self.serialCom.read_distance(1)
    volume = distance / 100
    water_volume = self.calculate_water_volume(volume)
    # print(water_volume)
    if distance <= 100:
      if self.serialCom.relay_status[PUMP_1] == True:
        message = {
          "content": "Máy bơm đã được tắt!",
          "userId": self.user_ID
        }
        self.cloud.publish("info", message)
      self.serialCom.control_relay(PUMP_1, OFF)
    elif distance >= 2800:
      if self.serialCom.relay_status[PUMP_1] == False:
        message = {
          "content": "Máy bơm đã được bật!",
          "userId": self.user_ID
        }
        self.cloud.publish("info", message)
        self.serialCom.control_relay(PUMP_1, ON)
  
  def calculate_water_volume(self, distance):
    # d = 34, h = 40
    calc_volume = lambda h: (29 - h)*27*19 
    # calc_volume = lambda h: (40 - h) * 17 * 17 *3.14 
    return calc_volume(distance)
  
  def reset_system(self):
    self.cloud.logout()
    self.user_ID = None
    self.current_irrigation = []
    self.current_activity = []
    self.activities = []
    self.history_sensor = {}
    self.list_sensor = []
    self.isRunning = False
    self.isUpdate = False
    self.count = 0
    self.send_data_status = [False, False, False, False, False, False, False, False, False, False]
        
    self.serialCom.turn_off_all()
    
  def find_first_one_index(self, data):
    for i, item in enumerate(data):
      if item["status"] == 1:
        return i
    return -1

  def get_next_one(self, data):
    first_one_index = self.find_first_one_index(data)
    if first_one_index != -1:
      next_one_index = self.find_first_one_index(data)
      if next_one_index != -1:
        return data[next_one_index]
    
    return []

  def convert_data_to_json(self, data):
    present_time = int(datetime.now().timestamp())
    return {
      "station_id":"soil_0001",
      "station_name":"SOIL 0001",
      "gps_longitude": 106.89,
      "gps_latitude": 10.5,
      "time": present_time,
      "sensors": [
        {
          "sensor_id":"temp_0001",
          "sensor_name":"Nhiệt Độ",
          "sensor_value": data[TEMP],
          "sensor_unit": "ms/cm"
        },
        {
          "sensor_id":"humi_0001",
          "sensor_name":"Độ Ẩm",
          "sensor_value": data[HUMI],
          "sensor_unit": "%"
        },
        {
          "sensor_id":"ph_0001",
          "sensor_name":"PH",
          "sensor_value": data[PH],
          "sensor_unit": " "
        },
        {
          "sensor_id":"EC_0001",
          "sensor_name":"EC",
          "sensor_value": data[EC],
          "sensor_unit": "ms/cm"
        },
        {
          "sensor_id":"Nito_0001",
          "sensor_name":"N",
          "sensor_value": data[N],
          "sensor_unit": "ms/cm"
        },
        {
          "sensor_id":"Photpho_0001",
          "sensor_name":"P",
          "sensor_value": data[P],
          "sensor_unit": "ms/cm"
        },
        {
          "sensor_id":"Kali_0001",
          "sensor_name":"K",
          "sensor_value": data[K],
          "sensor_unit": "ms/cm"
        }
      ]
    }