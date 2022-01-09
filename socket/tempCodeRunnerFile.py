import socket
import threading
import numpy as np
import cv2
import os 

host_name=socket.gethostname()
HOST=socket.gethostbyname(host_name)
PORT=8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)