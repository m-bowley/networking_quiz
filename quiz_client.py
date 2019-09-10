import networkzero as nwz

quiz_server = nwz.discover("Quiz")
reply = nwz.send_message_to(quiz_server, "World")
question = reply.split('|')
print(question[0])
for i in range(1, len(question)):
    letter = chr(64 + i)
    print(letter + ") " + question[i])
print("Enter the letter of your answer")
answer = input(">")
response = ord(answer) - 64
message = nwz.send_message_to(quiz_server, question[response])
print(message)
