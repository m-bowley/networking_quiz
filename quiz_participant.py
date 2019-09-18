import networkzero as nwz
from time import sleep

quiz_server = nwz.discover("Quiz")
connection = nwz.advertise(nwz.address())
reply = nwz.send_message_to(quiz_server, nwz.address())
while True:
    reply = nwz.wait_for_message_from(quiz_server, wait_for_s=0)
    if reply is not None:
        print(reply)
    else:
        reply = nwz.wait_for_message_from(connection, wait_for_s=0)
        if reply is not None:
            print(reply)
        sleep(1)
