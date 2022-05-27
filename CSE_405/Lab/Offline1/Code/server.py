import socket, os
import threading
import AES, RSA

class ClientThread(threading.Thread):
    def __init__(self, clientAdd, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAdd = clientAdd
        print("New connection from: ", self.clientAdd)

    def run(self):
        print("Connection from : ", self.clientAdd)
        self.clientSocket.send(bytes("send_something",'utf-8'))
        received_msg = ''
        while True:
            data = self.clientSocket.recv(2048)
            received_msg = data.decode()
            received_msg = received_msg.split("####")

            encrypted_msg = received_msg[0]
            encrypted_key = received_msg[1]
            public_key = received_msg[2]
            N = received_msg[3]
            key_len = received_msg[4]

            fileDir = open("/Don’t Open this/PRK.txt", "r")
            private_key = fileDir.readline()

            AES_key = RSA.RSA_Decryption(encrypted_key, private_key, N, key_len)
            # Insert here the AES key to the AES_handler
            decrypted_hex = AES.DecryptMessage()
            decrypted_msg = AES.print_message(decrypted_hex)

            fileDir = "/Don’t Open this/DPT.txt"
            os.makedirs(os.path.dirname(fileDir), exist_ok=True)
            with open(fileDir, "w") as file:
                file.write(decrypted_msg)

            # if received_msg == 'close':
            #     break
            # print("From Client: ", received_msg)

            # send_msg = input("Say something to client: ")
            send_msg = "check"
            self.clientSocket.send(bytes(send_msg, 'UTF-8'))


        print("Client at ", self.clientAdd, " disconnected...")


PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(5)
    clientSocket, clientAdd = server.accept()
    newClientThread = ClientThread(clientAdd, clientSocket)
    newClientThread.start()

# import socket
#
# s = socket.socket();
# print("Socket successfully created")
# port = 12345
#
# s.bind(('localhost', port))
# print("Socket binded to %s " % (port))
# s.listen(5)
# print("Socket is listening")
#
# while True:
#     con_socket, con_addr = s.accept()
#     print("Got connection from", con_addr)
#
#     while True:
#         messageToClient = "How you doin Client? ".encode()
#         con_socket.send(messageToClient)
#
#         # data = con_socket.recv(1024)
#         # if not data:
#         #     break
#         # print("client sent: ", data)
#         # con_socket.sendall(data)
#
#         messageFromClient = con_socket.recv(1024)
#         print("Message from Client: ", messageFromClient)
#     # messagefromserver = raw_input("Enter reply message for client: ")
#
#
#     # c.send('Thank you for connecting'.encode())
#
#     con_socket.close()
#
#     break
#
# s.close()