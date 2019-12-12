"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import websocket
import time
import json
import numpy as np

data_ = {"Ax":[], "Ay":[], "Az":[], "Gx":[], "Gy":[], "Gz":[]}
x = []

def plot_data(ax):
	"""
	data_ - as passed by read_socket()
	"""
	last = 50

	if len(data_['Ax']) > 1:
		x = [j for j in range(len(data_['Ax']))]
		ax[0][0].plot(x[-last:], data_['Ax'][-last:])
		ax[0][1].plot(x[-last:], data_['Ay'][-last:])
		ax[0][2].plot(x[-last:], data_['Az'][-last:])

		ax[1][0].plot(x[-last:], data_['Gx'][-last:])
		ax[1][1].plot(x[-last:], data_['Gy'][-last:])
		ax[1][2].plot(x[-last:], data_['Gz'][-last:])

def read_data(ws, wait=0.001):
	"""
	ip - as returned by esp8266 in serial monitor
	delay - in seconds
	"""

	# To prevent overloading esp
	time.sleep(wait)

	ws.send("Ping")

	data = ws.recv()
	# print(data)

	data = json.loads(data)
	return data

def read_data2(_, ws, ax):
	ws.send("Ping")
	data = ws.recv()
	data = json.loads(data)

	plot_data3(ax, read_data(ws))

def plot_data2(ax, data):
	"""
	data_ - as passed by read_socket()
	"""
	last = 20

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

def plot_data3(ax, data):
	"""
	data_ - as passed by read_socket()
	"""
	last = 20

	# for x in range(len(ax)):
	# 	for y in range(len(ax[0])):
	# 		ax[x][y].clear()
	for ax_ in ax:
		ax_.clear()

	for key in data:
		data_[key].append(data[key])

	if len(data_['Ax']) > 1:
		x = [j for j in range(len(data_['Ax']))]
		ax[0].plot(x[-last:], data_['Ax'][-last:])
		ax[0].plot(x[-last:], data_['Ay'][-last:])
		ax[0].plot(x[-last:], data_['Az'][-last:])

		ax[1].plot(x[-last:], data_['Gx'][-last:])
		ax[1].plot(x[-last:], data_['Gy'][-last:])
		ax[1].plot(x[-last:], data_['Gz'][-last:])


def animate(i, ws, ln):
	x.append(i)
	data = read_data(ws)
	last = 20
	print(data)
	mean = dict()
	for key in data:
		if key is not "T":
			data_[key].append(data[key])
			mean[key] = np.mean(np.array(data_['Ax'], dtype=np.float64))

	# for count, key in enumerate(data_.keys()):
	ln[0].set_data(x[-last:], data_['Ax'][-last:])
