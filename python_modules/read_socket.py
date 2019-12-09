"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time
import json


data_ = {"Ax":[], "Ay":[], "Az":[], "Gx":[], "Gy":[], "Gz":[]}

def plot_data(ax, data):
	"""
	data_ - as passed by read_socket()
	"""
    last = 5
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
		ax[0][0].plot(x[-last:], data_['Ax'][-last:])
		ax[0][1].plot(x[-last:], data_['Ay'][-last:])
		ax[0][2].plot(x[-last:], data_['Az'][-last:])

		ax[1][0].plot(x[-last:], data_['Gx'][-last:])
		ax[1][1].plot(x[-last:], data_['Gy'][-last:])
		ax[1][2].plot(x[-last:], data_['Gz'][-last:])

def read_data(_, ws, ax):
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
