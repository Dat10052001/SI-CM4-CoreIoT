import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage, CTkProgressBar, CTkOptionMenu, StringVar
from PIL import Image
import os
from utils import *
from constant import *
from datetime import datetime

class Home(CTkFrame):
  def __init__(self, parent, controller=None,*args, **kwargs):
    CTkFrame.__init__(self, parent,*args, **kwargs)
    self.parent = parent
    self.irrigation = []
    self.pre_sensor = None
    self.sensor_data = [0, 0, 0, 0, 0, 0, 0]
    self.select_sensor = TEMP
    
    self.name_irrigation = ""
    self.plant_irrigation = ""
    self.type_irrigation = "Riêng tư"
    self.plant_time_irrigation = ""
    self.start_time_irrigation = ""
    self.method_irrigation = ""
    #transparent
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    
    self.main_frame = CTkFrame(self, width=740, fg_color='transparent')
    self.main_frame.grid(row=0, column=0, padx=(15, 10), pady=(10, 10), sticky="nsew")
    self.main_frame.grid_columnconfigure(0, weight=1)
    # self.main_frame.grid_rowconfigure(0, weight=1)
    self.main_frame.grid_rowconfigure(1, weight=1)
    self.main_frame.grid_propagate(0)
    
    self.irrigation_frame = CTkFrame(self.main_frame, fg_color="transparent")
    self.irrigation_frame.grid(row=0, column=0, sticky="nsew")
    # self.irrigation_frame.grid_columnconfigure((0, 1), weight=2)
    self.irrigation_frame.grid_rowconfigure(0, weight=1)
    
    self.history_frame = CTkFrame(self.main_frame, fg_color="transparent")
    self.history_frame.grid(row=1, column=0, sticky="nsew")
    self.history_frame.grid_columnconfigure(0, weight=1)
    self.history_frame.grid_rowconfigure(0, weight=2)
    
    self.content_frame = CTkFrame(self.irrigation_frame, corner_radius=6, width=365, fg_color='white')
    self.content_frame.grid(row=0, column=0, sticky="nsew")
    self.content_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    self.content_frame.grid_columnconfigure(0, weight=1)
    self.content_frame.grid_propagate(0)
    
    self.activity_frame = CTkFrame(self.irrigation_frame, corner_radius=6, width=365, fg_color='white')
    self.activity_frame.grid(row=0, column=1, padx=15, sticky="nsew")
    self.activity_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    self.activity_frame.grid_columnconfigure(0, weight=1)
    self.activity_frame.grid_propagate(0)
    
    self.graph_frame = CTkFrame(self.history_frame, corner_radius=6, width=745, fg_color='white')
    self.graph_frame.grid(row=0, column=0, pady=(10, 0), sticky="nsew")
    self.graph_frame.grid_columnconfigure(0, weight=1)
    self.graph_frame.grid_rowconfigure(0, weight=1)
    self.graph_frame.grid_rowconfigure(1, weight=2)
    # self.graph_frame.grid_propagate(0)
    
    self.sensor_frame = CTkFrame(self.parent.right_frame, width=240, height=500, corner_radius=6, fg_color='#1890ff')
    self.sensor_frame.grid(row=1, column=0, pady=(10, 10), padx=(0, 10), sticky="nsew")
    self.sensor_frame.grid_columnconfigure(0, weight=1)
    self.sensor_frame.grid_rowconfigure(1, weight=1)
    # self.sensor_frame.grid_propagate(0)
    
    self.title_frame = CTkFrame(self.content_frame, fg_color="transparent")
    self.title_frame.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew")
    self.title_frame.grid_columnconfigure((0, 1), weight=1)
    self.current_irrigation = CTkLabel(self.title_frame, text="Lịch tưới cây hiện tại", font=("Montserrat Bold", 20 * -1), anchor="w")
    self.current_irrigation.grid(row=0, column=0, sticky="nsew")
    self.button_detail = CTkButton(self.title_frame, text="Chi tiết", width=55)
    
    self.name_current_irrigation = CTkLabel(self.content_frame, text="", anchor="w")
    self.name_current_irrigation.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="nsew")
    
    self.plant_name_current_irrigation = CTkLabel(self.content_frame, text="", anchor="w")
    self.plant_name_current_irrigation.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="nsew")
    
    self.time_current_irrigation = CTkLabel(self.content_frame, text="", anchor="w")
    self.time_current_irrigation.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="nsew")
    
    self.type_current_irrigation = CTkLabel(self.content_frame, text="", anchor="w")
    self.type_current_irrigation.grid(row=4, column=0, padx=20, pady=(5, 0), sticky="nsew")

    self.plant_time_current_irrigation = CTkLabel(self.content_frame, text="", anchor="w")
    self.plant_time_current_irrigation.grid(row=5, column=0, padx=20, pady=(5, 8), sticky="nsew")
    
    
    
    # ========================================= #
    self.activity = []
    
    self.activity_irrigation = CTkLabel(self.activity_frame, text="Hoạt động tưới hiện tại", font=("Montserrat Bold", 20 * -1), anchor="w")
    self.activity_irrigation.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
    
    self.name_activity_irrigation = CTkLabel(self.activity_frame, text="", anchor="w")
    self.name_activity_irrigation.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")
    
    self.state_frame = CTkFrame(self.activity_frame, fg_color="transparent")
    self.state_frame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")
    # self.state_frame.grid_columnconfigure((0, 1), weight=1)
    self.state_activity_title = CTkLabel(self.state_frame, text="", anchor='w')
    self.state_activity_title.grid(row=0, column=0, sticky="nsew")
    self.state_activity = CTkLabel(self.state_frame, text="", corner_radius=20, text_color="white")
    self.state_activity.grid(row=0, column=1, padx= (10, 0), sticky="nsew")
    
    self.start_activity_irrigation = CTkLabel(self.activity_frame, text="", anchor="w")
    self.start_activity_irrigation.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nsew")
    
    self.end_activity_irrigation = CTkLabel(self.activity_frame, text="", anchor="w")
    self.end_activity_irrigation.grid(row=4, column=0, padx=10, pady=(5, 0), sticky="nsew")
    
    self.proccess_frame = CTkFrame(self.activity_frame, fg_color="transparent")
    self.proccess_frame.grid(row=5, column=0, padx=10, sticky="nsew")
    self.proccess_frame.grid_columnconfigure((0, 1, 2), weight=1)
    
    self.proccess_activity_irrigation = CTkLabel(self.proccess_frame, text="", anchor="w")
    self.proccess_activity_irrigation.grid(row=0, column=0, pady=(5, 8), sticky="nsew")
    
    self.progressbar = CTkProgressBar(self.proccess_frame)
    self.progressbar.grid(row=0, column=1, padx=(20, 10), pady=(10, 8), sticky="ew")
    
    self.precent_text = CTkLabel(self.proccess_frame, text="")
    self.precent_text.grid(row=0, column=2, pady=(5, 8), sticky="nsew")
    
    self.activity_info = CTkLabel(self.activity_frame, text="", anchor="w", font=("Montserrat Bold", 18 * -1),)
    self.activity_info.grid(row=2, column=0, padx=10, pady=(5, 0),)
    
    #--------GRAPH--------#
    
    self.graph_content_frame = CTkFrame(self.graph_frame, fg_color="transparent")
    self.graph_content_frame.grid(row=0, column=0)
    # self.graph_content_frame.grid_rowconfigure(0, weight=1)
    # self.graph_content_frame.grid_columnconfigure((0, 1), weight=1)
    
    self.graph_title = CTkLabel(self.graph_content_frame, text="Lịch sử nhiệt độ", font=("Montserrat Bold", 20 * -1))
    self.graph_title.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
    
    # Create a Frame for the chart
    chart_frame = CTkFrame(self.graph_frame, fg_color="transparent")
    chart_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
    chart_frame.columnconfigure(0, weight=1)
    chart_frame.rowconfigure(0, weight=1)
    # Create a chart
    self.fig = Figure(figsize=(7.8, 3.5))
    self.ax = self.fig.add_subplot(111)
    self.x_data = []
    self.y_data = []
    self.select_data = [row[self.select_sensor] for row in self.y_data]
    
    xfmt = mdates.DateFormatter('%H:%M:%S')
    self.ax.xaxis.set_major_formatter(xfmt)
    
    self.line, = self.ax.plot(self.x_data, self.select_data, color='b')
    self.ax.set_ylabel("Giá trị")
    self.ax.tick_params(axis='x', rotation=5)
    
    self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
    self.canvas_widget = self.canvas.get_tk_widget()
    self.canvas_widget.grid(row=0, column=0, sticky='nsew')
    
    #-----------SENSOR----------#

    self.title_sensor = CTkLabel(self.sensor_frame, text="Đất trồng", text_color="white", font=("Montserrat Bold", 20 * -1))
    self.title_sensor.grid(row=0, column=0, padx=10, pady=10)
    self.data_sensor_frame = CTkFrame(self.sensor_frame, fg_color="transparent")
    self.data_sensor_frame.grid(row=1, column=0, padx=10, sticky="nsew")
    self.data_sensor_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    self.data_sensor_frame.grid_columnconfigure(0, weight=1)
    self.sensor_value = []
    for i in range(7):
        self.child_frame = CTkFrame(self.data_sensor_frame, width=200, height=56, fg_color='white')
        self.child_frame.grid(row = i, column = 0, sticky="nsew", padx=(10, 10), pady=(0, 8))
        self.child_frame.bind("<Button>", self.on_click_change(self.child_frame, i))
        
        self.sensor_value.append(self.child_frame)
    
    self.temp_label = CTkLabel(self.sensor_value[TEMP], text="Nhiệt độ (°C)", anchor='e' , font=("Montserrat Bold", 14))
    self.temp_label.place(relx=0.5, rely=0.15, anchor="center")
    self.temp_value = CTkLabel(self.sensor_value[TEMP], text=f"{self.sensor_data[TEMP]}", font=("Montserrat", 16))
    self.temp_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.humi_label = CTkLabel(self.sensor_value[HUMI], text="Độ ẩm (%)", anchor='e' , font=("Montserrat Bold", 14))
    self.humi_label.place(relx=0.5, rely=0.15, anchor="center")
    self.humi_value = CTkLabel(self.sensor_value[HUMI], text=f"{self.sensor_data[HUMI]}%", font=("Montserrat", 16))
    self.humi_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.ph_label = CTkLabel(self.sensor_value[PH], text="PH", anchor='e' , font=("Montserrat Bold", 14))
    self.ph_label.place(relx=0.5, rely=0.15, anchor="center")
    self.ph_value = CTkLabel(self.sensor_value[PH], text=f"{self.sensor_data[PH]}", font=("Montserrat", 16))
    self.ph_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.ec_label = CTkLabel(self.sensor_value[EC], text="Độ dẫn điện (ppm)", anchor='e' , font=("Montserrat Bold", 14))
    self.ec_label.place(relx=0.5, rely=0.15, anchor="center")
    self.ec_value = CTkLabel(self.sensor_value[EC], text=f"{self.sensor_data[EC]}", font=("Montserrat", 16))
    self.ec_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.n_label = CTkLabel(self.sensor_value[N], text="Nati", anchor='e' , font=("Montserrat Bold", 14))
    self.n_label.place(relx=0.5, rely=0.15, anchor="center")
    self.n_value = CTkLabel(self.sensor_value[N], text=f"{self.sensor_data[N]}", font=("Montserrat", 16))
    self.n_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.p_label = CTkLabel(self.sensor_value[P], text="Photpho", anchor='e' , font=("Montserrat Bold", 14))
    self.p_label.place(relx=0.5, rely=0.15, anchor="center")
    self.p_value = CTkLabel(self.sensor_value[P], text=f"{self.sensor_data[P]}", font=("Montserrat", 16))
    self.p_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.k_label = CTkLabel(self.sensor_value[K], text="Kali", anchor='e' , font=("Montserrat Bold", 14))
    self.k_label.place(relx=0.5, rely=0.15, anchor="center")
    self.k_value = CTkLabel(self.sensor_value[K], text=f"{self.sensor_data[K]}", font=("Montserrat", 16))
    self.k_value.place(relx=0.5, rely=0.6 , anchor="center")
    
    self.none_irrigation_frame = CTkFrame(self.content_frame, fg_color='transparent')
    self.none_irrigation_frame.grid(row=3, column=0)
    self.none_irrigation_text = CTkLabel(self.none_irrigation_frame, text="Đang tải")
    self.none_irrigation_text.grid(row=0, column=0)
    
    self.none_activity_frame = CTkFrame(self.activity_frame, fg_color='transparent')
    self.none_activity_frame.grid(row=3, column=0)
    self.none_activity_text = CTkLabel(self.none_activity_frame, text="Đang tải")
    self.none_activity_text.grid(row=0, column=0)
    
    self.sensor_value[TEMP].configure(fg_color='#b7e892')
    self.update_data()
    
  def update_data(self):
    self.sensor_data = self.parent.task.system.sensor_data
    self.irrigation = self.parent.task.system.current_irrigation
    self.activity = self.parent.task.system.current_activity
    self.history_sensor = self.parent.task.system.history_sensor
    self.isRunning = self.parent.task.system.isRunning
    self.update_chart(self.history_sensor)

    self.temp_value.configure(text=f"{self.sensor_data[TEMP]}")
    self.humi_value.configure(text=f"{self.sensor_data[HUMI]}")
    self.ph_value.configure(text=f"{self.sensor_data[PH]}")
    self.ec_value.configure(text=f"{self.sensor_data[EC]}")
    self.n_value.configure(text=f"{self.sensor_data[N]}")
    self.p_value.configure(text=f"{self.sensor_data[P]}")
    self.k_value.configure(text=f"{self.sensor_data[K]}")

    if len(self.irrigation):
      self.id_irrigation = self.irrigation['id']
      self.name_irrigation = self.irrigation['name']
      self.plant_irrigation = self.irrigation['plant']
      self.plant_time_irrigation = self.irrigation['plantingTime']
      self.start_time_irrigation = convert_time(self.irrigation['startTime'])
      self.method_irrigation = "Tưới theo thời gian" if self.irrigation['type']==2 else "Tưới theo điều kiện cảm biến"
      
      self.none_irrigation_text.configure(text="")
      
      self.name_current_irrigation.configure(text=f"{self.name_irrigation}")
      self.button_detail.configure(command=self.parent.btn_event)
      self.button_detail.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
      
      self.plant_name_current_irrigation.configure(text=f"Cây trồng: {self.plant_irrigation}")
      self.time_current_irrigation.configure(text=f"Thời gian bắt đầu: {self.start_time_irrigation}")
      self.type_current_irrigation.configure(text=f"Chế độ tưới: {self.method_irrigation}")
      self.plant_time_current_irrigation.configure(text=f"Thời gian trồng: {self.plant_time_irrigation}")
    else:
      self.name_current_irrigation.configure(text="")
      self.button_detail.configure(command=())
      self.button_detail.grid_remove()
      self.plant_name_current_irrigation.configure(text="")
      self.time_current_irrigation.configure(text="")
      self.type_current_irrigation.configure(text="")
      self.plant_time_current_irrigation.configure(text="")
      self.none_irrigation_text.configure(text="Không có lịch tưới nào hoạt động")
    
    if len(self.activity):
      self.name_activity = self.activity['name']
      self.start_activity = format_time(self.activity['startAt'])
      self.end_activity = format_time(self.activity['endAt'])
      self.progressStatus_activity = self.activity['progressStatus']
      self.status_activity = self.activity['status']
      
      self.none_activity_text.configure(text="")
      
      self.name_activity_irrigation.configure(text=f"{self.name_activity}")
      self.state_activity_title.configure(text="Trạng thái:")
      if self.isRunning:
        self.state_activity.configure(text=f"Đang chạy", fg_color="green")
      else:
        self.state_activity.configure(text=f"Đang chờ", fg_color="blue")
      self.start_activity_irrigation.configure(text=f"Bắt đầu: {self.start_activity}")
      self.end_activity_irrigation.configure(text=f"Kết thúc: {self.end_activity}")
      self.proccess_activity_irrigation.configure(text="Tiến độ:")
      self.progressStatus_activity = self.activity['progressStatus']
      self.progressbar.set(self.progressStatus_activity / 100)
      self.progressbar.grid(row=0, column=1, padx=(20, 10), pady=(5, 8), sticky="ew")
      self.precent_text.configure(text=f'{self.progressStatus_activity}%')
    else:
      self.progressbar.grid_remove()
      self.name_activity_irrigation.configure(text="")
      self.state_activity_title.configure(text="")
      self.state_activity.configure(text="", fg_color="white")
      self.start_activity_irrigation.configure(text="")
      self.end_activity_irrigation.configure(text="")
      self.proccess_activity_irrigation.configure(text="")
      self.precent_text.configure(text='')
      self.none_activity_text.configure(text="Không có hoạt động")
    
    self.after(1000, self.update_data)
    
  def update_chart(self, data):
    if data:
      sensor_value = data['data']
      tmp = data['time'].strftime('%H:%M:%S')
      # time = datetime.strptime(f"{tmp}", "%H:%M:%S")
      
      if self.pre_sensor and self.pre_sensor['time'] != data['time']:
      
        self.x_data.append(tmp)
        # self.y_data.append(sensor_value[self.select_sensor])
        self.y_data.append(sensor_value)
        self.select_data = [row[self.select_sensor] for row in self.y_data]
        
        self.x_data = self.x_data[-15:]
        self.y_data = self.y_data[-15:]
        self.select_data = self.select_data[-15:]
        
        self.line.set_xdata(range(len(self.x_data)))
        self.line.set_ydata(self.select_data)
        # self.ax.set_xlim(0, len(self.x_data))
        # if len(set(self.y_data)) > 1:  # Check if there is variation in y values
        #     self.ax.set_ylim(min(self.y_data), max(self.y_data))
        self.ax.set_xticks(range(len(self.x_data)))
        self.ax.set_xticklabels(self.x_data, rotation=15, ha='right')
        
        # self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
      self.pre_sensor = data
  
  def on_click_change(self, frame, type):
    return lambda event: self.change_select_sensor(frame, type)
  
  def change_select_sensor(self, frame, type):
    for item in self.sensor_value:
      item.configure(fg_color="white")
    
    if self.select_sensor != type:
      self.select_sensor = type
      frame.configure(fg_color="#b7e892")
    
    if self.select_sensor==TEMP:
      self.graph_title.configure(text="Lịch sử nhiệt độ")
    elif self.select_sensor==HUMI:
      self.graph_title.configure(text="Lịch sử độ ẩm")
    elif self.select_sensor==PH:
      self.graph_title.configure(text="Lịch sử pH")
    elif self.select_sensor==EC:
      self.graph_title.configure(text="Lịch sử độ dẫn điện")
    elif self.select_sensor==N:
      self.graph_title.configure(text="Lịch sử nitor")
    elif self.select_sensor==P:
      self.graph_title.configure(text="Lịch sử photpho")
    elif self.select_sensor==K:
      self.graph_title.configure(text="Lịch sử kali")
      
    # self.x_data = []
    # self.y_data = []
    self.select_data = [row[self.select_sensor] for row in self.y_data]
  
  def lay_phan_tu_theo_cot(arr, index):
    return [row[index] for row in arr]

    
  def load_data(self):
    # self.parent.task.system.reload_data_irrigation()
    pass