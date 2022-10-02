# we need to import the threading and the socket
import threading
import socket

# then we need to get an alias
alias = input('Choose an alias >>> ')
# then we want to create a client object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# instead of binding a client to a host and a board we're going to connect it
client.connect(('127.0.0.1', 60650))


# we will create our client receive function
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            # the aliases message then we want to send the alias
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


# this is our sending function
def client_send():
    while True:
        #  to chat with a different person on the server:
        #  you should to type whatever message you want to send & then you will hit enter to send that message
        message = f'{alias}: {input("")}'
        # then we will send this message
        client.send(message.encode('utf-8'))


# we will create receive thread variable this again will be equal to the threading module
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# and similarly with the send thread
send_thread = threading.Thread(target=client_send)
send_thread.start()
