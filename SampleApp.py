import socket
import random
from time import sleep

def SetPosition():
    s = socket.socket()          
              
    # connect to the server on local computer 
    s.connect(('192.168.1.35', 1755))
    s.send((
        str(random.randint(-10,10)) + ","+ 
        str(random.randint(-10,10)) + ","+ 
        str(random.randint(-10,10))).encode())
    s.close()

    
if __name__ == "__main__" :
    for i in range(100):
        SetPosition()
        sleep(1)
