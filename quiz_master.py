import networkzero as nwz
from quiz_player import Player
from time import time, sleep

players = []
MAX_PLAYERS = 4

quiz_server = nwz.advertise('Quiz')
player_ID = 0

wait_time = 0.0
while True:
    time_taken = time()
    message = nwz.wait_for_message_from(quiz_server, wait_for_s=0)
    if message is not None:
        address = message
        print(address)
        players.append(Player(player_ID, address))
        player_ID += 1
        reply = nwz.send_reply_to(quiz_server, "Welcome to the quiz")
        if len(players) == 4:
            break
        time_taken -= time()
        wait_time += time_taken
    else:
        if len(players) > 0:
            sleep(1)
            time_taken += 1
            nwz.send_reply_to(quiz_server, "Quiz starts in " + str(int(30 - wait_time)))
            if wait_time >= 30:
                nwz.send_reply_to(quiz_server, "Quiz starting...")

