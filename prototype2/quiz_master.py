import networkzero as nwz
from quiz_player import Player
from Questions import Question 
from time import time, sleep
import random

players = []
MAX_PLAYERS = 2

# Open the quiz server and bind it to a port - creating a socket
quiz_server = nwz.advertise('Quiz')
player_ID = 0

# Search for messages from participants until roster is full
while len(players) < MAX_PLAYERS:
    # Poll the server checking for rquests from participants
    message = nwz.wait_for_message_from(quiz_server, wait_for_s=0, autoreply=True)
    # If a message has been recieved
    if message is not None:
        # Capture the address for the connection to the quiz client
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
        if len(players) > 0:
            reply = nwz.send_message_to(players[0].connection, "Waiting for... " + str(len(players) - MAX_PLAYERS))

questions = []
with open("questions.csv", 'r') as file:
    for line in file.readlines():
        line = line.split(',')
        if len(line) > 4:
            new_q = Question(line[0], line[1:5], line[5])
            questions.append(new_q)
for p in players:
    reply = nwz.send_message_to(p.connection, "Quiz Starting")
    reply = nwz.send_message_to(p.connection, "Next Question")
while len(questions) > 0:
    current_q = random.choice(questions)
    print(current_q.correct)
    for p in players:
        reply = nwz.send_message_to(p.connection, current_q.question)
        sleep(1)
        nwz.send_reply_to(p.connection, current_q.answers)
    answered = 0
    reply = None
    while answered < len(players):
        for p in players:
            reply = nwz.wait_for_message_from(p.connection, wait_for_s=0)
            if reply is not None:
                print(reply)
                if int(reply) == int(current_q.correct):
                    p.score += 1
                    reply = nwz.send_message_to(p.connection, "Correct. Your score is: " + str(p.score))
                    answered += 1
                else:
                    reply = nwz.send_message_to(p.connection, "Incorrect. Your score is: " + str(p.score))
                    answered += 1
            else:
                sleep(0.1)
    questions.remove(current_q)
    for p in players:
        reply = nwz.send_message_to(p.connection, "Next Question")
