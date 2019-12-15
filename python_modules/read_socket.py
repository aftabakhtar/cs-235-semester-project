"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time
import json
import numpy as np
import helpers

data_ = {"Ax":[], "Ay":[], "Az":[], "Gx":[], "Gy":[], "Gz":[]}
gradient_ = {"Ax":[], "Ay":[], "Az":[], "Gx":[], "Gy":[], "Gz":[]}
x = []


def read_data(ws):
	"""
	ws - websocket to read data from
	"""
	ws.send("Ping")
	data = ws.recv()
	data = json.loads(data)
	return data

def read_data2(i, ws, ax):
	x.append(i)
	for ax_ in ax:
		for a in ax_:
			a.clear()
	data = read_data(ws)

	for key in data:
		data_[key].append(data[key])
		if i > 0:
			gradient_[key].append(data_[key][i]-data_[key][i-1])
		else:
			gradient_[key].append(0)

	helpers.plot_data(ax, x, data_, gradient_)