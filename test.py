import network
from machine import Pin, Signal
import time

import usocket as socket

led = Signal(2, Pin.OUT, invert=True)
led.on()

ap = network.WLAN(network.AP_IF)
ap.active(False)


def connect():
    ssid = "GNU"
    password = "FECAD13141"

    station = network.WLAN(network.STA_IF)

    if station.isconnected() == True:
        print("Already connected")
        return

    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    print("Connection successful")
    print(station.ifconfig())
    led.off()


def ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='Unconfigured', password='lightswitch')
    ap.active(True)
    led.on()


def web_page():
    file = open('index.html', 'r')
    s = file.read()
    file.close()
    return s


def parse_qs(self):
    form = parse_qs(self.qs)
    self.form = form


def read_form_data(request):
    size = int(request.headers[b"Content-Length"])
    data = yield from request.reader.readexactly(size)
    form = parse_qs(data.decode())
    request.form = form


def handle_http_request(request):
    response = web_page()
    return response


# App starts here
connect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:  # This is where we handle incoming requests
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = handle_http_request(request)
    conn.send(response)
    conn.close()

# Connect the device to the network


# # Start the program
