"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time
from plot_curves import plot_data

ws = websocket.WebSocket()
ws_ip = 'ws://' + ip
ws.connect(ws_ip)

def read_data(ip, delay, ax):
    """
    ip - as returned by esp8266 in serial monitor
    delay - in seconds
    """


    # reading data periodically
    # while True:
    data = ws.recv()
    # print(data)
    # here you may add operations on data
    plot_data(ax, data)
    # time.sleep(delay)

    # closing connection gracefully
    # ws.close()
