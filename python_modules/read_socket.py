"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time


def read_data(ip, delay):
    """
    ip - as returned by esp8266 in serial monitor
    delay - in seconds
    """
    ws = websocket.WebSocket()
    ws_ip = 'ws://' + ip
    ws.connect(ws_ip)

    # reading data periodically
    while True:
        data = ws.recv()
        print(data)
        # here you may add operations on data

        time.sleep(delay)

    # closing connection gracefully
    ws.close()
