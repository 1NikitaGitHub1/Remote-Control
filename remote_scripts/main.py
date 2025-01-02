import json
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout  

import asyncio
  
"""  
CONSTS  
SPEED_CURSOR - speed of move the windows's, linux's cursor  
WIDTH window  
HEIGHT window  
"""  
SPEED_CURSOR = 30 
  
class BindLink(BoxLayout):
    """Bind Link Menu"""
    def __init__(self, client_socket, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client_socket = client_socket
        self.orientation = 'vertical'  
        self.pos_hint = {'x': 0.05, 'y': 0}
        self.size_hint = (0.9, 0.5)

        self.actionscr_boxlayout = BoxLayout(
            orientation='horizontal',
            pos_hint = {"top": 0.4},
            size_hint=(1, None),  
            height=self.height * 0.1,
        )
        
        self.bt_new = Button(
            text = "New",
            size_hint = (None, None), 
            size = (50, 20),
            on_press = self.add_link
        )
        self.actionscr_boxlayout.add_widget(self.bt_new)

        self.add_widget(self.actionscr_boxlayout)

        self.quick_lnk = ScrollView(
            size_hint = (1, 0.5)
        )
        self.list_of_link = BoxLayout(orientation='vertical', size_hint_y=None)  
        self.list_of_link.bind(minimum_height=self.list_of_link.setter('height'))  

        self.quick_lnk.add_widget(self.list_of_link)  

        self.add_widget(self.quick_lnk)

    def add_link(self, instance) -> None:
        """Add a new link bind to menu panel"""
        content = BoxLayout(orientation = 'vertical')
        close = Button(text="OK", size_hint = (1, 0.1))
        input_name = TextInput(hint_text="Enter web name", size_hint=(1, 0.2))
        input_link = TextInput(hint_text="Enter web's link")

        content.add_widget(input_name)
        content.add_widget(input_link)
        content.add_widget(close)

        popup = Popup(title='Add bind link',
        content = content,
        size_hint = (0.5, 0.5),
        auto_dismiss = False)

        def save_result_to_listoflink(instance) -> None:
            """Save button from values of data from input link and name and add commands to server.py"""
            data = ("ADD", input_name.text, input_link.text)
            self.client_socket.send(json.dumps(data).encode('utf-8'))
            self.list_of_link.add_widget(Button(
                text = input_name.text,
                on_press = lambda _: self.client_socket.send(input_name.text.encode('utf-8'))
            ))
            popup.dismiss()

        close.bind(on_press=save_result_to_listoflink)
        popup.open()
    
        


class Ip(BoxLayout):
    """GUI for working with a given IP address"""


    def __init__(self, client_socket, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = 'horizontal'  
        self.ip = None
        self.port = 5050
        self.client_socket = client_socket
        self.pos_hint={'x': 0.05, 'y': 0.85}

        self.label = Label(
            font_name="Roboto",
            font_size=15,
            text="IPv4",
            size_hint=(None, None),
            size=(25, 20),
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


    def connect_to_server(self) -> None:
        """Set connection by ip"""
        try:
            self.client_socket.connect((self.text_input.text, self.port))
            print("Successful connection")
        except Exception as e:
            print(f"Error connection: {e}\nData of ip will destroy")
            self.ip = ""
            self.text_input.text = ""


    def on_button_click(self, instance) -> None:
        """Checks the entered IP address.
           If the the entered ip adress has valid form keeped the self.ip if not display an error.
           The value can be deleted during the operetions.   
        """
        unvalide_ip = (self.text_input.text).split(".")
        if len(unvalide_ip) == 4: 
            self.connect_to_server()
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
         
        # root = BoxLayout(pos=(25, 200), orientation='vertical', spacing = 1, padding = 1) 
        root = FloatLayout()

        # add buttons top, left, right, bottom to app 

        gl = GridLayout(rows = 3, size_hint=(None, None), size=(200, 200), pos = (50, 250), spacing = 15)  
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

        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # create object of gui classes 
        self.ip = Ip(self.client_socket)
        self.bind_link = BindLink(self.client_socket)
        # Add elements to root widget  
        root.add_widget(self.ip)
        root.add_widget(gl)
        root.add_widget(self.bind_link)
        return root 
    

    


    def clickm(self, instance : None) -> None: 
        """Handles computer's click""" 
        self.ip.client_socket.send("clc".encode('utf-8')) 


    def move(self, direction: str) -> None: 
      """ 
      Handles movement based on the direction string. 
      :param direction: One of 'up', 'down', 'left', 'right' 
      """ 
      if direction == "up": 
          self.ip.client_socket.send("up".encode('utf-8'))
      elif direction == "down": 
          self.ip.client_socket.send("bottom".encode('utf-8'))
      elif direction == "left": 
          self.ip.client_socket.send("left".encode('utf-8'))
      elif direction == "right": 
          self.ip.client_socket.send("right".encode('utf-8'))
      # For special on_key_down function the condition 
      else: 
          self.clickm(None) 
     
    def on_key_down(self, instance, keyboard, keycode, text, modifiers) -> None: 
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