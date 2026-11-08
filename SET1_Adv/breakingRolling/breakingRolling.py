import base64
import itertools

numCHUNKS = 20

#HAMMING DISTANCES
def hammingDist(b1: bytes, b2: bytes) -> int:
    if len(b1) != len(b2):
        raise ValueError("Strings must be of equal length")
    return sum((a ^ b).bit_count() for a, b in zip(b1, b2))

def normalizedHamming(b1: bytes, b2: bytes) -> float:
    return hammingDist(b1,b2)/len(b1)

#FILE
with open('/home/ocean/Documents/Code/cryptography/SET1_Adv/breakingRolling/file.txt', 'r') as f:
    ciphertext = base64.b64decode(f.read())

#KEYSIZE FINDER
results = []
for KEYSIZE in range(2, 41):
    ctList = []
    for i in range(numCHUNKS):
        ctExcerpt = ciphertext[i*KEYSIZE:(i+1)*KEYSIZE]
        ctList.append(ctExcerpt)


    scores = [normalizedHamming(a,b) for a,b in itertools.combinations(ctList,2)]
    results.append((sum(scores) / len(scores), KEYSIZE))

results.sort()
best5R = results[:5] #Best 5 results

#SCORING FUNCTION
LETTER_SCORES = {
    ord(c): weight for c, weight in {
        'e': 14, 't': 9, 'a': 8, 'o': 8, 'i': 7, 'n': 7, 's': 6, 'h': 6, 'r': 6,
        'd': 4, 'l': 4, 'c': 3, 'u': 3, 'm': 3, 'w': 2, 'f': 2, 'g': 2, 'y': 2,
        'p': 2, 'b': 1, 'v': 1, 'k': 1, 'j': 0.1, 'x': 0.1, 'q': 0.1, 'z': 0.1,
        ' ': 20
    }.items()
}
def textScoring(candidateBytes:bytes):
    score = sum(LETTER_SCORES.get(b | 0x20 if (65 <= b <= 90 or 97 <= b <= 122) else b, -10) for b in candidateBytes)
    return score

# BEST KEY FUNCTION
def bestKeyByte(group: bytes) -> int:
    bestKeyScore = float("-inf")
    bestK = 0

    for k in range(256):
        byteGroup = bytearray()
        for b in group:
            byteGroup.append(b ^ k)
        score = textScoring(byteGroup)

        if score > bestKeyScore:
            bestKeyScore = score
            bestK = k

    return bestK

# ROLLING KEY FUNCTION
def rollingKey(data: bytes, key: bytes)->bytes:
    plaintext = bytearray()
    for i, byte in enumerate(data):
            byteKey = key[i % len(key)]
            plaintext.append(byte ^ byteKey)
    return plaintext

#TRANSPOSITION& FINDING THE BEST KEY
bestKeysList = []
for _, N in best5R:
    keyString = bytearray()
    for j in range(N):
        ctTransposed = ciphertext[j::N]
        bestK = bestKeyByte(ctTransposed)
        keyString.append(bestK)
    bestKeysList.append(keyString) # First will always be the highest hamming score
print(bestKeysList)
firstBestK:bytes = bestKeysList[0] # First will have the highest hamming score

#DECRYPT THE FILE
candidates = []

for key in bestKeysList:
    candidateScore = 0
    pt = rollingKey(ciphertext, key)
    candidateScore = textScoring(pt)
    candidates.append((candidateScore, pt, key))

candidates.sort(reverse=True)
finalText = candidates[0][1]
print(candidates[0][0])
print(finalText.decode(errors="replace"))