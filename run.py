"""
This python script will run the whole project and handle all the processes
"""

# imports
from python_modules import read_socket
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import websocket
import time

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(8,4))
fig.canvas.set_window_title('Plots')

ax[0][0].legend(['Ax'])
ax[0][1].legend(['Ay'])
ax[0][2].legend(['Az'])

ax[1][0].legend(['Gx'])
ax[1][1].legend(['Gy'])
ax[1][2].legend(['Gz'])

# read_socket.read_data(ip="192.168.137.195", delay=0.01)
ws = websocket.WebSocket()
ws_ip = 'ws://' + "192.168.137.80"
ws.connect(ws_ip)

while True:
	ws.send("Send Data")

	print(ws.recv())
	time.sleep(0.001)

ws.close()


# ani = animation.FuncAnimation(fig, read_socket.read_data, interval=5, fargs=(ws, ax))
# plt.show()