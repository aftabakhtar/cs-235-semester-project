"""
This python script will run the whole project and handle all the processes
"""

# imports
from python_modules import read_socket
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import websocket
import time

plt.rcParams.update({'legend.fontsize':7})
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8,4))
fig.canvas.set_window_title('Plots')

ws = websocket.WebSocket()
ws_ip = 'ws://' + "192.168.137.40"
ws.connect(ws_ip)

ani = animation.FuncAnimation(fig, read_socket.read_data2, interval=10, fargs=(ws, ax, True))
plt.show()