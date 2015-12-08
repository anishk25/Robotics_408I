import socket
import nav
import re


Obstacle = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 31415))
s.sendall('r'.encode())

while 1:
    reply = s.recv(4096).decode()
    if not reply == '':
        if reply[0] == 'w':
            nums = re.findall('-?\d+.?\d+', reply)
            heading = nums[0]
            dist = nums[1]
            print("New waypoint: Heading of " + str(heading) + ", Distance of " + str(dist))
            nav.rotate_to(heading)
            Obstacle = nav.finish_manuver()
            nav.drive(dist)
            Obstacle |= nav.finish_manuver()
            if Obstacle:
                s.sendall("o".encode())
            else:
                s.sendall("s".encode())

        elif reply[0] == 'i':
            nav.stop()

        elif reply[0] == 'h':
            s.sendall("h" + str(nav.get_heading()).encode())
