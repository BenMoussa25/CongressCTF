from pwn import *

# Connect to the remote server
r = remote('161.35.212.46', 6000)

BLOCK_SIZE = 16

def encrypt(plaintext):
    r.recvuntil(b"choice:")
    r.sendline(b"1")
    r.recvuntil(b"ecrypt? ")
    r.sendline(plaintext.hex().encode())
    encrypted = r.recvline().strip()
    return bytes.fromhex(encrypted.decode())

def find_flag():
    known = b''
    
    while True:
        pad_len = (BLOCK_SIZE - (len(known) + 1) % BLOCK_SIZE)
        padding = b'A' * pad_len
        base_cipher = encrypt(padding)
        
        block_num = (len(padding) + len(known)) // BLOCK_SIZE

        # Build dictionary
        lookup = dict()
        for i in range(256):
            guess = padding + known + bytes([i])
            guess_cipher = encrypt(guess)
            lookup[guess_cipher[block_num*BLOCK_SIZE:(block_num+1)*BLOCK_SIZE]] = i
        
        target_block = base_cipher[block_num*BLOCK_SIZE:(block_num+1)*BLOCK_SIZE]
        
        if target_block in lookup:
            next_byte = lookup[target_block]
            known += bytes([next_byte])
            print(known)
        else:
            print("FLAG RECOVERED:", known)
            break

find_flag()
