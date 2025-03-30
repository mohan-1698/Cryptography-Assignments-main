import hashlib

def generate_sha512_hash(text):
    return hashlib.sha512(text.encode()).hexdigest()

message = "Hello, secure world!"
hash_code = generate_sha512_hash(message)
print(f"SHA-512 Hash: {hash_code}")
