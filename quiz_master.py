import networkzero as nwz
from quiz_player import Player
from Questions import Question 
from time import time, sleep
import random

players = []
player_addresses = []
MAX_PLAYERS = 2

# Open the quiz server and bind it to a port - creating a socket
quiz_server = nwz.advertise('Quiz')
player_ID = 0

# Search for messages from participants until roster is full
while len(players) < MAX_PLAYERS:
    # Poll the server checking for requests from participants
    connections = nwz.discover_all()
    #print(connections)
    # If a message has been recieved
    if len(connections) > 0:
        for c in connections:
            # Capture the address for the connection to the quiz client
            if "Quiz Participant" in c[0] and c[1] not in player_addresses:
                print(connections)
                nwz.send_news_to(quiz_server, "Information", "Player acknowledged" + c[1])
                #print(address)
                conn = nwz.discover(c[0])
                response = nwz.send_message_to(conn, player_ID)
                print(response)
                nwz.send_reply_to(conn)
                players.append(Player(player_ID, c[1], conn))
                player_addresses.append(c[1])
                player_ID += 1
    else:
        sleep(1)
        if len(players) > 0:
            print("sending news")
            nwz.send_news_to(quiz_server, "Information", "Waiting for... " + str(MAX_PLAYERS -len(players)) + " players")
sleep (5)
questions = []

with open("questions.csv", 'r') as file:
    for line in file.readlines():
        line = line.split(',')
        if len(line) > 4:
            new_q = Question(line[0], line[1:5], line[5])
            questions.append(new_q)

nwz.send_news_to(quiz_server, "Information", "Quiz Starting")

while len(questions) > 0:
    current_q = random.choice(questions)
    sleep(1)
    nwz.send_news_to(quiz_server, "Question", current_q.question)
    sleep(2)
    nwz.send_news_to(quiz_server, "Answers", current_q.answers)
    answered = 0
    while answered < len(players):
        for p in players:
            message = nwz.wait_for_message_from(p.connection, wait_for_s=0)
            if message is not None:
                print(message)
                answer = message[1]
                player = players[message[0]]
                if int(answer) == int(current_q.correct):
                    player.score += 1
                    nwz.send_reply_to(player.connection, "Correct! Your score is: " + str(player.score))
                else:
                    nwz.send_reply_to(player.connection, "Incorrect! Your score is: " + str(player.score))
                answered += 1
                message = None
        else:
            sleep(1)
    questions.remove(current_q)