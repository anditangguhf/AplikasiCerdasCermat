import socket
import select
import sys
import json
import time
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.setblocking(0)

HOST = socket.gethostname()
PORT = 10000
MIN_CLIENTS = 2

# timer in seconds
QUESTION_TIMER = 15

server.bind((HOST,PORT))
server.listen(100)

clients = []
players = []
players_data = {}

print(f"Starting quiz server on {HOST}:{PORT}")
min = input("Set minimum clients to start the quiz: ")
MIN_CLIENTS = int(min)
print("Waiting for clients to connect...")

def clientthread(conn, addr):
    while True:
        try:
            dump = conn.recv(2048).decode()
            data = json.loads(dump)
            # print(dump)

            delta_raw = QUESTION_TIMER - float(data['tta'])
            delta = float("{:.3}".format(delta_raw)) * 100

            print(f"Question #{data['qnum']} - {data['client']} submits answer {data['answer']} with time delta of {delta_raw}")

            # scoring logic below
            # {"client": "ca", "flag": "quiz", "correct_ans": "A", "correct_score": "10", "qnum": "1", "qidx": "0", "answer": "a", "tta": 4.188803195953369}
            # {"client": "cb", "flag": "quiz", "correct_ans": "A", "correct_score": "10", "qnum": "1", "qidx": "0", "answer": "b", "tta": 7.101882219314575}
            score = 0
            if data['answer'].lower() == data['correct_ans'].lower():
                correct_score = float(data['correct_score'])
                # tta = float("{:.3}".format(data['tta']))

                score = correct_score * delta
                # print(score)

                players_data[data['client']] = players_data[data['client']] + int(score)

        except:
            continue

def broadcast(msg, conn):
    for c in clients:
        if c != conn:
            try:
                c.send(msg)
            except:
                c.close()

def broadcast_to_all(dump, clients):
    for conn in clients:
        broadcast(dump.encode(encoding="UTF-8"), conn)

def listen_answer(clients, timeout):
    return ""

def timer(timeout):
    t = timeout
    while t >= 0:
        t = t - 1
        time.sleep(1)

def quiz(clients, players):
    # prompt admin to start the quiz
    data = {}
    time.sleep(1)
    prompt = input(f"{len(clients)} clients has joined the quiz. Would you like to start the quiz? (y/n) ")

    if prompt != "y":
        quiz(clients)
    else:
        # prompt all clients that quiz is starting
        print("Quiz started!")
        data['flag'] = 'notification'
        data['msg']  = 'Quiz started!'
        dump = json.dumps(data)
        broadcast_to_all(dump, clients)

        # read questions
        file_soal = open('soal.txt', 'r').read().splitlines()
        # print(file_soal)

        total_soal = len(file_soal)
        counter = 0

        # loop every questions
        while counter < total_soal:
            # prompt current score
            ctr = 0
            while ctr < len(clients):
                data['flag']    = 'notification'
                data['msg']     = "Current score: " + str(players_data[players[ctr]])
                dump = json.dumps(data)
                clients[ctr].send(dump.encode(encoding="UTF-8"))
                ctr = ctr + 1

            curr = file_soal[counter].split("#")

            # Format array soal:
            # 0: Nomor soal
            # 1: Pertanyaan
            # 2: Nilai
            # 3: Jwb A
            # 4: Jwb B
            # 5: Jwb C
            # 6: Jwb D
            # 7: Jwb benar

            data['flag']    = 'quiz'
            data['timer']   = QUESTION_TIMER
            data['correct_score'] = curr[2]
            data['correct_ans'] = curr[7]
            data['qnum']    = curr[0]
            data['msg']     = curr[0] + ". " + curr[1]
            data['answers'] = "A. "+ curr[3] + "; B. "+ curr[4] + "; C. " + curr[5] + "; D. " + curr[6]
            dump = json.dumps(data)
            broadcast_to_all(dump, clients)

            counter = counter + 1

            ready = select.select([server], [], [], QUESTION_TIMER)
            # if ready[0]:
            #     print(conn.recv(2048).decode())
            #     ansdump = conn.recv(2048).decode()
            #     ansdata = json.loads(ansdump)
            #     # scoring logic here
            #     # {"client": "ca", "flag": "quiz", "qnum": "1", "answer": "a", "tta": 5.000228643417358}
            #     # {"client": "ca", "flag": "quiz", "qnum": "1", "answer": "ANSWER_TIMEOUT", "tta": 10}
            #     score = 100
            #     players_data[ansdata['client']] = score
            #     print(score)
            #     print(players_data)

            # if counter == total_soal:
            #     # print(players_data)
            #     data['flag']        = 'result'
            #     data['msg']         = "Quiz finished! Here is the result: "
            #     data['result']      = {
            #         'position'   : '0',
            #         'score'      : '0',
            #         'leaderboard': '0'
            #     }
            #     dump = json.dumps(data)
            #     broadcast_to_all(dump, clients)
            #
            #     break;

finalres = {}
while True:
    conn, addr = server.accept()

    conn_msg = {
        'flag'  : "init",
        'msg'   : "You are connected! Press <enter> if you are ready to join."
    }
    dump = json.dumps(conn_msg)
    conn.send(dump.encode(encoding="UTF-8"))

    initClient = conn.recv(2048).decode()
    if initClient:
        clientData = json.loads(initClient)

        start_new_thread(clientthread, (conn, addr))

        print(f"{addr[0]}:{addr[1]} connected as {clientData['client']}.")

        conn_msg = {
            'flag'  : "notification",
            'msg'   : "You have joined the quiz! Please wait for admin to start."
        }
        dump = json.dumps(conn_msg)
        conn.send(dump.encode(encoding="UTF-8"))

        clients.append(conn)
        players.append(clientData['client'])
        players_data[clientData['client']] = 0

    if len(clients) >= MIN_CLIENTS:
        # print(clients)
        quiz(clients, players)

        ctr = 0
        while ctr < len(clients):
            # print(clients[ctr])
            # print(players[ctr])

            finalres['flag']        = 'result'
            finalres['msg']         = "Quiz finished! Here is the result: "
            finalres['result']      = {
                # 'position'   : '0',
                'score'      : players_data[players[ctr]],
                'leaderboard': json.dumps(players_data)
            }
            frs = json.dumps(finalres)
            clients[ctr].send(frs.encode(encoding="UTF-8"))

            ctr = ctr + 1

        # print(f"Leaderboard: {players_data}")
        print("Final result: ")
        for pd in players_data:
            print(f"# {pd} : {players_data[pd]}")


conn.close()
server.close()
