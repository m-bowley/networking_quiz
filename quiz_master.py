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
    message = nwz.wait_for_message_from(quiz_server, wait_for_s=0)
    # If a message has been recieved
    if message is not None:
        # Capture the address for the connection to the quiz client
        address = message
        print(address)
        conn = nwz.discover(address)
        players.append(Player(player_ID, address, conn))
        nwz.send_reply_to(quiz_server, player_ID)
        nwz.send_news_to(quiz_server, "Information", "Player acknowledged: " + address)
        player_ID += 1
        message = None
    else:
        sleep(1)
        if len(players) > 0:
            reply = nwz.send_news_to(quiz_server, "Information", "Waiting for... " + str(len(players) - MAX_PLAYERS))

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
    nwz.send_news_to(quiz_server, "Question", current_q.question)
    sleep(2)
    nwz.send_news_to(quiz_server, "Answer", current_q.answers)
    answered = 0
    while answered < len(players):
        news = nwz.wait_for_news_from(quiz_server)
        if news[0] <= player_ID:
            answer = news[1]
            player = players[news[0]
            if int(answer) == int(current_q.answer):
                player.score += 1
                nwz.send_news_to(quiz_server, news[0], "Correct! Your score is: " + str(player.score]))
            else:
                nwz.send_news_to(quiz_server, news[0], "Correct! Your score is: " + str(player.score]))
    


