import socket
import re
import movement


Obstacle = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.2', 31415))
s.sendall('r'.encode())

while 1:
    reply = s.recv(4096).decode()
    if not reply == '':
        if reply[0] == 'w':
            nums = re.findall('-?\d+.?\d+', reply)
            heading = nums[0]
            dist = nums[1]
            print("New waypoint: Heading of " + str(heading) + ", Distance of " + str(dist))
            movement.go(heading, dist)
            if Obstacle:
                s.sendall("o".encode())
            else:
                s.sendall("s".encode())

        elif reply[0] == 'i':
            nav.stop()

        elif reply[0] == 'h':
            s.sendall("h" + str(nav.get_heading()).encode())
