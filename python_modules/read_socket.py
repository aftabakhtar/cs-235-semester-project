"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time
import json

ws = websocket.WebSocket()
ws_ip = 'ws://' + "192.168.137.225"
ws.connect(ws_ip)

data_ = {"Ax":[], "Ay":[], "Az":[], "Gx":[], "Gy":[], "Gz":[]}

def plot_data(ax, data):
	"""
	data_ - as passed by read_socket()
	"""
	if data is dict():
		return
	for x in range(len(ax)):
		for y in range(len(ax[0])):
			ax[x][y].clear()

	for key in data:
			if key is not "T":
				data_[key].append(data[key])

	if len(data_['Ax']) > 1:
		x = [j for j in range(len(data_['Ax']))]
		ax[0][0].plot(x, data_['Ax'])
		ax[0][1].plot(x, data_['Ay'])
		ax[0][2].plot(x, data_['Az'])

		ax[1][0].plot(x, data_['Gx'])
		ax[1][1].plot(x, data_['Gy'])
		ax[1][2].plot(x, data_['Gz'])

def read_data(_, ip, delay, ax):
    """
    ip - as returned by esp8266 in serial monitor
    delay - in seconds
    """


    # reading data periodically
    # while True:
    data = ws.recv()
    data = json.loads(data)
    # print(data)
    # here you may add operations on data
    plot_data(ax, data)
    # time.sleep(delay)

    # closing connection gracefully
    # ws.close()
