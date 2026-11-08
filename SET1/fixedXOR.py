plaintext = bytes.fromhex("1c0111001f010100061a024b53535009181c")
key = bytes.fromhex("686974207468652062756c6c277320657965")

output = bytes(a ^ b for a,b in zip(plaintext,key))
print(output.hex())