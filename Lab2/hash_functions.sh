#!/bin/bash

# =============================================
# Cryptographic Hash Functions Demo
# This script demonstrates various hash functions and their properties
# It will show MD5, SHA-1, SHA-256, and SHA-512 hashes
# =============================================

# Create a sample message
# This will be our input for all hash functions
echo "Hello, World!" > message.txt

echo "Original message:"
cat message.txt

# Calculate MD5 hash
# MD5 produces a 128-bit (16-byte) hash
# Note: MD5 is considered cryptographically broken
# -md5: Specifies MD5 algorithm
openssl dgst -md5 message.txt

# Calculate SHA-1 hash
# SHA-1 produces a 160-bit (20-byte) hash
# Note: SHA-1 is also considered cryptographically weak
# -sha1: Specifies SHA-1 algorithm
openssl dgst -sha1 message.txt

# Calculate SHA-256 hash
# SHA-256 produces a 256-bit (32-byte) hash
# This is currently considered cryptographically secure
# -sha256: Specifies SHA-256 algorithm
openssl dgst -sha256 message.txt

# Calculate SHA-512 hash
# SHA-512 produces a 512-bit (64-byte) hash
# This is currently considered cryptographically secure
# -sha512: Specifies SHA-512 algorithm
openssl dgst -sha512 message.txt

# Demonstrate avalanche effect
# This shows how a small change in input produces a large change in output
# We'll modify the message slightly and compare hashes
echo "Hello, World!!" > modified.txt

echo -e "\nModified message:"
cat modified.txt

echo -e "\nModified message hashes:"
echo "MD5:"
openssl dgst -md5 modified.txt
echo "SHA-256:"
openssl dgst -sha256 modified.txt

# Clean up temporary files
# Remove all generated files to keep the directory clean
rm message.txt modified.txt

echo -e "\n=== Demo Complete ==="