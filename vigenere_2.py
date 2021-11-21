import cv2
import numpy as np

def generateKey(len_str, key): # len_str = Độ dài key cần tạo(int), key(string) => return key được lặp lại (string)
    key = list(key)
    if len_str == len(key):
        return(key)
    else:
        for i in range(len_str - len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
     
# TEXT
def cipherText(string, key): # Mã hóa text
    cipher_text = []
    key = generateKey(len(string), key)
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 256
        # x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))

def decryptedText(cipher_text, key): # Giải mã text
    decry_text = []
    key = generateKey(len(cipher_text), key)
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 256) % 256
        # x += ord('A')
        decry_text.append(chr(x))
    return("" . join(decry_text))


# IMAGE
def encodeImg(img, key):    # img = Array của numpy , key(string) bất kì
    print("Proceed to encode the image...")
    # Tạo key (mảng 3 chiều (int))
    key_num = []
    (h,w,d) = img.shape
    key = generateKey(h*w*d,key)
    for i in range(h*w*d):
        key_num.append(ord(key[i]))
    key_num = np.array(key_num)
    key_num = np.reshape(key_num,(-1,w,d))
    # Mã hóa
    img = (img + key_num) %256
    print("Done")
    return img.astype(np.uint8)
                
def decodeImg(img, key): # img = string, key của encodeImg
    print("Proceed to decode the image...")
    # Tạo key (mảng 3 chiều (int))
    (h,w,d) = img.shape
    key = generateKey(h*w*d,key)
    key_num = []
    for i in range(h*w*d):
        key_num.append(ord(key[i]))
    key_num = np.array(key_num)
    key_num = np.reshape(key_num,(-1,w,d))
    # Giải mã
    img = (img - key_num + 256) %256
    print("Done")
    return img.astype(np.uint8)

while 1:
    print("---------------------------------------"+
            "\n1. Text\n2. Image\n3. Exit\n>>",end ="")
    evt = int(input())
    
    if evt == 1:

        print("Input text: ",end="")
        text = input()

        print("Key: ",end="")
        key = input()

        cip = cipherText(text,key)

        print("Encode: ",cip)
        print("Decode: ",decryptedText(cip,key))
    elif evt == 2:

        print("Path: ",end="")
        path = input()
        tail = "." + path.split(".")[-1]
        file_img = cv2.imread(path)
        img = np.array(file_img)

        print("Key: ",end="")
        key = input()

        cip = encodeImg(img,key)
        cv2.imshow("Image after encoding", cip)
        cv2.imwrite("Img_encode"+tail, cip)
        print("Img_encode"+tail)
        de = decodeImg(cip,key)
        cv2.imshow("Image after decoding", de)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif evt == 3:
        break
    else:
        continue




# C:\\Users\\admin\\Desktop\\Temp\\Car-data\\Data\\anh1.jpg