"""
This python module will read the data sent by esp8266 to the server from
a socket.
"""

import socket
import sys
import urllib.request

def read_data(ip, port):
    url = ip
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.connect((ip, port))
    n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
    n = n.decode("utf-8") # convert raw html bytes format to string
    data = n
    print(data)
