import base64
from Crypto.Cipher import AES 

KEY = b"YELLOW SUBMARINE"

with open("/home/ocean/Documents/Code/cryptography/SET1_Adv/AES128/file.txt", 'r') as f:
    ciphertext = base64.b64decode(f.read())

cipher = AES.new(KEY, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)
print(plaintext.decode(errors="replace"))
