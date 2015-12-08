import socket
import threading
import imgproc


robots = []

#Takes a socket input
def client_handler(c, addr):
    address, port = addr
    print('Incoming Connection')
    while 1:
        reply = c.recv(4096).decode()
        if not reply == '':
            if reply[0] == 'r':
                if not address in robots:
                    robots.append(address)
                    print('Registered Robot at ' + address)
                    s.sendall()
            elif reply[0] == 'o':
                print('Robot at ' + address + ' encountered obstacle')
            elif reply[0] == 's':
                print('Robot at ' + address + 'finshed waypoint')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 31415))

s.listen(5)

while 1:
    (clientsocket, address) = s.accept()
    threading.Thread(target=client_handler(clientsocket, address)).start()