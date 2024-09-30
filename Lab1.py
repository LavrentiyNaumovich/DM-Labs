import random

# Function to perform modular exponentiation
def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1 
        base = (base * base) % modulus
    return result

# Iterative Extended Euclidean Algorithm to find modular inverse
def egcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

def mod_inverse(e, phi):
    gcd, x, y = egcd(e, phi)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

# Miller-Rabin Primality Test
def is_prime(n, k=128):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r +=1
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = mod_pow(a, d, n)
        if x == 1 or x == n -1:
            continue
        for _ in range(r -1):
            x = mod_pow(x, 2, n)
            if x == n -1:
                break
        else:
            return False
    return True

# Function to generate a random prime number of bit length 'bits'
def generate_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        # Ensure it's odd and has the highest bit set
        prime_candidate |= (1 << bits -1) | 1
        if is_prime(prime_candidate):
            return prime_candidate

# RSA Key Generation
def generate_keys():
    bits = 1024
    print("Generating p...")
    p = generate_prime(bits)
    print("Generating q...")
    q = generate_prime(bits)
    n = p * q
    phi = (p -1)*(q -1)
    e = 65537  
    d = mod_inverse(e, phi)
    return (n, e, d)

# Encryption function
def encrypt(message, n, e):
    # Convert message to integer
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    if message_int > n:
        raise ValueError("Message too large to encrypt with given key.")
    cipher_int = mod_pow(message_int, e, n)
    return cipher_int

# Decryption function
def decrypt(cipher_int, n, d):
    message_int = mod_pow(cipher_int, d, n)
    # Convert integer back to bytes
    message_length = (message_int.bit_length() + 7) // 8
    message = message_int.to_bytes(message_length, byteorder='big').decode('utf-8')
    return message


# Main Program
if __name__ == "__main__":
    n, e, d = generate_keys()
    message = "This is a secret message."
    print(f"Original Message: {message}")
    # Encrypt the message
    cipher_int = encrypt(message, n, e)
    print(f"Encrypted Message: {cipher_int}")
    # Decrypt the message
    decrypted_message = decrypt(cipher_int, n, d)
    print(f"Decrypted Message: {decrypted_message}")
