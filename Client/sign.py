from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

import getpass
# -*- coding: utf-8 -*-

def createSignature(pathToPrivateKey, prehashed):
    file = open(pathToPrivateKey, "r")
    serialized_private = ''.join(file.readlines())

    password = getpass.getpass("Enter your password>")
    try:
        private_key = serialization.load_pem_private_key(
        serialized_private,
        password=bytes(password),
        backend=default_backend()
        )
        signature = private_key.sign(
            prehashed,
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    except:
        print "Wrong password."
        return createSignature(pathToPrivateKey, prehashed)

def verifySignature(serialized_public, signature, prehashed):
    #file = open(pathToPublicKey, "r")
    #serialized_public = ''.join(file.readlines())
    public_key = serialization.load_pem_public_key(
        serialized_public,
        backend=default_backend()
    )

    try:
        public_key.verify(signature, prehashed, ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False

def createSerializedKeys(password):
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    serialized_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(password))
    )
    file = open("private.pem", "w")
    file.write(serialized_private)
    file.close()
    public_key = private_key.public_key()
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    file = open("public.pem", "w")
    file.write(serialized_public)
    file.close()