import socket

from kivy.app import App 
 
from kivy.config import Config  
  
WIDTH = '300'  
HEIGHT = '500'  
  
Config.set('graphics', 'resizable', '0')  
Config.set('graphics', 'width', WIDTH)  
Config.set('graphics', 'height', HEIGHT)  
  
from kivy.core.window import Window  
  
from kivy.graphics import (Color, Rectangle)  
  
from kivy.uix.button import Button  
from kivy.uix.widget import Widget  
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout  
  
from pyautogui import click 
from pyautogui import moveRel  

import asyncio
  
"""  
CONSTS  
SPEED_CURSOR - speed of move the windows's, linux's cursor  
WIDTH window  
HEIGHT window  
"""  
SPEED_CURSOR = 30 
  


class Ip(BoxLayout):
    """GUI for working with a given IP address"""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'  
        self.ip = None
        self.port = 5050

        self.label = Label(
            font_name="Roboto",
            font_size=20,
            text="IPv4",
            size_hint=(None, None),
            size=(10, 30),
            pos_hint={"center_x": 0, "center_y": 0.1}
        )
        self.add_widget(self.label)

        self.text_input = TextInput(
            multiline=False,
            pos_hint={"center_x": 0.2, "center_y": 0.1},
            size_hint=(None, None),
            font_size=15,
            size=(200, 30)
        )
        self.add_widget(self.text_input)

        self.button = Button(
            font_size=20,
            text="OK",
            pos_hint={"center_x": 0.2, "center_y": 0.1},
            size_hint=(None, None),
            size=(30, 30),
            on_press = self.on_button_click
        )
        self.add_widget(self.button)


    def connect_to_server(self, ip):
        """Set connection by ip"""
        try:
            with socket.create_connection((ip, self.port), timeout=5) as sock:
                print(f"Connection with {ip}:{self.port}")
        except Exception as e:
            print(f"Error connection: {e}\nData of ip will destroy")
            self.ip = ""
            self.text_input.text = ""


    def on_button_click(self, instance):
        """Checks the entered IP address.
           If the the entered ip adress has valid form keeped the self.ip if not display an error.
           The value can be deleted during the operetions.   
        """
        unvalide_ip = (self.text_input.text).split(".")
        if len(unvalide_ip) == 4: 
            self.connect_to_server(self.ip)
            self.ip = self.text_input.text
            print("I saved ip")
        else:
            print("Error 1\nIncorrect format ip")
  


class Program(App):  
    """                                 
    ░░██░░░░███░░░░░█░░░░░░░░█░░█░░░░░░░█░  
    ░░███░░██░█░░░░███░░░░░░░█░░███░░░░░█░  
    ░░█░██░█░░██░░░█░░█░░░░░░█░░█░██░░░░█░  
    ░░█░░███░░░█░░█░░░░█░░░░░█░░█░░██░░░█░  
    ░░█░░░░░░░░█░░█░░░░██░░░░█░░█░░░██░░█░  
    ░░█░░░░░░░░█░░███████░░░░█░░█░░░░██░█░  
    ░░█░░░░░░░░█░░█░░░░░░█░░░█░░█░░░░░█░█░  
    ░░█░░░░░░░░█░░█░░░░░░█░░░█░░█░░░░░░██░   
    """  
     
    def build(self) -> None:  
        """Build element gui "↑", "←", "→", "↓" to control cursor""" 
        Window.bind(on_key_down=self.on_key_down)  
         
        root = BoxLayout(pos=(25, 200), orientation='vertical', spacing = 1, padding = 1) 

        # add buttons top, left, right, bottom to app 

        gl = GridLayout(rows = 3, size_hint=(None, None), size=(250, 250), pos = (25, 200), spacing = 15)  
        signs = {  
            "↑": "up",  
            "←": "left",  
            "→": "right",  
            "↓": "bottom"  
        }  
        accept = False  
        INDEX_WITH_EMPTYWIDGET = 9  
        for i in range(INDEX_WITH_EMPTYWIDGET):  
            if accept:  
                sign_key = next(iter(signs))   
                action = signs[sign_key]  
  
                del signs[sign_key]  
                  
                sign_key = Button(text = sign_key, font_name="DejaVuSans", font_size = 30, on_press=self.button_on_press)  
                  
                gl.add_widget(sign_key)  
  
                accept = False   
                  
                del sign_key  
            elif i == 4: 
                gl.add_widget(Button(text = "CLICK", on_press=self.clickm)) 
                accept = True 
            else:  
                gl.add_widget(Widget())  
                accept = True  

        # create object of gui classes 
        self.ip = Ip()
        
        # Add elements to root widget  
        root.add_widget(self.ip)
        root.add_widget(gl) 

        return root 
    

    


    def clickm(self, instance : None) -> None: 
        """Handles computer's click""" 
        print("space") 
        click() 


    def move(self, direction: str) -> None: 
      """ 
      Handles movement based on the direction string. 
      :param direction: One of 'up', 'down', 'left', 'right' 
      """ 
      print(self.ip.ip)
      if direction == "up": 
          moveRel(0, -SPEED_CURSOR) 
      elif direction == "down": 
          moveRel(0, SPEED_CURSOR) 
      elif direction == "left": 
          moveRel(-SPEED_CURSOR, 0) 
      elif direction == "right": 
          moveRel(SPEED_CURSOR, 0) 
      # For special on_key_down function the condition 
      else: 
          self.clickm(None) 
     
    def on_key_down(self, instance, keyboard, keycode, text, modifiers): 
      """ 
      Handling keys from player's keyboard. 
      """ 
      key_to_direction = { 
          "w": "up", 
          "s": "down", 
          "a": "left", 
          "d": "right", 
          "f": "click" 
      } 
      if text in key_to_direction: 
          self.move(key_to_direction[text]) 
 
    def button_on_press(self, instance) -> None: 
      """ 
      Handling clicks in the GUI. 
      """ 
      button_to_direction = { 
          "↑": "up", 
          "↓": "down", 
          "←": "left", 
          "→": "right", 
      } 
      if instance.text in button_to_direction: 
          self.move(button_to_direction[instance.text]) 
  
  
  
if __name__ == "__main__":  
    Program().run()