import requests

# Server URL
BASE_URL = "https://l5xwzx0n-5000.inc1.devtunnels.ms/"  # Update the URL if the server is hosted elsewhere

def main():
    print("Select Encryption Method:")
    print("1. Vigenere Cipher")
    print("2. Playfair Cipher")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice! Exiting.")
        return

    text = input("Enter the text to encrypt: ").strip()
    key = input("Enter the key: ").strip()

    # API endpoint and payload
    if choice == "1":
        encrypt_endpoint = f"{BASE_URL}/vignere-encrypt"
        decrypt_endpoint = f"{BASE_URL}/vignere-decrypt"
    else:
        encrypt_endpoint = f"{BASE_URL}/playfair-encrypt"
        decrypt_endpoint = f"{BASE_URL}/playfair-decrypt"

    # Send text for encryption
    encrypt_response = requests.post(encrypt_endpoint, json={"text": text, "key": key})

    if encrypt_response.status_code == 200:
        encrypt_data = encrypt_response.json()
        print("\nEncryption Successful!")
        print(f"Original Text: {encrypt_data['plain_text']}")
        print(f"Encrypted Text: {encrypt_data['encrypted_text']}")
    else:
        print("\nEncryption Failed!")
        print(encrypt_response.json())
        return

    # Send ciphertext for decryption
    encrypted_text = encrypt_data["encrypted_text"]
    decrypt_response = requests.post(decrypt_endpoint, json={"text": encrypted_text, "key": key})

    if decrypt_response.status_code == 200:
        decrypt_data = decrypt_response.json()
        print("\nDecryption Successful!")
        print(f"Decrypted Text: {decrypt_data.get('plain_text', decrypt_data.get('decrypted_text'))}")
    else:
        print("\nDecryption Failed!")
        print(decrypt_response.json())

if __name__ == "__main__":
    main()
