import socket
import random
from time import sleep

def SetPosition(Cord, Rot):
    s = socket.socket()          
              
    # connect to the server on local computer 
    s.connect(('192.168.1.35', 1755))
    s.send((
        str(Cord[0]) + ","+ 
        str(Cord[1]) + ","+ 
        str(Cord[2]) + ","+
        str(Rot[0]) + ","+
        str(Rot[1]) + ","+
        str(Rot[2])).encode())
    print((
        str(Cord[0]) + ","+ 
        str(Cord[1]) + ","+ 
        str(Cord[2]) + ","+
        str(Rot[0]) + ","+
        str(Rot[1]) + ","+
        str(Rot[2])).encode())
    s.close()

    
if __name__ == "__main__" :
    for i in range(10):
        SetPosition((random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)), (random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)))
        sleep(1)
