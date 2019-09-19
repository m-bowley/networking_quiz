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

