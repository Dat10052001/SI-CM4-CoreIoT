# from scheduler_test import Scheduler
# import time
# def task1():
#   print("Task 1")

# def task2():
#   print("task2")
  
# scheduler = Scheduler()
  
# scheduler.SCH_Init()
# scheduler.SCH_Add_Task(task1, 5000, 3000)
# scheduler.SCH_Add_Task(task2, 2000, 1000)
  
# if __name__ == "__main__":
#   while True:
#     scheduler.SCH_Dispatch_Tasks()
    
#     scheduler.SCH_Update()
      
# import json

# # Dữ liệu bạn muốn lưu dưới dạng JSON
# data = [
#   {
#     "name": "John",
#     "age": 30,
#     "city": "New York"
#   },
#   {
#     "name": "John",
#     "age": 30,
#     "city": "New York"
#   }
# ]

# import json

# file_name = "test.json"

# def readFileJson():
#   with open(file_name, "r") as json_file:
#       return json.load(json_file)[0]

# activities = readFileJson()

# print(activities['activities'])

# def calculate_water_volume(distance):
#     # d = 34, h = 40
#     volume = (40*1000 - distance) * 17 * 17 *3.14 
#     return volume
  
# print(calculate_water_volume(1500))

# import sched
# import time

# # Tạo một đối tượng scheduler
# scheduler = sched.scheduler(time.time, time.sleep)

# def do_task():
#     # Thực hiện tác vụ ở đây
#     print("Runn")

# # Lên lịch cho lần thực hiện đầu tiên
# while True:
#   scheduler.enter(5, 1, do_task, ())
#   scheduler.run()

import time

# Thời điểm bắt đầu và kết thúc
start = time.mktime(time.strptime('2023-12-19 00:50:00', '%Y-%m-%d %H:%M:%S'))
end = time.mktime(time.strptime('2023-12-19 00:53:00', '%Y-%m-%d %H:%M:%S'))
# start = 1698919200
# end = 1698920100

task_done = [False, False, False, False, False, False, False, False, False, False]
proccess = 0

while True:
    current_time = time.time()
    if current_time >= start and current_time <= end:
      if current_time == end: 
        proccess = 100
      if proccess < 100.0:
        total_time = end - start
        elapsed_time = end - current_time
        progress_tmp = 1 - (elapsed_time/total_time)
        proccess = int(progress_tmp * 100)
        if proccess > 100: proccess = 100
      
      print("Progress: ", proccess)
      
      current_time = time.time()
      time_interval = (end - start) / 10
      time_elapsed = current_time - start
      running_time = int(time_elapsed / time_interval)
      
      if ((running_time == 1 and not task_done[0]) or
        (running_time == 2 and not task_done[1]) or
        (running_time == 3 and not task_done[2]) or
        (running_time == 4 and not task_done[3]) or
        (running_time == 5 and not task_done[4]) or
        (running_time == 6 and not task_done[5]) or
        (running_time == 7 and not task_done[6]) or
        (running_time == 8 and not task_done[7]) or
        (running_time == 9 and not task_done[8]) or
        proccess >= 100) : 
        print("Progress Update: ", proccess)
        match running_time:
          case 1:
            task_done[0] = True
          case 2:
            task_done[1] = True
          case 3:
            task_done[2] = True
          case 4:
            task_done[3] = True
          case 5:
            task_done[4] = True
          case 6:
            task_done[5] = True
          case 7:
            task_done[6] = True
          case 8:
            task_done[7] = True
          case 9:
            task_done[8] = True
        if proccess == 100: task_done[9] = True

    if all(task_done):
      print("Tất cả tác vụ đã được thực hiện")
      break

    time.sleep(1)

# import numpy as np
# from Serial.serial_communicate import *
# from customtkinter import *
# import time

# serialCom = SerialCommunicate("/dev/ttyUSB0", 9600)

# def pour_liquid(volume):
#     distance_calibration = np.asarray([ 2595, 2591, 2578, 2560, 2543, 2528, 2512, 2495, 2480, 2464, 2447, 2431, 2416, 2399, 2381, 2366, 2351, 2333, 2318,
#                                         2301, 2283, 2271, 2255, 2238, 2223, 2194, 2177, 2160, 2144, 2129, 2114, 2099, 2082, 2068, 2054, 2038, 2024, 2010,
#                                         1993, 1980, 1965, 1952, 1935, 1920, 1905, 1892, 1877, 1864, 1890, 1834, 1820])
#     # convert volume to water level
#     volume_level = round(volume/100)

