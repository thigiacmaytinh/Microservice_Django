import string
import random

def GenerateRandomString(length=10):
    return ''.join(random.choices(string.ascii_lowercase + "_" + string.ascii_uppercase +  string.digits, k=length))

def GenerateRandomNumber(min, max):
    n = random.randint(min, max)
    return n