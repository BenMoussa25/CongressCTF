from z3 import *

# Target hash (hex string converted to bytes)
target_hash_hex = input()
target_hash = bytes.fromhex(target_hash_hex)

def bytes_to_uint32(b):
    return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]

def uint32_to_bytes(val):
    return [(val >> 24) & 0xFF, (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF]

def z3_avalanche(state):
    # Implement the avalanche function with Z3
    state = state ^ LShR(state, 16)
    state = (state * 0x85ebca6b) & 0xFFFFFFFF
    state = state ^ LShR(state, 13)
    state = (state * 0xc2b2ae35) & 0xFFFFFFFF
    state = state ^ LShR(state, 16)
    return state

def solve_hash():
    # Create a solver instance
    s = Solver()
    
    # Setup the constants from the original hash function
    HASH_SIZE = int(input())
    initial_states = [
        0xDEADBEEF, 0xB16B00B5, 0xCAFEBABE, 0xF00DDEAD,
        0xFACEB00C, 0x8BADF00D, 0xDEADC0DE, 0xFEEDFACE
    ]
    
    # Let's try a reasonable length for the input
    # Start with a shorter input - let's try 8 characters first
    input_length = int(input())
    input_chars = [BitVec(f'input_{i}', 8) for i in range(input_length)]
    
    # Constrain input to printable ASCII
    for c in input_chars:
        s.add(c >= 32, c <= 126)
    
    # Model the hash function
    states = [BitVecVal(state, 32) for state in initial_states]
    
    # Process each input character
    for pos in range(0, input_length, 16):
        chunk_size = min(16, input_length - pos)
        for i in range(chunk_size):
            if pos + i < input_length:
                byte = input_chars[pos + i]
                for j in range(8):
                    shift_amount = (j * 8) % 32
                    states[j] = states[j] ^ (ZeroExt(24, byte) << shift_amount)
                    states[j] = z3_avalanche(states[j])
    
    # Apply length in bits
    length_bits = input_length * 8
    states[0] = states[0] ^ BitVecVal(length_bits & 0xFFFFFFFF, 32)
    states[1] = states[1] ^ BitVecVal(length_bits >> 32, 32)
    
    # Final avalanche for all states
    for i in range(8):
        states[i] = z3_avalanche(states[i])
    
    # Create hash result array (as BitVec variables)
    hash_result = [BitVec(f'hash_{i}', 8) for i in range(HASH_SIZE)]
    
    # Fill the hash result from the states
    for i in range(HASH_SIZE):
        hash_result[i] = Extract(7, 0, LShR(states[i % 8], ((i % 4) * 8)))
    
    # Model mix_bits function
    def mix_bits(hash_vars):
        result = hash_vars.copy()
        for i in range(0, HASH_SIZE - 4, 4):
            chunk = Concat(result[i], result[i+1], result[i+2], result[i+3])
            chunk = z3_avalanche(chunk)
            result[i] = Extract(31, 24, chunk)
            result[i+1] = Extract(23, 16, chunk)
            result[i+2] = Extract(15, 8, chunk)
            result[i+3] = Extract(7, 0, chunk)
        return result
    
    # Apply mix_bits twice
    hash_result = mix_bits(hash_result)
    hash_result = mix_bits(hash_result)
    
    # Add constraints for target hash
    for i in range(HASH_SIZE):
        s.add(hash_result[i] == target_hash[i])
    
    if s.check() == sat:
        m = s.model()
        solution = ''.join(chr(m[c].as_long()) for c in input_chars)
        return solution
    else:
        print("No solution found for this input length")
        return None

if __name__ == "__main__":
    solution = solve_hash()
    if solution:
        print(solution)
    else:
        print("Failed to find a solution")