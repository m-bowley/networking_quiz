import networkzero as nwz

question = "What colour is the sky?|Red|Purple|Blue|Yellow"
answer = "Blue"
quiz_server = nwz.advertise('Quiz')
while True:
    nwz.wait_for_message_from(quiz_server)
    reply = nwz.send_message_to(quiz_server, question)
    print("Answer was... " + reply)
    if answer == reply:
        correct = "Correct"
    else:
        correct = "Wrong Answer"
    nwz.send_message_to(quiz_server, correct)
