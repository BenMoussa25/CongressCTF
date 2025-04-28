from Crypto.Cipher import AES
from os import urandom
from Crypto.Util.Padding import pad
from secret import FLAG


KEY = urandom(16)


def encrypt_aes_ecb_with_payload(plaintext):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext + FLAG ,16))

def choices():
    print("1. Encrypt")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        return True
    elif choice == '2':
        return False
    else:
        print("Invalid choice. Please try again.")
        return choices()

def main():
    while True:
        c = choices()
        if c:
            i = input('what do u wanna ecrypt? ')
            print(encrypt_aes_ecb_with_payload(bytes.fromhex(i)).hex())
        else:
            print("Exiting...")
            exit(0)



if __name__ == "__main__":
    main()
