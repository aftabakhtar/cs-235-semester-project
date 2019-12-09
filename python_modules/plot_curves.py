"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import matplotlib.pyplot as plt
import time
import json

lst = ['{"Temperature":7, "Water":3}',
'{"Temperature":6, "Water":0}',
'{"Temperature":4, "Water":8}',
'{"Temperature":0, "Water":3}',
'{"Temperature":8, "Water":4}',
'{"Temperature":2, "Water":9}',
'{"Temperature":7, "Water":5}',
'{"Temperature":1, "Water":3}',
'{"Temperature":0, "Water":5}',
'{"Temperature":1, "Water":2}',
'{"Temperature":1, "Water":6}',
'{"Temperature":2, "Water":9}']

def plot_data(delay):
    """
    ip - as returned by esp8266 in serial monitor
    delay - in seconds
    """
    data = list()
    i = 0
    # reading data periodically
    while True:
        data.append(json.loads(lst[i])["Temperature"])
        i+=1
        print(data)
        print("o hai mark")
        # here you may add operations on data

        plt.plot([j for j in range(i)], data)
        plt.show()
        time.sleep(delay)

    # closing connection gracefully
    ws.close()

plot_data(1)