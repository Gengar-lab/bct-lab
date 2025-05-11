#!/bin/bash

# =============================================
# Self-Signed Certificate Demo
# This script demonstrates the creation of a self-signed certificate
# It will generate a private key and create a certificate valid for 365 days
# =============================================

# Generate a 2048-bit RSA private key
# This key will be used to sign the certificate
# The key will be saved in PEM format
openssl genrsa -out private.pem 2048

# Generate a self-signed certificate
# -new: Creates a new certificate request
# -x509: Creates a self-signed certificate
# -key: Specifies the private key to use
# -days: Sets the validity period
# -subj: Sets the subject information
openssl req -new -x509 -key private.pem -out certificate.pem -days 365 -subj "/CN=localhost/O=My Organization/C=US"

# Display certificate information
# -text: Shows the certificate in text format
# -noout: Prevents output of the encoded certificate
openssl x509 -in certificate.pem -text -noout

# Clean up temporary files
# Remove all generated files to keep the directory clean
rm private.pem certificate.pem

echo -e "\n=== Demo Complete ==="