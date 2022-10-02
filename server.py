'Chat Room Connection - Client-To-Client'
import threading  # is used to run multiple threads (tasks, function calls) at the same time.
import socket  # this method is used to create a server-side socket.

# we need to set a host ip and port for the run server
host = '127.0.0.1'
port = 60650
# this is server object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# for bind the server to the host
server.bind((host, port))
# to activate the listening mode for any incoming connections to the server
server.listen()
# a lists for clients and aliases
clients = []
aliases = []

# Yrysbek added
test = {}


# this function is will iterate through the list of clients and for each client will send this message
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle clients connections
# it takes one parameter which is the client himself
def handle_client(client):
    while True:
        try:
            # the message in this case will be equal to the message received from client
            message = client.recv(1024)  # 1024 is the max number of bytes that the server can receive from client

            # Yrysbek added
            try:
                test[message.decode('utf-8')[message.decode('utf-8').find('//') + 2:]].send(
                    message.decode('utf-8')[:message.decode('utf-8').find('//')].encode('utf-8'))
            except Exception as e:
                # then we will broadcast that message
                broadcast(message)


            # if a message received successfully from the client, we will invoke the broadcast function to send this
            # message to all clients except that:
        except:
            # in case of any failures or errors in connection, we will identify client that we need to get rid of from
            # the clients list
            # We need to create an index
            index = clients.index(client)
            # index method here searches the tuple for a specified value and returns its position
            clients.remove(client)  # then we will remove the client
            client.close()  # and then will close the connection with that client
            # we will to do same thing for the aliases because we need to remove this alias of that specific client
            # from the aliases list

            alias = aliases[index]  # here we have overwritten value of the alias
            # we will invoke our broadcast function
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            # we need to remove that alias
            aliases.remove(alias)
            break


# Main function to receive the clients connection


def receive():
    while True:
        print('Server is running and listening ...')
        #  next what we want to do is we want to let the server
        #  be ready to accept any incoming connections
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        # we need to create that alias based on the information received from the client
        alias = client.recv(1024)
        # we need to append this alias to the list of aliases & we need to do the same thing with the clients
        aliases.append(alias)
        clients.append(client)


        # Yrysbek added
        test[alias.decode('utf-8')] = client



        # next we will display a message in my server
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        # we need to send a message from the server to this client telling them that you are now connected
        client.send('you are now connected!'.encode('utf-8'))
        # we need to create and start the thread in order to invoke handle client function
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


# we need to invoke that receive function here
if __name__ == "__main__":
    receive()
