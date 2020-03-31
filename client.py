import socket
import select
import sys
import json
import time

CLIENT_NAME = input("Input your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 10000
client.connect((HOST, PORT))

print(f"Connected to Aplikasi Cerdas Cermat as {CLIENT_NAME}")

flag = ""
answer = {}

while True:
    data = {}

    sockets = [sys.stdin, client]

    read_sock, write_sock, error_sock = select.select(sockets, [], [])

    for sock in read_sock:
        is_timeout = False
        if sock == client:
            dump = sock.recv(2048).decode()
            data = json.loads(dump)
            # print(msg)
            flag = data['flag']
            print()
            print(data['msg'])
            if flag == 'quiz':
                print(data['answers'])
                answer['qnum']  = data['qnum']
                answer['timer'] = data['timer']
                answer['correct_ans'] = data['correct_ans']
                answer['correct_score'] = data['correct_score']
                answer['start'] = time.time()
                # while time.time()-answer['start'] <= answer['timer']:
                #     if time.time()-answer['start'] >= answer['timer']:
                #         is_timeout = True
                #         print("TIMEOUT")
                #         data = {}
                #         data['client']  = CLIENT_NAME
                #         data['flag']    = flag
                #         data['qnum']    = answer['qnum']
                #         data['answer']  = "ANSWER_TIMEOUT"
                #         data['tta']     = answer['timer']
                #         dump = json.dumps(data)
                #         client.send(dump.encode(encoding="UTF-8"))
            elif flag == 'result':
                # print(f"# Position: {data['result']['position']}")
                print(f"# Your score: {data['result']['score']}")
                lboard = json.loads(data['result']['leaderboard'])
                print("Final result: ")
                for lb in lboard:
                    print(f"# {lb} : {lboard[lb]}")
                # print(f"# Leaderboard: {data['result']['leaderboard']}")
        else:
            data['client']  = CLIENT_NAME
            data['flag']    = flag
            if flag == 'quiz':
                # count tta = time to answer
                data['correct_ans'] = answer['correct_ans']
                data['correct_score'] = answer['correct_score']
                data['qnum']    = answer['qnum']
                data['qidx']    = str(int(answer['qnum']) - 1)
                data['answer']  = input()
                answer['end']   = time.time()
                data['tta']     = answer['end']-answer['start']
            else:
                data['msg'] = input()
            dump = json.dumps(data)
            client.send(dump.encode(encoding="UTF-8"))
            # print(f"Sends {msg} to server.")
            # print(f"{CLIENT_NAME} > {msg}")

server.close()
