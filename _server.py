import socket
import json
from threading import Thread

class ServThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip     = ip
        self.port   = port

    def run(self):
        # print("Connected clients: ")
        # print(conns)
        while True:
            data = json.loads(conn.recv(2048).decode())
            # print(data)
            print("Message from client " + data['client'] + ": " + data['msg'])
            # for c in conns:
                # print(c)
            conn.sendall(data['msg'].encode(encoding="UTF-8"))  # echo


HOST = '0.0.0.0'
PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
threads = []
conns = []

while True:
    server.listen(5)
    (conn, (host, port)) = server.accept()
    conns.append(conn)
    nthread = ServThread(host, port)
    nthread.start()
    threads.append(nthread)
    # print(threads)

for i in threads:
    i.join()
