import os
import shutil
import threading
import base64
from .TGMTutil import GenerateRandomString
from Crypto.PublicKey import RSA
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.serialization import load_pem_private_key
# from cryptography.hazmat.primitives.serialization import load_der_public_key
import ast
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify, unhexlify
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
import binascii
from Crypto.Hash import SHA256

####################################################################################################

def GenKeyPair():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    return private_key, public_key

####################################################################################################

def Encrypt(content, key):
    encryptor = PKCS1_OAEP.new(key)
    encrypted = encryptor.encrypt(content.encode('utf-8'))
    encrypted = hexlify(encrypted)
    return encrypted

####################################################################################################

def Decrypt(content, key):
    content = unhexlify(content)
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(ast.literal_eval(str(content)))
    return decrypted

####################################################################################################

def Sign(message, private_key):
    hash = SHA256.new(message.encode())
    signer = PKCS115_SigScheme(private_key)
    signature = signer.sign(hash)
    signature = binascii.hexlify(signature).decode()
    return signature

####################################################################################################

def Verify(message, signature, public_key):
    signature = binascii.unhexlify(signature)
    hash = SHA256.new(message.encode())
    verifier = PKCS115_SigScheme(public_key)
    try:
        verifier.verify(hash, signature)
        return True
    except:
        return False

####################################################################################################

def ReadFile(filePath):
    f = open(filePath, 'r')
    content = f.read()
    f.close()
    return content

####################################################################################################

def LoadPubKey(filePath):
    file = open(filePath,'r')
    key_data = file.read()
    return ParsePubKey(key_data)

####################################################################################################

def LoadPriKey(filePath):
    file = open(filePath,'r')
    key_data = file.read()
    return ParsePriKey(key_data)

####################################################################################################

def ParsePubKey(key_data):
    key = RSA.import_key(key_data)
    return key

####################################################################################################

def ParsePriKey(key_data):
    key = RSA.import_key(key_data)
    return key

####################################################################################################

def SavePriKey(privateKey, filename):
    try:
        with open(filename, 'w+') as keyfile:
            keyfile.write(privateKey.exportKey('PEM').decode())
            keyfile.close()
    except Exception as e:
        print ("[*] Error creating your key", e)

####################################################################################################

def SavePubKey(publicKey, filename):
    try:
        with open(filename, 'w+') as keyfile:
            keyfile.write(publicKey.exportKey('PEM').decode())
            keyfile.close()
    except Exception as e:
        print ("[*] Error creating your key", e)

####################################################################################################

# private_key, public_key = GenKeyPair()



#public_key = LoadPubKey("pub.ppk")
#private_key = LoadPriKey("pri.ppk")

# message = b'Hello world'


#signature = Sign("03D402741284547763360160435-0550-2E06-900700080009", private_key)
#print(signature)
