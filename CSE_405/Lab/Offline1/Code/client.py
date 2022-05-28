import socket
import os
import AES, RSA
import time
import json


def convertToJson(enc_msg, enc_key, public_key, N):


  json_text = {
    "encrypted_msg": enc_msg,
    "encrypted_key": enc_key,
    "public_key": public_key,
    "N": N
  }

  print("json to send: ", json_text)
  return json.dumps(json_text)



PORT = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("127.0.0.1", PORT))

# clientSocket.sendall(bytes("This is from Client",'UTF-8'))
while True:
  fromServer = clientSocket.recv(2048).decode()
  print("From Server :", fromServer.strip())

  if fromServer.strip() == "send_something":
    print("inside if")
    toServer = input("Say something to Server: ")
    key_len = input("Enter RSA key length: ")
    AES_key = input("Enter AES key: ")

    encrypted_key, public_key, private_key, N = RSA.RSA_Encryption(AES_key, key_len)

    fileDir = "./Don’t Open this/PRK.txt"
    os.makedirs(os.path.dirname(fileDir), exist_ok=True)
    with open(fileDir, "w") as file:
      file.write(str(private_key))

    AES.AES_handler(AES_key)

    encrypted_msg = AES.EncryptMessage(toServer)
    print("Encrypted Msg: ", encrypted_msg)

    # sock.sendall(bytes(data,encoding="utf-8"))

    # clientSocket.sendall(bytes(convertToJson(encrypted_msg, encrypted_key, public_key, N), encoding="utf-8"))
    clientSocket.send(convertToJson(encrypted_msg, encrypted_key, public_key, N).encode())


    print("json sent to server")
    # sendToServer = encrypted_msg + "####" + encrypted_key + "####" + public_key + "####" + str(N) + "####" + key_len
    # clientSocket.sendall(bytes(sendToServer, 'UTF-8'))

  elif fromServer == "check":
    # decrypted_msg = AES.DecryptMessage(encrypted_msg)
    # print("Decrypted Msg: ", decrypted_msg)

    print("sent message: ", toServer)
    # printed_msg = AES.print_message(decrypted_msg)

    fileDir = open("./Don’t Open this/DPT.txt", "r")
    server_dpt = fileDir.readline()
    print("message received by server: ", server_dpt)

    if server_dpt == toServer:
      print("Match")
    else:
      print("Did not Match")

  else:
    print("no idea what happened?")



  if fromServer=='close':
    break

toServer.close()






























# import socket
#
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # default port for socket
# port = 12345
#
# try:
#     host_ip = socket.gethostbyname('www.google.com')
# except socket.gaierror:
#     print("there was an error resolving the host")
#     # sys.exit()
#
# # connecting to the server
# client_socket.connect(("localhost", port))
#
# print("the socket has successfully connected to serder")
#
# while True:
#     # print("Got connection from", con_addr)
#
#     data = client_socket.recv(1024)
#     if not data:
#         break
#     print("Server sent: ", data)
#     # con_socket.sendall(data)
#
#     # messageFromServer = client_socket.recv(1024)
#     # print (messageFromServer.decode())
#     # print("Message from Server: ", messageFromServer)
#     # messagefromserver = raw_input("Enter reply message for client: ")
#     messageToServer = "How you doin Server? ".encode()
#
#     client_socket.send(messageToServer)
#
#     # c.send('Thank you for connecting'.encode())
#
# client_socket.close()
#
# # receive data from the server and decoding to get the string.
# # print (s.recv(1024).decode())
# # close the connection
# # s.close()
