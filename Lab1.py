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

# Extended Euclidean Algorithm 
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

# Function to find the modular inverse
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
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r +=1
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
        prime_candidate |= (1 << (bits -1)) | 1
        if is_prime(prime_candidate):
            return prime_candidate

# RSA Key Generation and saving to files
def generate_keys():
    bits = 1024
    print("Generating p...")
    p = generate_prime(bits)
    print("Generating q...")
    q = generate_prime(bits)
    n = p * q
    phi = (p -1)*(q -1)
    e = 65537  
    try:
        d = mod_inverse(e, phi)
    except Exception as ex:
        print(f"Error computing d: {ex}")
        return None, None, None
    with open('public_key.txt', 'w') as f:
        f.write(f"{n}\n{e}")
    with open('private_key.txt', 'w') as f:
        f.write(f"{n}\n{d}")
    print("Keys generated and saved to 'public_key.txt' and 'private_key.txt'.")
    return (n, e, d)

# Function to encrypt a message
def encrypt(message, n, e):
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    if message_int > n:
        raise ValueError("Message too large for the given key.")
    cipher_int = mod_pow(message_int, e, n)
    return cipher_int

# Function to decrypt a message
def decrypt(cipher_int, n, d):
    message_int = mod_pow(cipher_int, d, n)
    message_length = (message_int.bit_length() + 7) // 8
    message = message_int.to_bytes(message_length, byteorder='big').decode('utf-8')
    return message

# Function to read the public key from file
def read_public_key():
    try:
        with open('public_key.txt', 'r') as f:
            n = int(f.readline())
            e = int(f.readline())
        return n, e
    except FileNotFoundError:
        print("Public key file not found. Please generate keys first.")
        return None, None
    except Exception as ex:
        print(f"Error reading public key: {ex}")
        return None, None

# Function to read the private key from file
def read_private_key():
    try:
        with open('private_key.txt', 'r') as f:
            n = int(f.readline())
            d = int(f.readline())
        return n, d
    except FileNotFoundError:
        print("Private key file not found. Please generate keys first.")
        return None, None
    except Exception as ex:
        print(f"Error reading private key: {ex}")
        return None, None

# Function to get user input for encryption
def get_message():
    choice = input("Encrypt from (1) Keyboard or (2) File? Enter 1 or 2: ")
    if choice == '1':
        message = input("Enter the message to encrypt: ")
        return message
    elif choice == '2':
        filename = input("Enter the filename to read the message from: ")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                message = f.read()
            return message
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as ex:
            print(f"Error reading file: {ex}")
            return None
    else:
        print("Invalid choice.")
        return None

# Function to get user input for decryption
def get_cipher():
    choice = input("Decrypt from (1) Keyboard or (2) File? Enter 1 or 2: ")
    if choice == '1':
        cipher = input("Enter the cipher integer to decrypt: ")
        try:
            cipher_int = int(cipher)
            return cipher_int
        except ValueError:
            print("Invalid integer.")
            return None
    elif choice == '2':
        filename = input("Enter the filename to read the cipher from: ")
        try:
            with open(filename, 'r') as f:
                cipher = f.read().strip()
                cipher_int = int(cipher)
            return cipher_int
        except FileNotFoundError:
            print("File not found.")
            return None
        except ValueError:
            print("Invalid integer in file.")
            return None
        except Exception as ex:
            print(f"Error reading file: {ex}")
            return None
    else:
        print("Invalid choice.")
        return None

# Main program with menu
def main_menu():
    while True:
        print("Choose an action(1-4):")
        print("1. Generate keys and save to files")
        print("2. Encrypt a message (from file or keyboard)")
        print("3. Decrypt a message (from file or keyboard)")
        print("4. Exit")
        choice = input("Your choice: ")

        if choice == '1':
            n, e, d = generate_keys()
            if n is None:
                print("Key generation failed.")
        elif choice == '2':
            n, e = read_public_key()
            if n is None or e is None:
                continue
            message = get_message()
            if message is None:
                continue
            try:
                cipher_int = encrypt(message, n, e)
                print(f"Encrypted Message: {cipher_int}")
                save_choice = input("Save cipher to file? (y/n): ").lower()
                if save_choice == 'y':
                    filename = input("Enter filename to save the cipher: ")
                    with open(filename, 'w') as f:
                        f.write(str(cipher_int))
                    print(f"Cipher saved to {filename}.")
            except ValueError as ve:
                print(ve)
            except Exception as ex:
                print(f"Encryption error: {ex}")
        elif choice == '3':
            n, d = read_private_key()
            if n is None or d is None:
                continue
            cipher_int = get_cipher()
            if cipher_int is None:
                continue
            try:
                decrypted_message = decrypt(cipher_int, n, d)
                print(f"Decrypted Message: {decrypted_message}")
                save_choice = input("Save decrypted message to file? (y/n): ").lower()
                if save_choice == 'y':
                    filename = input("Enter filename to save the decrypted message: ")
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(decrypted_message)
                    print(f"Decrypted message saved to {filename}.")
            except Exception as ex:
                print(f"Decryption error: {ex}")
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()
    
   
