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

ax[0][0].set_ylim(-1.5, 1.5)
ax[0][1].set_ylim(-1.5, 1.5)
ax[0][2].set_ylim(-1.5, 1.5)

ln = ax[0][0].plot([],[])
# 	ax[0][1].plot([],[]),
# 	ax[0][2].plot([],[]),
# 	ax[1][0].plot([],[]),
# 	ax[1][1].plot([],[]),
# 	ax[1][2].plot([],[])
# ]

ws = websocket.WebSocket()
ws_ip = 'ws://' + "192.168.137.112"
ws.connect(ws_ip)

# while True:

# 	dictionary = read_socket.read_data(ws, 1)
# 	print(dictionary)


# ani = animation.FuncAnimation(fig, read_socket.animate, interval=5, fargs=(ws, ln))

ani = animation.FuncAnimation(fig, read_socket.read_data2, interval=10, fargs=(ws, ax))

plt.show()

# ws.close()
