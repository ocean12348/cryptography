import base64
from Crypto.Cipher import AES 


#VARS
KEY = b"YELLOW SUBMARINE"

#PKCS#7 PADDING
def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    n = block_size - (len(data) % block_size)
    return data + bytes([n]) * n

#PKCS#7 UNPADDING
def pkcs7_unpad(data: bytes) -> bytes:
    padLength = int.from_bytes(data[len(data)-1:len(data)])
    return data[:len(data)-padLength]

#BYTEWISE XOR
def byteXOR(x:bytes, y:bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(x, y))


#CIPHER
cipher = AES.new(KEY, AES.MODE_ECB)

#AES128CBC
def encryptAES128CBC(plaintext):
    IV = pkcs7_pad("")
    byteXOR(IV)


#PROGRAM START
with open("/home/ocean/Documents/Code/cryptography/SET2/ImplementCBC/10.txt", 'r') as f:
    ciphertext = pkcs7_pad(base64.b64decode(f.read()))
    print(ciphertext)

    ct = bytearray()
    for i, byte in enumerate(ciphertext):
        byteKey = KEY[i % len(KEY)]
        ct.append(byte ^ byteKey)

    

