from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import secrets

def generate_dh_keypair(prime, base):
    private_key = secrets.randbelow(prime)
    public_key = pow(base, private_key, prime)
    return private_key, public_key

def compute_shared_key(private_key, received_public, prime):
    return pow(received_public, private_key, prime)

PRIME = 23
BASE = 5

alice_private, alice_public = generate_dh_keypair(PRIME, BASE)
bob_private, bob_public = generate_dh_keypair(PRIME, BASE)

alice_shared_key = compute_shared_key(alice_private, bob_public, PRIME)
bob_shared_key = compute_shared_key(bob_private, alice_public, PRIME)

session_key = hashlib.sha256(str(alice_shared_key).encode()).digest()[:16]

def generate_sha512_hash(text):
    return hashlib.sha512(text.encode()).hexdigest()

def encrypt_message(plaintext, key):
    hash_code = generate_sha512_hash(plaintext)
    full_message = plaintext + hash_code

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_message = cipher.encrypt(pad(full_message.encode(), AES.block_size))

    return iv + encrypted_message

def decrypt_message(encrypted_data, key):
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size).decode()

    received_text = decrypted_message[:-128]
    received_hash = decrypted_message[-128:]

    if generate_sha512_hash(received_text) == received_hash:
        return f"Integrity Verified! Message: {received_text}"
    else:
        return "Integrity Check Failed!"

message = "Hello, Secure World!"
encrypted_data = encrypt_message(message, session_key)
print(f"Encrypted Data Sent: {encrypted_data.hex()}")

decrypted_text = decrypt_message(encrypted_data, session_key)
print(decrypted_text)
