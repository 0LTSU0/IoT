from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
from plyer import accelerometer



class SensorApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1

        self.header = Label(text='SensorApp', font_size=64)
        self.window.add_widget(self.header)

        self.ip = TextInput(text="127.0.0.1", multiline=False)
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
            accelerometer.enable()
            
        elif self.button.text == "Stop":
            self.button.text = "Start"
            msg = bytes("STOP", encoding='utf-8')
            self.s.sendall(msg)
            self.s.close()
            accelerometer.disable()
    
    def sender(self, dt):
        if self.button.text == "Stop": #Only do this when sending is supposed to be on
            print("Do send")
            gr = str(accelerometer.acceleration())
            sensordata = bytes(gr, encoding='utf-8')
            self.s.sendall(sensordata)
            
        


if __name__ == "__main__":
    
    SensorApp().run()
