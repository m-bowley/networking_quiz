import networkzero as nwz
from quiz_player import Player
from Questions import Question 
from time import time, sleep

players = []
MAX_PLAYERS = 4

quiz_server = nwz.advertise('Quiz')
player_ID = 0

wait_time = 0.0
while len(players) < MAX_PLAYERS:
    time_taken = time()
    message = nwz.wait_for_message_from(quiz_server, wait_for_s=0)
    if message is not None:
        address = message
        print(address)
        conn = nwz.discover(address)
        players.append(Player(player_ID, address, conn))
        player_ID += 1
        nwz.send_reply_to(quiz_server, "Player acknowledged")
        reply = nwz.send_message_to(conn, "Welcome to the quiz")
        message = None
    else:
        sleep(1)
        wait_time += 1
        print(wait_time)
        if len(players) > 0:
            reply = nwz.send_message_to(players[0].connection, "Wait time" + str(wait_time))

questions = []
with open("questions.csv", 'r') as file:
    line = file.readline()
    line = line.split(',')
    new_q = Question(line[0], line[1:4], line[5])
    questions.append(new_q)

while len(questions) > 0:
    for p in players:
        reply = nwz.send_message_to(p.connection, "Next Question")
    current_q = random.choice(questions)
    for p in players:
        reply = nwz.send_message_to(p.connection, current_q.question)
