
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

from kivy.core.audio_output import SoundLoader

from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout  

  
"""  
CONSTS  
SPEED_CURSOR - speed of move the windows's, linux's cursor  
WIDTH window  
HEIGHT window  
"""  
SPEED_CURSOR = 30 

class IpNotFoundError(Popup):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        content = BoxLayout(orientation='vertical')
        close = Button (    text='OK',
                            on_press=self.dismiss, 
                            pos_hint = {"center_x": 0.5},
                            size_hint=(0.5, 0.5)
                        )
        info = Label(   text="Ip not found\nFirst of all\nenter ipv4 at the gui\nand then press OK",
                        pos_hint = {"center_x": 0.5},
                        font_size = 15, 
                    )

        content.add_widget(info)
        content.add_widget(close)
        self.content = content

        self.title = "Error"
        self.auto_dismiss = False
        self.size_hint = (0.5, 0.5)

class IncorrectFormatIp(Popup):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        content = BoxLayout(orientation='vertical')
        close = Button (    text='OK',
                            on_press=self.dismiss, 
                            pos_hint = {"center_x": 0.5},
                            size_hint=(0.5, 0.5)
                        )
        info = Label(   text="Incorrect format ip\nEnter like this\n192.168.0.102\n",
                        pos_hint = {"center_x": 0.5},
                        font_size = 15, 
                    )

        content.add_widget(info)
        content.add_widget(close)
        self.content = content

        self.title = "Error"
        self.auto_dismiss = False
        self.size_hint = (0.5, 0.5)
        

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

        # checking on connection to server
        try:
            self.client_socket.send(b'')  
        except OSError:
            SoundLoader.load('Error.mp3').play()
            return IpNotFoundError().open()

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
            SoundLoader.load('Error.mp3').play()
            return IncorrectFormatIp().open()


class ButtonsControl(GridLayout):
    """Buttons control"""
    def __init__(self, client_socket, **kwargs) -> None:
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down) 
        self.client_socket = client_socket
        self.rows = 3
        self.size_hint=(None, None)
        self.size=(200, 200)
        self.pos = (50, 250)
        self.spacing = 15
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
                  
                self.add_widget(sign_key)  
  
                accept = False   
                  
                del sign_key  
            elif i == 4: 
                self.add_widget(Button(text = "CLICK", on_press=self.clickm)) 
                accept = True 
            else:  
                self.add_widget(Widget())  
                accept = True  


    def clickm(self, instance : None) -> None: 
        """Handles computer's click""" 
        try:
            self.client_socket.send("clc".encode('utf-8')) 
        except OSError:
            SoundLoader.load('Error.mp3').play()
            return IpNotFoundError().open()


    def move(self, direction: str) -> None: 
        """ 
        Handles movement based on the direction string. 
        :param direction: One of 'up', 'down', 'left', 'right' 
        """ 
        try:
            if direction == "up": 
                self.client_socket.send("up".encode('utf-8'))
            elif direction == "down": 
                self.client_socket.send("bottom".encode('utf-8'))
            elif direction == "left": 
                self.client_socket.send("left".encode('utf-8'))
            elif direction == "right": 
                self.client_socket.send("right".encode('utf-8'))
            # For special on_key_down function the condition 
            else: 
                self.clickm(None)
        except OSError:
            SoundLoader.load('Error.mp3').play()
            return IpNotFoundError().open()



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
         
         
        root = FloatLayout()
        
        # basic socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # create object of gui classes 
        self.buttons_control = ButtonsControl(self.client_socket)
        self.ip = Ip(self.client_socket)
        self.bind_link = BindLink(self.client_socket)
        # Add elements to root widget  
        root.add_widget(self.ip)
        root.add_widget(self.buttons_control)
        root.add_widget(self.bind_link)
        return root  

if __name__ == "__main__":  
    Program().run()