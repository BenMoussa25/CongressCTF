HASH_SIZE = 32

# Reverse the deterministic shuffle
def reverse_shuffle_hash(hash_str):
    reversed_hash = [''] * HASH_SIZE
    for i in range(0, HASH_SIZE - 1, 2):
        reversed_hash[i] = hash_str[i + 1]
        reversed_hash[i + 1] = hash_str[i]
    return ''.join(reversed_hash)

# Reverse the reversible hash
def reverse_hash(hash_str):
    original = [''] * (HASH_SIZE + 1)
    # STATES (Reinitialize to the same values)
    states = [
        0xDEADBEEF,
        0xB16B00B5,
        0xCAFEBABE,
        0xF00DDEAD,
        0xFACEB00C
    ]
    # First, we need to reverse the shuffle
    reversed_hash = reverse_shuffle_hash(hash_str)
    # Simple reversible bitwise transformation with 5 states (keys)
    for i in range(HASH_SIZE):
        original[i] = chr(ord(reversed_hash[i]) ^ (states[i % 5] & 0xFF))  # XOR to get the original character
        states[i % 5] = (states[i % 5] >> 8) | (states[i % 5] << 24)  # Reverse the key's rotation
    original[HASH_SIZE] = '\0'  # Null-terminate the string
    # Remove padding (if any)
    for i in range(HASH_SIZE - 1, -1, -1):
        if original[i] == 'X':
            original[i] = '\0'
        else:
            break
    return ''.join(original).rstrip('\0')

def hex_to_hash(hex_str):
    return bytearray.fromhex(hex_str)

def main():
    hash_bytes = hex_to_hash("ccacc8dced7ed270c2bb10c845ad818faffc8eb5f08af2d0e17b8336e8a333f5")  # Convert the given hash to binary
    # Reversed hash to get the original input
    original = reverse_hash(hash_bytes.decode('latin1'))  # Decode bytes to string
    print(f"Flag: {original}")  # Print the original input

if __name__ == "__main__":
    main()
