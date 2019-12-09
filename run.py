"""
This python script will run the whole project and handle all the processes
"""

# imports
from python_modules import read_socket, plot_curves
import matplotlib.animation as animation
import matplotlib.pyplot as plt

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
ws_ip = 'ws://' + "192.168.137.225"
ws.connect(ws_ip)

ani = animation.FuncAnimation(fig, read_socket.read_data, interval=100, fargs=(ws, ax))
plt.show()