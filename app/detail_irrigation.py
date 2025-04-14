import customtkinter
import os
from itertools import groupby
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import ttk
from utils import *
from constant import *
import requests
class DetailIrrigation(customtkinter.CTkFrame):
  def __init__(self, master=None, content="Name Irrigation", **kwargs):
    super().__init__(master, **kwargs)
    
    self.parent = master
    self.select_activity = None
    self.detail_label = []
    self.data = []
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    
    self.main_frame = customtkinter.CTkFrame(self, width=740, height=575, corner_radius=6, fg_color="white")
    self.main_frame.grid(row=0, column=0, padx=(15, 10), pady=(10, 10), sticky="nsew")
    self.main_frame.grid_columnconfigure(0, weight=1)
    self.main_frame.grid_rowconfigure((0, 1), weight=1)
    self.main_frame.grid_propagate(0)
    
    self.content_frame = customtkinter.CTkFrame(self.main_frame, width=400, fg_color="transparent")
    self.content_frame.grid(row=0, column=0,padx=(20, 0), pady=25, sticky="nsew")
    self.content_frame.grid_columnconfigure((0, 1), weight=1)
    self.content_frame.grid_rowconfigure(0, weight=1)
    
    
    self.text_frame = customtkinter.CTkFrame(self.content_frame, width=400, height=500, fg_color="transparent")
    self.text_frame.grid(row=0, column=0, sticky="nsew")
    self.text_frame.grid_rowconfigure(5, weight=20)
    self.text_frame.grid_columnconfigure(0, weight=1)
    # self.text_frame.grid_propagate(0)
    
    self.label_1 = customtkinter.CTkLabel(self.main_frame, text="", anchor="w")
    self.label_1.grid(row=0, column=0, padx=20, pady=(10, 0))
  
    self.name_irrigation = customtkinter.CTkLabel(self.text_frame, text="", anchor="w", font=("Montserrat Bold", 20))
    self.name_irrigation.grid(row=0, column=0, sticky="nsew")
    self.plant_irrigation = customtkinter.CTkLabel(self.text_frame, text="", anchor="w")
    self.plant_irrigation.grid(row=1, column=0, sticky="nsew")
    self.type_irrigation = customtkinter.CTkLabel(self.text_frame, text="", anchor="w")
    self.type_irrigation.grid(row=3, column=0, sticky="nsew")
    self.date_irrigation = customtkinter.CTkLabel(self.text_frame, text="", anchor="w")
    self.date_irrigation.grid(row=4, column=0, sticky="nsew")
    
    self.image_frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
    self.image_frame.grid(row=0, column=1, padx=20, sticky="nsew")
    
    
    
  def load_data(self):
    self.data = self.parent.task.system.current_irrigation
    
    if self.data:
      self.name = self.data['name']
      self.plant = self.data['plant']
      self.type = "Tưới theo thời gian" if self.data['type'] == 2 else "Tưới theo điều kiện cảm biến"
      self.startTime = convert_time(self.data['startTime'])
      self.activities = self.data['activities']
      self.image_src = self.data['avatar']
      self.activities = self.filter_activities(self.data['activities'])
      
      response = requests.get(f'{BASE_URL}/img/{self.image_src}')
      self.image = Image.open(BytesIO(response.content))
      self.photo = customtkinter.CTkImage(self.image, size=(320, 200))
      
      self.image_label = customtkinter.CTkLabel(self.image_frame, text="", image=self.photo)
      self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
      
      # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assets")
      # self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "photo.jpg")), size=(320, 200))
      # self.home_frame_large_image_label = customtkinter.CTkLabel(self.image_frame, text="", image=self.large_test_image)
      # self.home_frame_large_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
      
      self.name_irrigation.configure(text=f"{self.name}")
      self.plant_irrigation.configure(text=f"Loại cây trồng: {self.plant}")
      self.type_irrigation.configure(text=f"Kiểu lịch: {self.type}")
      self.date_irrigation.configure(text=f"Ngay bat dau: {self.startTime}")
      
      
      # self.name_irrigation = customtkinter.CTkLabel(self.text_frame, text=f"{self.name}", anchor="w", font=("Montserrat Bold", 20))
      # self.name_irrigation.grid(row=0, column=0, sticky="nsew")
      # self.plant_irrigation = customtkinter.CTkLabel(self.text_frame, text=f"Loại cây trồng: {self.plant}", anchor="w")
      # self.plant_irrigation.grid(row=1, column=0, sticky="nsew")
      # self.type_irrigation = customtkinter.CTkLabel(self.text_frame, text=f"Kiểu lịch: {self.type}", anchor="w")
      # self.type_irrigation.grid(row=3, column=0, sticky="nsew")
      # self.date_irrigation = customtkinter.CTkLabel(self.text_frame, text=f"Ngay bat dau: {self.startTime}", anchor="w")
      # self.date_irrigation.grid(row=4, column=0, sticky="nsew")
      
      if self.data['type'] == 1:
        thresholdTemp = self.data['thresholdSoilTemperature']
        thresholdHumi = self.data['thresholdSoilHumidity']
        thresholdPH = self.data['thresholdSoilPH']
        thresholdEC = self.data['thresholdSoilEC']
        thresholdN = self.data['thresholdSoilN']
        thresholdP = self.data['thresholdSoilP']
        thresholdK = self.data['thresholdSoilK']
        
        self.type_frame = customtkinter.CTkFrame(self.text_frame)
        self.type_frame.grid(row=5, column=0, sticky='nsew')
        
        self.title_threshold = customtkinter.CTkLabel(self.type_frame, text="Ngưỡng cảm biến")
        self.title_threshold.grid(row=0, column=0, sticky="nsew")
        
        self.thresholdSoilTemperature = customtkinter.CTkLabel(self.type_frame, text=f"Nhiệt độ: {thresholdTemp}°C")
        self.thresholdSoilTemperature.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.thresholdSoilHumidity = customtkinter.CTkLabel(self.type_frame, text=f"Độ ẩm: {thresholdHumi}%")
        self.thresholdSoilHumidity.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.thresholdSoilPH = customtkinter.CTkLabel(self.type_frame, text=f"PH: {thresholdPH}")
        self.thresholdSoilPH.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.thresholdSoilEC = customtkinter.CTkLabel(self.type_frame, text=f"EC: {thresholdEC}")
        self.thresholdSoilEC.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.thresholdSoilN = customtkinter.CTkLabel(self.type_frame, text=f"N: {thresholdN}")
        self.thresholdSoilN.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.thresholdSoilP = customtkinter.CTkLabel(self.type_frame, text=f"P: {thresholdP}")
        self.thresholdSoilP.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.thresholdSoilK = customtkinter.CTkLabel(self.type_frame, text=f"K: {thresholdK}")
        self.thresholdSoilK.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        
      self.scrollable_frame = customtkinter.CTkFrame(self.main_frame,fg_color='#1890ff')
      self.scrollable_frame.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")
      self.scrollable_frame.grid_columnconfigure(0, weight=1)
      
      self.date_filter = customtkinter.CTkScrollableFrame(self.scrollable_frame, width=200, label_text="Các ngày tưới tiêu", fg_color='white')
      self.date_filter.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")
      self.date_filter.grid_columnconfigure((0, 1, 2), weight=1)
      
      for i, item in enumerate(self.activities):
        self.count_title = customtkinter.CTkLabel(self.date_filter, text=f"{i}")
        self.count_title.grid(row=i, column=0, pady=5, sticky="nsew")
        self.title = customtkinter.CTkLabel(self.date_filter, text=f"Ngày {item}")
        self.title.grid(row=i, column=1, pady=10, sticky="nsew")
        self.action = customtkinter.CTkButton(self.date_filter, width=5, text="Xem", fg_color='blue')
        self.action.grid(row=i, column=2, pady=5, sticky="nsew")
        self.action.bind("<Button-1>",command=lambda event, action=self.action, item=item: self.load_detail_activities(item, action) )
      
      self.detail_acticity = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=6, width=400, fg_color='white')
      self.detail_acticity.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="nsew")
      self.detail_acticity.grid_columnconfigure(0, weight=1)
      self.detail_acticity.grid_rowconfigure((1), weight=1)
      self.detail_acticity.grid_propagate(0)
      
      self.heading_frame = customtkinter.CTkFrame(self.detail_acticity, corner_radius=6)
      self.heading_frame.grid(row=0, column=0, sticky="nsew")
      self.heading_frame.grid_columnconfigure((0, 1, 2), weight=1)
      
      self.label_start = customtkinter.CTkLabel(self.heading_frame, text="Bắt đầu")
      self.label_start.grid(row=0, column=0, sticky="ns")
      self.label_end = customtkinter.CTkLabel(self.heading_frame, text="Kết thúc")
      self.label_end.grid(row=0, column=1, sticky="ns")
      self.label_status = customtkinter.CTkLabel(self.heading_frame, text="Trạng thái")
      self.label_status.grid(row=0, column=2, sticky="ns")
      
      self.table_frame = customtkinter.CTkScrollableFrame(self.detail_acticity, fg_color='transparent')
      self.table_frame.grid(row=1, column=0, sticky="nsew")
      
      self.label_1.destroy()
      
    else:
      self.label_1 = customtkinter.CTkLabel(self.main_frame, text="Không có dữ liệu", anchor="w")
      self.label_1.grid(row=0, column=0, padx=20, pady=(10, 0))
      
  def load_detail_activities(self, select, action):
    for item in self.detail_label:
      item.destroy()
      
    if select in self.activities:
      if self.select_activity:
        self.select_activity.configure(fg_color="blue")
      self.select_activity = action
      action.configure(fg_color="green")
      for i, obj in enumerate(self.activities[select]):
        status = obj['status']
        startTime = convert_to_time(obj['startAt'])
        endTime = convert_to_time(obj['endAt'])
        self.start_label = customtkinter.CTkLabel(self.table_frame, text=f"{startTime}")
        self.start_label.grid(row=i, column=0, padx=42, pady=5, sticky="ns")
        self.end_label = customtkinter.CTkLabel(self.table_frame, text=f"{endTime}")
        self.end_label.grid(row=i, column=1, padx=55, pady=5, sticky="ns")
        self.status_label = customtkinter.CTkLabel(self.table_frame, text=f"{startTime}", text_color="white", corner_radius=20)
        self.status_label.grid(row=i, column=2, padx=(20, 25), pady=5, sticky="ns")
        
        if status==2:
          self.status_label.configure(text="Hoàn thành", fg_color='green')
        else:
          self.status_label.configure(text="Đang chờ", fg_color='blue')
        
        self.detail_label.append(self.start_label)
        self.detail_label.append(self.end_label)
        self.detail_label.append(self.status_label)
    
  def filter_activities(self, data):
    data.sort(key=lambda x: convert_time(x['startAt']))
    result = {}
    for date, group in groupby(data, key=lambda x: convert_time(x['startAt'])):
      result[date] = list(group)
    return result