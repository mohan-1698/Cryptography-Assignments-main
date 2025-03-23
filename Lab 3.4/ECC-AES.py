from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

def generate_key_pair():
    curve = registry.get_curve('brainpoolP256r1')
    private_key = secrets.randbelow(curve.field.n)
    public_key = private_key * curve.g
    return private_key, public_key

def encrypt_AES_GCM(msg, secret_key):
    cipher = AES.new(secret_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return cipher.nonce, ciphertext, tag

def decrypt_AES_GCM(encrypted_data, secret_key):
    nonce, ciphertext, tag = encrypted_data
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

def derive_shared_secret(private_key, public_key):
    shared_secret = private_key * public_key
    return hashlib.sha256(int.to_bytes(shared_secret.x, 32, 'big')).digest()

private_key_A, public_key_A = generate_key_pair()
private_key_B, public_key_B = generate_key_pair()

shared_secret_A = derive_shared_secret(private_key_A, public_key_B)
shared_secret_B = derive_shared_secret(private_key_B, public_key_A)
assert shared_secret_A == shared_secret_B, "Shared secrets do not match!"

message = "Hello, SRM AP"
nonce, ciphertext, tag = encrypt_AES_GCM(message, shared_secret_A)
print(f"Ciphertext: {binascii.hexlify(ciphertext).decode()}")

decrypted_message = decrypt_AES_GCM((nonce, ciphertext, tag), shared_secret_B)
print(f"Decrypted Message: {decrypted_message}")
