from datetime import datetime
import requests
# import socketio
from constant import *
    
# access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTM0Mzk0MCwianRpIjoiYTNlOTg4OWYtZmEwYy00NWQzLWIwOGEtYzAwMzU0MjBiZGMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hbmgucGhhbTE3MDlAaGNtdXQuZWR1LnZuIiwibmJmIjoxNjk5MzQzOTQwLCJleHAiOjE2OTk0MzAzNDB9.ypbLZ_J8XqEQef-0bDfbtg8NVacxC_lLAFafT-9gCW0'
access_token = ""
headers = {
  'Authorization': f'Bearer {access_token}'
}
      
class IrrigationCloud:
  recvCallBack = None
  def __init__(self):
    self.user_ID = None
    self.user_Name = None
    self.room = None
    self.socket_status = False
    # self.sio = socketio.Client()
    
    # @self.sio.on('connect')
    # def on_connect():
    #   self.sio.emit('join_room', {'username': self.user_Name, 'room': self.room})
    #   print('Connected to the server')
    #   self.socket_status = True
    
    # @self.sio.on('disconnect')
    # def on_disconnet():
    #   self.socket_status = False
    #   print('Disconnect to server')

    # @self.sio.on('receive_message')
    # def on_message(data):
    #   self.recvCallBack(data)
      
  def connect(self):
    self.sio.connect(BASE_URL, wait_timeout = 10)
    
  def disconnect(self):
    self.sio.disconnect()
  
  def setRecvCallBack(self, func):
    self.recvCallBack = func
  
  def publish(self, type, data):
    if self.socket_status:
      self.sio.emit('send_message', {'username': self.user_Name, 'room': self.room, 'type': type, 'message': data})
  
  def wait(self):
    self.sio.wait()
  
  def login(self, body):
    res = requests.post(f'{BASE_URL}/login', json=body)
    if res.status_code==200:
      data = res.json()
      token = data['tokens']
      global access_token, headers
      access_token = token['access']
      headers = {
        'Authorization': f'Bearer {access_token}'
      }
      self.user_Name = data['name']
      self.user_ID = data['id_room']
      id_room = data['id_room']
      self.room = f"room{id_room}"
      return True
    return False
  
  def logout(self):
    global access_token, headers
    access_token = ""
    headers = None
    self.user_Name = None
    self.room = None
    self.user_ID = None
    self.disconnect()
  
  def get_current_irrigation(self):
    self.start = datetime.now()
    if len(access_token):
      res = requests.get(f'{BASE_URL}/current-irrigation', headers=headers)
      if res.status_code == 200:
        data = res.json()
        if data['data']:
          data_activity = data['data']
          for item in data_activity:
            # item['device']
            device =  item['device']
            if device['code'] == DEVIVE_ID:
              self.end = datetime.now()
              print(self.end - self.start)
              return item
        else: 
          return []
    return []
    
  def update_activity_irrigation(self, ID, data):
    res = requests.put(f'{BASE_URL}/activity/{ID}', headers=headers, json=data)
    if res.status_code == 200:
      print("Update activity!")
      return True
    return False
  
cloud = IrrigationCloud()
# cloud.connect()
