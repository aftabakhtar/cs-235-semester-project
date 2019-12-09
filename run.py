"""
This python script will run the whole project and handle all the processes
"""

# imports
from python_modules import read_socket
import matplotlib.animation as animation

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(8,4))
fig.canvas.set_window_title('Jarrar tatti')

ax[0][0].legend(['Ax'])
ax[0][1].legend(['Ay'])
ax[0][2].legend(['Az'])

ax[1][0].legend(['Gx'])
ax[1][1].legend(['Gy'])
ax[1][2].legend(['Gz'])

# read_socket.read_data(ip="192.168.137.195", delay=0.01)
ani = animation.FuncAnimation(fig, read_socket.read_data, interval=1000, fargs=("192.168.137.195", 0.01, ax))