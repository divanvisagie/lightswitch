import network
from machine import Pin, Signal
import time

import usocket as socket

led = Signal(2, Pin.OUT, invert=True)
led.off()
ap = network.WLAN(network.AP_IF)


def ap_mode():
    ap.config(essid='Unconfigured', password='lightswitch')
    ap.active(True)
    led.on()


def web_page():
    file = open('index.html', 'r')
    s = file.read()
    file.close()
    return s


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()

# Connect the device to the network
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)

# sta_if.connect('ssid', 'key')

# # Start the program
# if (sta_if.isconnected()):
#     led.off()  # off is on
#     print('Connected')
# else:
#     print('Not Connected')
