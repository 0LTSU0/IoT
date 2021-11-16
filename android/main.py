import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
from plyer import accelerometer
from plyer import gyroscope

kivy.require('1.9.0')

class SensorApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.header = Label(text='SensorApp', font_size=64)
        self.window.add_widget(self.header)

        self.ip = TextInput(text="192.168.1.6", multiline=False)
        self.window.add_widget(self.ip)

        self.button = Button(text="Start", font_size=32)
        self.button.bind(on_press=self.buttfunc)
        self.window.add_widget(self.button)

        Clock.schedule_interval(self.sender, 0.15)

        return self.window

    def buttfunc(self, event):
        if self.button.text == "Start":
            self.button.text = "Stop"
            HOST = self.ip.text
            PORT = 65432
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((HOST, PORT))
            #accelerometer.enable()
            gyroscope.enable()
            
        elif self.button.text == "Stop":
            self.button.text = "Start"
            msg = bytes("STOP", encoding='utf-8')
            self.s.sendall(msg)
            self.s.close()
            #accelerometer.disable()
            gyroscope.disable()
    
    def sender(self, dt):
        if self.button.text == "Stop": #Only do this when sending is supposed to be on
            print("Do send")
            #g = accelerometer.acceleration
            g = gyroscope.rotation
            gr = str(g)
            #gr = "test"
            sensordata = bytes(gr, encoding='utf-8')
            self.s.sendall(sensordata)
            
        


if __name__ == "__main__":
    
    SensorApp().run()
