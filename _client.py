import socket
import json

HOST = socket.gethostname()
# HOST = 'localhost'
PORT = 10000


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

CLIENT_NAME = input("Insert your name: ")

PROMPT = CLIENT_NAME + " > "

print("Type 'exit' to quit")

msg = input(PROMPT)

while msg != 'exit':
    passData = {
        'client': CLIENT_NAME,
        'msg'   : msg
    }
    sock.send(json.dumps(passData).encode(encoding="UTF-8"))
    data = sock.recv(2048)
    print("Received data: "+data.decode())
    msg = input(PROMPT)

sock.close()
