import hashlib
import random

def Com(r, m):
    str = f"{r}{m}".encode()
    return hashlib.sha256(str).hexdigest()

def dieCalc(a, b):
    return ((int(a) ^ int(b)) % 6) + 1

def randBitStr(n):
    result = ""
    for _ in range(n):
        temp = str(random.randint(0, 1))
        result += temp
    return result

def randDie():
    return random.randint(1, 6)