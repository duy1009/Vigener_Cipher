# from typing import Text
import cv2
import numpy as np

MAX_LEN_IMG = 10

def generateKey(len_str, key):
    key = list(key)
    if len_str == len(key):
        return(key)
    else:
        for i in range(len_str - len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
     
def cipherText(string, key):
    cipher_text = []
    key = generateKey(len(string), key)
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 256
        # x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))

def decryptedText(cipher_text, key):
    decry_text = []
    key = generateKey(len(cipher_text), key)
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 256) % 256
        # x += ord('A')
        decry_text.append(chr(x))
    return("" . join(decry_text))

def num_to_arr(num): # chuyển số thành mảng :)))
    arr = np.array([])
    for i in range(MAX_LEN_IMG):
        arr = np.insert(arr,0,num%10)
        num = num//10
    arr = arr.astype(int)
    return arr
def arr_to_num(arr): # Chuyển mảng về số
    num = 0
    for i in range(MAX_LEN_IMG):
        num+= arr[MAX_LEN_IMG-i-1] * 10 ** (i)
    return num


def formatImg(img):                                     # Chuyển ảnh sang vector
    img_format = np.array([len(img.shape),MAX_LEN_IMG])  # ô 0 lưu số chiều, ô 1 lưu độ dài tối đa của 1 độ dài ảnh        
                                                               
    for i in range(img_format[0]):
        conv_num = num_to_arr(img.shape[i])
        img_format = np.append(img_format, conv_num)   # (3*MAX_LEN_IMG) ô tiếp theo lưu cỡ của ảnh
    
    img_vector = np.reshape(img,-1)
    img_format = np.append(img_format, img)
    return img_format.astype(np.uint8)

def resImg(img):                                    # Chuyển từ vector về ảnh 
    dim = img[0]
    max_len = img[1]
    res_num = []
    for i in range(1,dim):
        res_num.append(arr_to_num(img[i*10+2 : i*10+12]))
    img_res = np.array(img[2+dim*max_len : ])
    res_num.insert(0,-1)
    img_res = np.reshape(img_res , res_num)
    return img_res.astype(np.uint8)

def cipherImg(img, key):
    print("Proceed to encode the image...")
    format = formatImg(img)
    key = generateKey(format.size, key)
    cip = []
    for i in range(format.size):
        x =  (format[i] + ord(key[i]) ) % 256
        cip.append(chr(x))
        if(i%100000 == 0) : print(i,'/',format.size)
    print("Done")
    return ("".join(cip))

def decryptedImg(img, key):
    print("Proceed to decode the image...")
    key = generateKey(len(img), key)
    dec = []
    for i in range(len(img)):
        x =  (ord(img[i]) - ord(key[i]) + 256) % 256
        dec.append(x)
        if(i%100000 == 0) : print(i,'/',len(img))
    print("Done")
    return resImg(dec)

f = cv2.imread('C:\\Users\\admin\\Desktop\\Temp\\pixel.png')
# f = cv2.imread('test_cip.png')
img = np.array(f)

# # print(np.reshape(img,-1))
# print(len(img.shape))

# arr.insert(0,(0,1))
# print(arr)
# text = "HELLOWORLD  dme"
# key = generateKey(len(text),"DKA")
# cip = cipherText(text,key)
# # f.write(cip)
# for i in cip:
#     # f.write(i+'\t')
#     f.write(str(ord(i))+'\n')
# # print(f.read)
# decry = decryptedText(cip, key)
# print(cip)
# print(decry)

# print(chr(255))

a = cipherImg(img,"Duy")
print(a)
a = decryptedImg(a,"Duy")
# a = resImg(a)
# print(a.shape)
# print(a.size)
cv2.imshow("abc",a)
cv2.waitKey(0)
cv2.destroyAllWindows()


# print(ord(chr(880)))


