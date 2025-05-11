#!/bin/bash

# =============================================
# AES-256-CBC Symmetric Encryption Demo
# This script demonstrates symmetric encryption using AES-256-CBC mode
# It will generate a key, encrypt a message, and then decrypt it back
# =============================================

# Generate a random 256-bit key (32 bytes) and save it to a file
# This key will be used for both encryption and decryption
openssl rand -hex 32 > key.txt

# Generate a random 128-bit IV (16 bytes) and save it to a file
# The IV is required for CBC mode to ensure the same plaintext
# doesn't produce the same ciphertext
openssl rand -hex 16 > iv.txt

# Create a sample message file
# This will be our plaintext that we want to encrypt
echo "Hello, this is a secret message!" > message.txt

echo "Original message:"
cat message.txt

# Encrypt the message using AES-256-CBC
# -aes-256-cbc: Uses AES in CBC mode with 256-bit key
# -K: Specifies the key in hex format
# -iv: Specifies the initialization vector in hex format
# Output will be in binary format
openssl enc -aes-256-cbc -in message.txt -out encrypted.bin -K $(cat key.txt) -iv $(cat iv.txt)

echo -e "\nEncrypted message (in hex format):"
xxd encrypted.bin

# Decrypt the message using the same key and IV
# -d: Decrypt mode
# Uses the same key and IV as encryption
# Converts binary back to text
openssl enc -aes-256-cbc -d -in encrypted.bin -out decrypted.txt -K $(cat key.txt) -iv $(cat iv.txt)

echo -e "\nDecrypted message:"
cat decrypted.txt

# Clean up temporary files
# Remove all generated files to keep the directory clean
rm key.txt iv.txt message.txt encrypted.bin decrypted.txt

echo -e "\n=== Demo Complete ==="