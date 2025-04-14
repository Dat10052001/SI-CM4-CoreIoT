from tkinter import *
from customtkinter import CTkButton, CTkImage, CTkLabel
import os
from PIL import Image

class ToggleButton:
    is_on = False
    on = NONE
    off = NONE
    on_click_event = NONE
    on_button = NONE

    def toggle_button_click(self, e):
        if self.is_on:
            self.on_button.configure(image=self.off)
            self.is_on = False

        else:
            self.on_button.configure(image=self.on)
            self.is_on = True

        self.on_click_event(self.is_on)
    
    def update_button_click(self, state):
        self.is_on = state
        if self.is_on:
            self.on_button.configure(image=self.on)
            self.is_on = True
        else:
            self.on_button.configure(image=self.off)
            self.is_on = False

    def __init__(self, win):
      image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

      self.on = CTkImage(light_image=Image.open(os.path.join(image_path, "on_button_xl.png")), size=(80, 80))
      self.off = CTkImage(light_image=Image.open(os.path.join(image_path, "off_button_xl.png")), size=(80, 80))

      # self.on = PhotoImage(file="app/assets/on_button_m.png")
      # self.off = PhotoImage(file="app/assets/off_button_m.png")

      self.is_on = False
      self.on_button = CTkLabel(win, image=self.off, text="")
      self.on_button.bind('<Button>', self.toggle_button_click)

    def setClickEvent(self, func):
        self.on_click_event = func

    def button_place(self, row, column):
        self.on_button.grid(row = row, column= column)