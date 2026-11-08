
# Standard English letter frequency weights
LETTER_SCORES = {
    ord(c): weight for c, weight in {
        'e': 13, 't': 9, 'a': 8, 'o': 8, 'i': 7, 'n': 7, 's': 6, 'h': 6, 'r': 6,
        'd': 4, 'l': 4, 'c': 3, 'u': 3, 'm': 3, 'w': 2, 'f': 2, 'g': 2, 'y': 2,
        'p': 2, 'b': 1, 'v': 1, 'k': 1, 'j': 0.1, 'x': 0.1, 'q': 0.1, 'z': 0.1,
        ' ': 15
    }.items()
}

best_score = float('-inf')
best_plaintext = ""
best_key = 0

with open("cryptography/SET1/singleStringXOR/file.txt", "r") as f:
    for line in f:
        ciphertext = bytes.fromhex(line.strip())
        for key in range(256):
            candidate_bytes = bytes(b ^ key for b in ciphertext)
            
            # Score based on lowercase letter matches
            score = sum(LETTER_SCORES.get(b | 0x20 if (65 <= b <= 90 or 97 <= b <= 122) else b, -10) for b in candidate_bytes)

            if score > best_score:
                best_score = score
                best_key = key
                best_plaintext = candidate_bytes.decode('ascii', errors='replace')

        if score > best_score:
                        best_score = score
                        best_key = key
                        best_plaintext = candidate_bytes.decode('ascii', errors='replace')

print(f"Key: {chr(best_key)}")
print(f"Decrypted text: {best_plaintext}")