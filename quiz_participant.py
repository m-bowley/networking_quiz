import networkzero as nwz
from time import sleep

quiz_server = nwz.discover("Quiz")
connection = nwz.advertise(nwz.address())
reply = nwz.send_message_to(quiz_server, nwz.address())
print(reply)