#     # find current distance of water
#     current_distance = serialCom.read_distance(1)
#     print("First current_distance =", current_distance )
#     # find closest water level of current distace
#     current_volume_level = (np.abs(distance_calibration - current_distance)).argmin()
#     print("current level", current_volume_level)
#     # calculate expect next water level after pour down
#     next_volume_level = current_volume_level - volume_level
#     print("next volume level: ", next_volume_level)
#     if next_volume_level < 0:
#       next_volume_level = 0
#     next_distance = distance_calibration[next_volume_level]
#     print("next distance: ", next_distance)
#     # self.turn_on_relay_0(relay_ID)
#     while True:
#       current_distance = serialCom.read_distance(1)
#       print("current_distance =", current_distance )
#       if current_distance >= next_distance:
#           # self.turn_off_relay_0(relay_ID)
#           print("turn off relay")
#           break
        
#       time.sleep(1)

# def calculate_water_volume(distance):
#   # d = 34, h = 40
#   volume = lambda h: (29 - h)*27*19 
#   # volume = lambda h: (40 - h) * 17 * 17 *3.14 
#   return volume(distance)

# def control_pump():
#   distance = serialCom.read_distance(1) # mm
#   print("Distance = ", distance)
#   water_volume = calculate_water_volume(distance / 100)
#   print("Water volume = ", water_volume)
#   if distance <= 100:
#     print("Turn off pump")
#     serialCom.control_relay(7, 0)
#   elif distance >= 2800:
#     print("Turn on pump")
#     serialCom.control_relay(7, 1)
    
# if __name__ == "__main__":
#   while True:
#     control_pump()    
#     pour_liquid(1800)
    
# import socketio
# import json
# from datetime import datetime

# sio = socketio.Client()

# # Define event handlers
# @sio.on('connect')
# def on_connect():
#     print('Connected to the server')
#     room_name = 'room1'
#     sio.emit('join_room', {'username': 'doan3', 'room': room_name})

# @sio.on('receive_message')
# def on_message(data):
#     # print("run")
#     print('Received a message:', data)
# # Connect to the Socket.IO server
# server_url = 'https://80a1-14-186-176-187.ngrok-free.app'
# sio.connect(server_url)

# response = {
#       "station_id":"SOIL_0001",
#       "station_name":"SOIL 0001",
#       "gps_longitude": 106.89,
#       "gps_latitude": 10.5,
#       "time": int(datetime.now().timestamp()),
#       "sensors": [
#         {
#           "sensor_id":"temp_0001",
#           "sensor_name":"Nhiệt Độ",
#           "sensor_value": 112.3,
#           "sensor_unit": "ms/cm"
#         },
#         {
#           "sensor_id":"humi_0001",
#           "sensor_name":"Độ Ẩm",
#           "sensor_value": 73.5,
#           "sensor_unit": "%"
#         },
#         {
#           "sensor_id":"ph_0001",
#           "sensor_name":"PH",
#           "sensor_value": 112.3,
#           "sensor_unit": " "
#         },
#         {
#           "sensor_id":"EC_0001",
#           "sensor_name":"EC",
#           "sensor_value": 400.3,
#           "sensor_unit": "ms/cm"
#         },
#         {
#           "sensor_id":"Nito_0001",
#           "sensor_name":"N",
#           "sensor_value": 400.3,
#           "sensor_unit": "ms/cm"
#         },
#         {
#           "sensor_id":"Photpho_0001",
#           "sensor_name":"P",
#           "sensor_value": 400.3,
#           "sensor_unit": "ms/cm"
#         },
#         {
#           "sensor_id":"Kali_0001",
#           "sensor_name":"K",
#           "sensor_value": 400.3,
#           "sensor_unit": "ms/cm"
#         }
#       ]
#     }
# sio.emit('send_message', {'username': 'doan3', 'room': 'room1', 'message': json.dumps(response)})

# sio.wait()

