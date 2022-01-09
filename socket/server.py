import socket
import threading
import numpy as np
import cv2
import os 
from Crypto.Cipher import AES
from Crypto import Random

HOST='localhost'
PORT=8000
DATA_MAX = 2**24
WIDTH = 960
HEIGHT = 540

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def generateVigenereKey(len_str, key): # len_str = Độ dài key cần tạo(int), key(string) => return key được lặp lại (string)
    key = list(key)
    if len_str == len(key):
        return(key)
    else:
        for i in range(len_str - len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
     
# TEXT
def encodeVigenere(string, key): # Mã hóa text
    cipher_text = []
    key = generateVigenereKey(len(string), key)
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 256
        # x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))

def decodeVigenere(cipher_text, key): # Giải mã text
    decry_text = []
    key = generateVigenereKey(len(cipher_text), key)
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 256) % 256
        # x += ord('A')
        decry_text.append(chr(x))
    return("" . join(decry_text))
# ****** AES **********
def generateAESKey(key_string):
    key = bytes(key_string,"utf8")
    while len(key)<16:
        key = key + key
    if len(key)>16:
        key = key[0:15]
    return key

def encode_AES(data, key):
    # Tạo IV ngẫu nhiên
    IV = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_EAX,IV)
    # Mã hóa 
    ciphertext =   IV + cipher.encrypt(data)
    return ciphertext

def decode_AES(data_enc, key): # decode AES
    IV_rec = data_enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_EAX, IV_rec)
    plaintext = cipher.decrypt(data_enc[AES.block_size:])
    return plaintext

# connect to client
def connect(s):
    print("Connecting...")
    while True:
        try: 
            client, addr = s.accept()
            print('Connected by', addr)
            break
        except:
            print("Run Client.py, Please")
    return client, addr
    

def chat(client,addr,key):
    print("Start chat(Enter \"quit\" to exit):")
    print("Waiting client...")
    
    while True:
        data = client.recv(1024)
        strdata = data.decode("utf8")
        str_data=decodeVigenere(strdata,key)
        if str_data == "quit":
            break
        print("Client: " + str_data)

        msg = str(input("Server: "))
        ci_msg=encodeVigenere(msg,key)
        client.send(bytes(ci_msg,"utf8"))
        if msg == "quit":
            break
    

def sendtext(client,addr,key_v):
    print("Send file text:")
    
    print('Connected by', addr)
    print("Path text file: ") #"D:/vscode/code Python/truyen_nhan_tin/VDK.txt"
    path=str(input())
    with open(path,'r') as f:
        enc_text = encodeVigenere(f.read(),key_v)
        client.send(bytes(enc_text,"utf8"))
        f.close()
    
    data = client.recv(1024)
    str_data = data.decode("utf8")
    if str_data == "ok":
        print("Done!")
    else:
        print("Error!")
           

def sendImage(client,addr,key_AES):
    print("Send image, waiting for response... ")
    
    resp1 = client.recv(10)
    if resp1 !=b"ready":
        print("Error.")
        return
    
    vid = cv2.VideoCapture(0)
    while True:
        rate,frame = vid.read()
        frame = cv2.resize(frame,(WIDTH,HEIGHT))
        
        im_byte = np.array(frame).tobytes()
        data_enc = encode_AES(im_byte, key_AES)
        client.send(data_enc) 
        resp2 = client.recv(100) 

        if resp2 == b"Exit":
            cv2.destroyAllWindows() 
            break
        data_enc = np.frombuffer(data_enc[AES.block_size:], dtype = np.uint8)   
        data_enc = data_enc.reshape(HEIGHT, WIDTH, 3)
        cv2.imshow("Image encoded",data_enc)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            client.send(b"Exit")
            cv2.destroyAllWindows() 
            break   

if __name__ == "__main__":

    print("Nhap key: ")
    key=str(input())

    key_AES = generateAESKey(key)
    print("Your AES key:", key_AES)

    client, addr = connect(s)
    client.send(bytes(key,"utf8")) # send key
    client_key = client.recv(1024).decode("utf8") #recv key
    
    if client_key!=key: #check key
        print("Wrong key!")
        client.close()
    else:
        while True:
            print("Chon cach truyen tin:")
            print("1: Chat (Vigenere cipher)")
            print("2: Send file text (Vigenere cipher)")
            print("3: Send image (AES cipher)")
            print("4: End")
            x=int(input())
            if x==1:
                chat(client,addr,key)
            elif x==2:
                sendtext(client,addr,key)
            elif x==3:
                sendImage(client,addr, key_AES)
            else:
                print("END")
                break
        client.close()
 
#key:VuxDDinhkhaideptraisieucapvippro%%%%%%%%%%%%$$$$$$$$$###########
# git remote add origin https://github.com/VuDinhKhai/socket_server_client.git
# git branch -M main
# git push -u origin main
# https://github.com/VuDinhKhai/socket_server_client.git