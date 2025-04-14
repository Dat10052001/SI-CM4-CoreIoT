import customtkinter
from tkinter import messagebox
import os
from PIL import Image
from app.home import Home
from app.detail_irrigation import DetailIrrigation
from app.control_system import Control_System
from scheduler import TaskManagament
from threading import Thread
from constant import *

class MainWindow(customtkinter.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    self.parent = master
    self.configure(fg_color="#3849b3")
    self.current_window = ""
    self.isLogin = False

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    # load images with light and dark mode image
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "app/assets")
    self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
    self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
    
    self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")), size=(15, 15))
    self.home_image_click = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_light.png")), size=(15, 15))
    self.irrigation_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "detail_dark.png")), size=(20, 20))
    self.irrigation_image_click = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "detail_light.png")), size=(20, 20))
    self.logout_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "logout_dark.png")), size=(15, 15))
    self.logout_image_click = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "logout_light.png")), size=(15, 15))
    self.reload_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "reload_dark.png")), size=(15, 15))
    self.reload_image_click = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "reload_light.png")), size=(15, 15))

    self.left_frame = customtkinter.CTkFrame(self, corner_radius=0, width=760, fg_color="transparent")
    self.left_frame.grid(row=0, column=0, sticky="nsew")
    self.left_frame.grid_columnconfigure(0, weight=1)
    self.left_frame.grid_rowconfigure(0, weight=1)
    self.left_frame.grid_propagate(0)
    
    self.right_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
    self.right_frame.grid(row=0, column=1, sticky="nsew")
    self.right_frame.grid_rowconfigure((0, 1), weight=1)

    # create sidebar frame with widgets
    self.sidebar_frame = customtkinter.CTkFrame(self.right_frame, corner_radius=6, height=70, fg_color="transparent")
    self.sidebar_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(0, weight=1)
    self.sidebar_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    # self.sidebar_frame.grid_propagate(0)

    self.home_button = customtkinter.CTkLabel(self.sidebar_frame, image=self.home_image, text="", width=40, height=40, corner_radius=25, fg_color="white")
    self.home_button.grid(row=0, column=0, sticky="ew")
    self.home_button.bind("<Button>", self.home_button_event)
    
    self.irrigation_button = customtkinter.CTkLabel(self.sidebar_frame, image=self.irrigation_image, text="", width=40, height=40, corner_radius=25, fg_color="white")
    self.irrigation_button.grid(row=0, column=1, sticky="ew")
    self.irrigation_button.bind("<Button>", self.control_button_event)
    
    self.logout_button = customtkinter.CTkLabel(self.sidebar_frame, image=self.logout_image, text="", width=40, height=40, corner_radius=25, fg_color="white")
    self.logout_button.grid(row=0, column=2, sticky="ew")
    self.logout_button.bind("<Button>", self.logout)
    
    self.reload_button = customtkinter.CTkLabel(self.sidebar_frame, image=self.reload_image, text="", width=40, height=40, corner_radius=25, fg_color="white")
    self.reload_button.grid(row=0, column=3, sticky="ew")
    self.reload_button.bind("<Button>", self.reload_data)
    
    # self.windows = {
    #   "home": Home(self, fg_color="transparent"),
    #   "detail_irrigation": DetailIrrigation(self, fg_color="transparent")
    # }
    
    # set default page
    # self.select_frame_by_name("home")

  def select_frame_by_name(self, name):
    for window in self.windows.values():
      window.grid_forget()
      
    self.current_window = self.windows.get(name)
    
    if name == 'detail_irrigation': self.current_window.load_data()
    elif name == 'home' : self.current_window.load_data()
    elif name == 'control': self.current_window.update()

    self.windows[name].grid(row=0, column=0, sticky="nsew")

    # set button color for selected button
    self.home_button.configure(fg_color="#1890ff" if name == "home" else "white")
    self.home_button.configure(image=self.home_image_click if name == "home" else self.home_image)
    if name == 'control':
      self.irrigation_button.configure(fg_color="#1890ff", image=self.irrigation_image_click)
    else:
      self.irrigation_button.configure(fg_color="white", image=self.irrigation_image)
    

  def home_button_event(self, e):
    self.select_frame_by_name("home")
    
  def control_button_event(self, e):
    self.select_frame_by_name("control")

  def irrigation_page_button_event(self, e):
    self.select_frame_by_name("detail_irrigation")

  def logout(self, e):
    res = messagebox.askyesno("Warning", "Bạn muốn thoát tài khoản ?")
    if res:
      print("Logout!")
      self.task.system.reset_system()
      self.closing()
      self.parent.select_frame_by_name('login')
  
  def reload_data(self, e):
    self.task.system.reload_data_irrigation()
    
  def btn_event(self):
    self.select_frame_by_name("detail_irrigation")
  
  def load_app(self):
    self.isLogin = True
    self.task = TaskManagament()
    self.windows = {
      "home": Home(self, fg_color="transparent"),
      "control": Control_System(self, fg_color="transparent"),
      "detail_irrigation": DetailIrrigation(self, fg_color="transparent")
    }
    self.thread_1 = Thread(target=self.task.run) # irrigation task
    self.thread_1.start()
    
  def closing(self):
    if self.isLogin:
      self.task.scheduler_run = False
      self.isLogin = False