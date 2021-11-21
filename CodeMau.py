import cv2
import numpy as np

# ***************** Phần định nghĩa hàm này bỏ qua, đọc cách sử dụng bên dưới là biết liền hà :P *****************************

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




# *******************************************************
# ************** Cách sử dụng nà :V *********************
# *******************************************************



# ************** Mã hóa văn bản ****************

text = "hế lô khải"
key = "lêu lêu"
# cip là văn bản đã được mã hóa (string)
cip = cipherText(text,key)
print("Encode: ",cip)
# de là văn bản đã được giải mã (string)
de = decryptedText(cip,key)
print("Decode: ",de)

# ************** Mã hóa ảnh ****************

path = ""
key = "nhìn gì mà nhìn, đánh cho giờ"

file_img = cv2.imread(path) # Đọc ảnh bằng cv2 -> Array 3 chiều
img = np.array(file_img)    # Chuyển Array thường thành Array của numpy

# cip là ảnh được mã hóa (Array 3 chiều của numpy)
cip = encodeImg(img,key)
cv2.imshow("Image after encoding", cip) # show nó ra thôi :))


# Lưu ảnh đã mã hóa
tail = "." + path.split(".")[-1] # Lấy ra đuôi của file ảnh ban đầu VD: "C:/Kai.png" -> ".png"
path_save = "./"  # ./ là thư mục đang chạy này
name = "encode_Img" # Tên (Không cần đuôi)
cv2.imwrite(path_save + name + tail, cip) #  Lưu file
print("Ảnh mã hóa đã được lưu vào: ", path_save + name + tail)

# de là ảnh được giải mã (Array 3 chiều của numpy)
de = decodeImg(cip,key)
cv2.imshow("Image after decoding", de)


cv2.waitKey(0)
cv2.destroyAllWindows()