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
ws_ip = 'ws://' + "192.168.137.81"
ws.connect(ws_ip)

ani = FuncAnimation(fig, read_data2, interval=10, fargs=(1, ax, True))
plt.show()