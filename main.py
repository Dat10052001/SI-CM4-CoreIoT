from customtkinter import *
from main_window import MainWindow
from app.login import Login
from threading import Thread
from app.control_system import Control_System
from scheduler import TaskManagament

set_appearance_mode("light")
set_default_color_theme("blue")

WIDTH = 1024 #1024
HEIGTH = 600 # 600
class App(CTk):
  def __init__(self):
    super().__init__()
    self.title("Irrigation System")
    self.geometry(f"{WIDTH}x{HEIGTH}")
    # self.overrideredirect(True)
    self.attributes("-fullscreen", True)
    self.resizable(0, 0)
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.task = TaskManagament()
    
    self.main_frame = MainWindow(self, fg_color="transparent")
    self.login_frame = Login(self, fg_color="transparent")
    self.control_system = Control_System(self, fg_color="transparent")
    
    self.frames = {
      "main_window": self.main_frame,
      "login": self.login_frame,
      "control_system": self.control_system
    }
    
    self.select_frame_by_name("control_system")
  def select_frame_by_name(self, name):
    for frame in self.frames.values():
      frame.grid_forget()
      
    self.current_window = self.frames.get(name)
    
    if name=="main_window": 
      self.main_frame.load_app()
      self.main_frame.select_frame_by_name('home')
    
    self.frames[name].grid(row=0, column=0, sticky="nsew")

  def start_control_system(self):
        self.select_frame_by_name("control_system")
    
if __name__ == "__main__":
  app = App()
  app.attributes("-fullscreen", True)
  
  def on_closing():
    app.main_frame.closing()
    app.destroy()
  app.protocol("WM_DELETE_WINDOW", on_closing)
  app.mainloop()
  