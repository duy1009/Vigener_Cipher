import socket
from PIL import Image
import numpy as np
import cv2
import os
from Crypto.Cipher import AES
from Crypto import Random
import time 

HOST='localhost'
PORT=8000
DATA_MAX = 2**24
WIDTH = 960
HEIGHT = 540



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


def chat(sc,key):
    print("Start chat(Enter \"quit\" to exit):")
    while True:
        msg = input('Client: ')
        ci_msg=encodeVigenere(msg,key)
        sc.sendall(bytes(ci_msg, "utf8"))
        if msg == "quit":
            break
        data = sc.recv(1024)
        str_data=data.decode("utf8")
        de_data=decodeVigenere(str_data,key)
        if de_data == "quit":
            break
        print('Server: ', de_data)
    

def Recvtext(sc, key_v):
    print("Receive file text:")
    print("Save path: ")
    path=str(input())
    with open(path,'w') as f:        #"D:/anhthe/khai.txt"
        data_enc=sc.recv(DATA_MAX)
        data_enc = data_enc.decode("utf8")
        data = decodeVigenere(data_enc, key_v)
        f.write(data)
        f.close()
    sc.sendall(bytes("ok", "utf8"))
    


def RecvImage(sc, key_AES):
    print("Receive image")
    sc.send(b"ready")
    # print("Nhap duong dan luu anh: ")
    # path=str(input())
    # D:/anhthe/Doremon.jpg
    while True:
        data_enc = sc.recv(DATA_MAX)
        if data_enc == b"Exit":
            cv2.destroyAllWindows() 
            break
        img_de = decode_AES(data_enc, key_AES)
        img_de = np.frombuffer(img_de,dtype = np.uint8)   
        img_de = img_de.reshape(HEIGHT, WIDTH, 3)
        
        cv2.imshow("Image decoded",img_de)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            sc.send(b"Exit")
            cv2.destroyAllWindows() 
            break
        sc.send(b"continue")
    


def connect(sc, key):
    print("Connecting...")
    while True:
        try:
            sc.connect(server_address)
            break
        except:
            print("Waiting server...")
    return sc
   

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    print("Nhap key: ")
    key = str(input())

    key_AES = generateAESKey(key)
    print("Your AES key:", key_AES)

    s = connect(s,key)
    sever_key = s.recv(1024).decode("utf8") #recv key
    s.send(bytes(key,"utf8")) #send key
    if sever_key!=key: #check key
        print("Wrong key!")
    else:
        while True:
            print("Chon cach truyen tin:")
            print("1: Chat (Vigenere cipher)")
            print("2: Receive file text (Vigenere cipher)")
            print("3: Receive image (AES cipher)")
            print("4: End")
            x=int(input())
            if x==1:
                chat(s, key)
            elif x==2:
                Recvtext(s, key)
            elif x==3:
                RecvImage(s, key_AES)
            else:
                print("END")
                break
        s.close()
    # time.sleep(16)