from tkinter import messagebox
import customtkinter
# from IrrigationCloud import cloud
import os
from PIL import Image

class Login(customtkinter.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    self.configure(fg_color="#FFFFFF")
    
    self.parent = master
    self.data_email, self.data_password = self.load_credentials()
    self.show_password = customtkinter.BooleanVar()
    self.show_password.set(False)
    
    self.grid_columnconfigure(0, weight=2)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)
    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
    self.image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "banner.png")), size=(400, 600))
    
    self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
    self.main_frame.grid(row=0, column=0, sticky="nsew")
    self.main_frame.grid_columnconfigure(0, weight=1)
    # self.main_frame.grid_rowconfigure(0, weight=1)
    
    self.banner_frame = customtkinter.CTkFrame(self, fg_color="transparent")
    self.banner_frame.grid(row=0, column=1, sticky="nsew")
    self.banner_frame.grid_columnconfigure(0, weight=1)
    self.banner_frame.grid_rowconfigure(0, weight=1)
    
    self.banner = customtkinter.CTkLabel(self, text="", image=self.image).place(relx=1, rely=0.5, anchor="e")
    
    self.center_frame = customtkinter.CTkFrame(self.main_frame, width=350, height=390, fg_color="white")
    self.center_frame.grid(row=0, column=0, padx=(100, 250), pady=(50, 200), sticky="nsew")
    self.center_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
    self.center_frame.grid_columnconfigure(0, weight=1)
    
    # tabview
    # self.slider_progressbar_frame = customtkinter.CTkFrame(self.center_frame, fg_color="transparent")
    # self.slider_progressbar_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    # self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
    # self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
    # self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
    # self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    # self.seg_button_1.configure(values=["Đăng nhập", "QR Code"])
    # self.seg_button_1.set("Đăng nhập")
    
    self.heading = customtkinter.CTkLabel(self.center_frame, text="Mừng bạn đến với", text_color='#57a1f8', anchor="w", font=('Tahoma', 30, 'bold'))
    self.heading.grid(row=0, column=0, pady=(0,10), sticky="nsew")
    self.heading_name = customtkinter.CTkLabel(self.center_frame, text="WaterWise Planner", text_color='#57a1f8', anchor="w",
                    font=('Tahoma', 30, 'bold'))
    self.heading_name.grid(row=1, column=0, pady=(0,20), sticky="nsew")
    
    self.email_label = customtkinter.CTkLabel(self.center_frame, text="Email", anchor="w")
    self.email_label.grid(row=2, column=0, pady=(0,5), sticky="nsew")
    self.email = customtkinter.CTkEntry(self.center_frame, width=295, height=50, text_color='black', corner_radius=4,
                fg_color='white', placeholder_text="example@gmail.com", font=("Tahoma", 14 * -1))
    self.email.grid(row=3, column=0, pady=(0,10), sticky="nsew")
    self.email.insert(0, self.data_email)
    # self.email.bind('<FocusIn>', self.on_enter)
    self.email.bind('<FocusOut>', self.on_leave)
    
    self.password_label = customtkinter.CTkLabel(self.center_frame, text="Mật khẩu", anchor="w")
    self.password_label.grid(row=4, column=0, pady=(0,5), sticky="nsew")
    self.password = customtkinter.CTkEntry(self.center_frame, width=295, height=50, text_color='black', corner_radius=4,
                fg_color='white', placeholder_text="Nhập mật khẩu", font=("Tahoma", 14 * -1), show="*")
    self.password.grid(row=5, column=0, pady=(0,10), sticky="nsew")
    self.password.insert(0, self.data_password)
    # self.password.bind('<FocusIn>', self.on_enter_password)
    self.password.bind('<FocusOut>', self.on_leave_password)
    
    self.show_password_checkbox = customtkinter.CTkCheckBox(self.center_frame, text="Hiện mật khẩu", variable=self.show_password, command=self.toggle_password_visibility)
    self.show_password_checkbox.grid(row=6, column=0, pady=(0,10), sticky="nsew")
    
    self.btn_login = customtkinter.CTkButton(self.center_frame, width=290, height=50, text='Đăng Nhập',
          fg_color='#57a1f8', text_color='white', corner_radius=10, command=self.loginFunc)
    self.btn_login.grid(row=7, column=0, padx=20, pady=20, sticky="nsew")

    self.btn_exit = customtkinter.CTkButton(self.center_frame, width=70, height=50, text='Thoát ứng dụng',
          fg_color='red', hover_color='red', text_color='white', corner_radius=10, command=self.exit_app)
    self.btn_exit.grid(row=9, column=0, sticky='s')
  
  def toggle_password_visibility(self):
    if self.show_password.get():
      self.password.configure(show="")
    else:
      self.password.configure(show="*")
    
  def on_enter(self, e):
        self.email.delete(0, 'end')

  def on_leave(self, e):
        email = self.email.get()
        if email == '':
            self.email.insert(0, 'Email')
  def on_enter_password(self, e):
    self.password.delete(0, 'end')
    self.password.configure(show='*')  # Hiển thị dấu *

  def on_leave_password(self, e):
      name = self.password.get()
      if name == '':
          self.password.insert(0, 'Mật khẩu')
          self.password.configure(show='')  # Ẩn dấu *
  
  def loginFunc(self):
     self.parent.select_frame_by_name('main_window')
    # self.parent.select_frame_by_name('control')
    # body = {
    #   "email": self.email.get().strip(),
    #   "password": self.password.get().strip()
    # }
    # response = cloud.login(body=body)
    # if response == True:
    # #   self.save_credentials(body['email'], body['password'])
    # #   self.parent.select_frame_by_name('main_window')
    # else:
    #   messagebox.showerror(title="Error", message="Vui lòng kiểm tra thông tin và đăng nhập lại")
  
  def save_credentials(self, email, password):
    with open("credentials.txt", "w") as file:
      file.write(f"Email: {email}\n")
      file.write(f"Password: {password}\n")
        
  def load_credentials(self):
    if os.path.exists("credentials.txt"):
      with open("credentials.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 2:
          email = lines[0].split(": ")[1].strip()
          password = lines[1].split(": ")[1].strip()
          return email, password
    return "", ""
  
  def exit_app(self):
    self.parent.destroy()