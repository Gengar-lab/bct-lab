#!/bin/bash

# =============================================
# RSA Public Key Cryptography Demo
# This script demonstrates RSA encryption and decryption
# It will generate an RSA key pair, encrypt a message, and then decrypt it
# =============================================

# Generate a 2048-bit RSA private key
# This is a secure key size for RSA
# The key will be saved in PEM format
openssl genrsa -out private.pem 2048

# Extract the public key from the private key
# The public key can be shared with others
# It will be used for encryption
openssl rsa -in private.pem -pubout -out public.pem

# Create a sample message
# This will be our plaintext that we want to encrypt
echo "Hello, this is a secret message!" > message.txt

echo "Original message:"
cat message.txt

# Encrypt the message using the public key
# -encrypt: Specifies encryption mode
# -pubin: Indicates we're using a public key
# -inkey: Specifies the key file
# Only the private key can decrypt this message
openssl pkeyutl -encrypt -pubin -inkey public.pem -in message.txt -out encrypted.bin

echo -e "\nEncrypted message (in base64 format):"
base64 encrypted.bin

# Decrypt the message using the private key
# -decrypt: Specifies decryption mode
# -inkey: Specifies the private key file
# This demonstrates that only the private key can decrypt the message
openssl pkeyutl -decrypt -inkey private.pem -in encrypted.bin -out decrypted.txt

echo -e "\nDecrypted message:"
cat decrypted.txt

# Clean up temporary files
# Remove all generated files to keep the directory clean
rm private.pem public.pem message.txt encrypted.bin decrypted.txt

echo -e "\n=== Demo Complete ==="