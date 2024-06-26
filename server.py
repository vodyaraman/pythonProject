import socket
import threading


HOST = '127.0.0.1'
PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

# трансляция
def broadcast(message):
    for client in clients:
        client.send(message)

def user_control():
        broadcast(f"{nicknames}".encode('utf-8'))
# поддержка
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == "gui_done":
                user_control()
            else:
                print(f"{nicknames[clients.index(client)]} says {message}")
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat\n".encode('utf-8'))

            nicknames.remove(nickname)
            user_control()
            break


# приём
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected  with {str(address)}.")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is: {nickname}")
        broadcast(f"{nickname} joined the chat.\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running...")
receive()



