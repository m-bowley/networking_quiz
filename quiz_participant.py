import networkzero as nwz
from time import sleep

quiz_server = nwz.discover("Quiz")
address = nwz.address()
connection = nwz.advertise("Quiz Participant :s"+address)
response = nwz.wait_for_message_from(connection, autoreply=True)
playerID = response
response = nwz.wait_for_message_from(connection)

response = ""
while response != "Done":
    news = nwz.wait_for_news_from(quiz_server)
    if news[0] == "Information":
        print("Quiz server says: " + news[1])
    elif news[0] == "Question":
        print("Incoming Question")
        print(news[1])
    elif news[0] == "Answers":
        answers = news[1]
        for i in range(len(answers)):
            print(str(i) + ". " + answers[i])
        print('Enter the number of your answer')
        my_answer = int(input(">"))
        reply = nwz.send_message_to(connection, [playerID, my_answer])
        print(reply)
    elif news[0] == playerID:
        print(news[1])
    
        
