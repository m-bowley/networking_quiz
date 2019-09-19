import networkzero as nwz
from time import sleep

quiz_server = nwz.discover("Quiz")
address = nwz.address()
connection = nwz.advertise(address)
reply = nwz.send_message_to(quiz_server, address)
print(reply)
quiz_starting = False
while not quiz_starting:
    reply = nwz.wait_for_message_from(quiz_server, wait_for_s=0, autoreply=True)
    if reply is not None:
        print(reply)
    else:
        reply = nwz.wait_for_message_from(connection, wait_for_s=0, autoreply=True)
        if reply is not None:
            print(reply)
            if reply == "Quiz Starting":
                quiz_starting = True
        sleep(1)

quiz_over = False
while not quiz_over:
    reply = nwz.wait_for_message_from(connection, wait_for_s=0, autoreply=True)
    if reply is not None:
        print(reply)
        if reply == "Next Question":
            question = nwz.wait_for_message_from(connection)
            print(question)
            reply = None
