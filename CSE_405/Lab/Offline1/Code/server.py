import socket, os
import threading
import AES, RSA
import json
import time


class ClientThread(threading.Thread):
    def __init__(self, clientAdd, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAdd = clientAdd
        print("New connection from: ", self.clientAdd)

    def run(self):
        # print("New Connection from : ", self.clientAdd)
        while True:
            self.clientSocket.send(bytes("send_something", 'utf-8'))
            # print("before dat reception: ")
            data = self.clientSocket.recv(1024).decode()

            # print("data, ", data)
            # print("len(data): ", len(data))
            # print("before making json loads")

            received_json = {}
            if data != "" or len(data) != 0:
                # print("inside if")
                received_json = json.loads(data)

            print("client sent: ", received_json)

            encrypted_msg = received_json["encrypted_msg"]
            encrypted_key = received_json["encrypted_key"]
            public_key = received_json["public_key"]
            N = received_json["N"]

            fileDir = open("./Don’t Open this/PRK.txt", "r")
            private_key = fileDir.readline()
            print("read from prk.txt, private key: ", private_key)

            AES_key = RSA.RSA_Decryption(encrypted_key, private_key, N)

            print("This is the decrypted AES key: ", AES_key)

            AES.AES_handler(AES_key)
            decrypted_hex = AES.DecryptMessage(encrypted_msg)
            decrypted_msg = AES.print_message(decrypted_hex)

            print("decrypted msg : {} to file".format(decrypted_msg))

            fileDir = "./Don’t Open this/DPT.txt"
            os.makedirs(os.path.dirname(fileDir), exist_ok=True)
            with open(fileDir, "w") as file:
                file.write(decrypted_msg)

            print("writing to file done")

            # if received_msg == 'close':
            #     break
            # print("From Client: ", received_msg)

            # send_msg = input("Say something to client: ")
            send_msg = "check"
            self.clientSocket.send(bytes(send_msg, 'UTF-8'))

            print("sent 'check' to client")
            time.sleep(1)


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