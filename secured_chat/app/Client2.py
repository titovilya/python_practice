import socket
import threading
from secured_chat.security import DH
from secured_chat.config import ServerConfig

user = DH.DH_Endpoint(197, 151, 199)
user2 = DH.DH_Endpoint(197, 151, 157)
partical_key1 = user.generate_partial_key()
partical_key2 = user2.generate_partial_key()
full_key1 = user.generate_full_key(partical_key2)
full_key2 = user2.generate_full_key(partical_key1)


def handle_messages(connection: socket.socket):
    while True:
        try:
            msg = connection.recv(ServerConfig.recv)
            if msg:
                print("Пришло:", user2.decrypt_message(msg.decode()))
            else:
                connection.close()
                break
        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break


def client() -> None:
    SERVER_ADDRESS = ServerConfig.address
    SERVER_PORT = ServerConfig.port

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        threading.Thread(target=handle_messages, args=[socket_instance]).start()
        print('Connected to chat!')

        while True:
            msg = input()
            if msg == 'quit':
                break
            socket_instance.send(user.encrypt_message(str(msg)).encode())
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
