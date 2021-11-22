import socket
from sys import byteorder
from rpi_ws281x import *


LED_COUNT = 300
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

HOST = '192.168.1.9'  # own address
PORT = 65431        # Port to listen on

def func():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print('Connected by', addr)
        while True:
            sock.listen()
            data = conn.recv(1024)
            if data:
                decoded = data.decode(encoding='utf-8')
                print(decoded)
                if data == "STOP":
                    sock.close()
                    func()
                else:
                    LED(decoded)    

    
def LED(data):
    if data == "close":
        color = 0
    else:
        color = 255
    for k in range(LED_COUNT):
        strip.setPixelColor(k, Color(color, color, color))
            
    strip.show()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
func()
