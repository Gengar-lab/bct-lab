#!/bin/bash

# =============================================
# Digital Signature Demo
# This script demonstrates digital signature creation and verification
# It will generate an RSA key pair, sign a message, and verify the signature
# =============================================

# Generate a 2048-bit RSA private key
# This key will be used for signing
# The key will be saved in PEM format
openssl genrsa -out private.pem 2048

# Extract the public key from the private key
# This key will be used for verification
# It can be shared with others
openssl rsa -in private.pem -pubout -out public.pem

# Create a sample message
# This will be our message that we want to sign
echo "Hello, this is a message to sign!" > message.txt

echo "Original message:"
cat message.txt

# Create a digital signature using SHA-256 and the private key
# -sha256: Uses SHA-256 for hashing
# -sign: Creates a signature using the private key
# The signature is saved in binary format
openssl dgst -sha256 -sign private.pem -out signature.bin message.txt

echo -e "\nDigital signature (in base64 format):"
base64 signature.bin

# Verify the signature using the public key
# -verify: Verifies the signature
# -signature: Specifies the signature file
# This should succeed for the original message
openssl dgst -sha256 -verify public.pem -signature signature.bin message.txt

# Try verifying with a modified message
# This should fail as the message has been altered
# Demonstrates that any change to the message invalidates the signature
echo "Hello, this is a modified message!" > modified.txt
openssl dgst -sha256 -verify public.pem -signature signature.bin modified.txt

# Clean up temporary files
# Remove all generated files to keep the directory clean
rm private.pem public.pem message.txt modified.txt signature.bin

echo -e "\n=== Demo Complete ==="