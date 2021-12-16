from m5stack import *
from m5ui import *
from uiflow import *
import socket

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

label0 = M5Label('Running', x=69, y=99, color=0x000, font=FONT_MONT_14, parent=None)

IP = '127.0.0.1'  
DATA = b"Hello, World!"

udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udpsocket.connect((IP, 5005))

k = 0
while k <10:
  #Receive 1024 bytes data
  udpsocket.sendto(DATA, (IP, 5005))
  label0 = M5Label('Running' + str(k), x=69, y=120, color=0x000, font=FONT_MONT_14, parent=None)
  k+=1
    


