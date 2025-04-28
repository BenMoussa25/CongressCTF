from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from secret import FLAG

def pkcs1_v1_5_pad(message, key_size):
    max_message_length = key_size - 11
    if len(message) > max_message_length:
        raise ValueError("Message too long")

    padding_length = key_size - len(message) - 3
    padding = b''
    while len(padding) < padding_length:
        b = b'\x69'
        if b != b'\x00':
            padding += b

    return b'\x00\x02' + padding + b'\x00' + message

def pkcs1_v1_5_unpad(padded):
    if len(padded) < 11 or padded[0:2] != b'\x00\x02':
        raise ValueError("Incorrect padding")

    sep_index = padded.find(b'\x00', 2)
    if sep_index == -1 or sep_index < 10:
        raise ValueError("Padding separator not found or too short")

    return padded[sep_index + 1:]

def rsa_encrypt(message, pub_key):
    key_size = pub_key.size_in_bytes()
    padded = pkcs1_v1_5_pad(message, key_size)
    m = bytes_to_long(padded)
    c = pow(m, pub_key.e, pub_key.n)
    return c

def rsa_decrypt(ciphertext, priv_key):
    key_size = priv_key.size_in_bytes()
    m = pow(ciphertext, priv_key.d, priv_key.n)
    padded = long_to_bytes(m, key_size)
    return pkcs1_v1_5_unpad(padded)

def rsa_check(ciphertext, priv_key):
    key_size = priv_key.size_in_bytes()
    m = pow(ciphertext, priv_key.d, priv_key.n)
    padded = long_to_bytes(m, key_size)
    return padded[0:2] == b'\x00\x02'


def main():
    # Generate RSA key pair
    key = RSA.generate(1024)
    pub_key = key.publickey()
    priv_key = key
    enc_flag = rsa_encrypt(FLAG, pub_key)
    while True:
        c = input("choice: ")
        if c == '1':
            print("enc_flag: ", enc_flag)
            print("n: ", pub_key.n)
            print("e: ", pub_key.e)
        elif c == '2':
            c = int(input("ciphertext: "))
            if rsa_check(c, priv_key):
                print("correct")
            else:
                print("incorrect")
        else:
            print("Invalid choice")
            break
    print("Exiting...")

if __name__ == "__main__":
    main()