import socket
s = socket.socket()
s.connect(("", 5050))
s.send("A")
print s.recv(1024)
