#!/bin/bash
set -e

mkdir -p certs
cd certs

# Step 1: Generate CA key and certificate
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/CN=Test CA"

# Step 2: Generate server key and certificate signing request (CSR)
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256

# Step 3: Generate client (musician) key and certificate signing request (CSR)
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/CN=musician-client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 -sha256

# Cleanup
rm -f *.csr *.srl

echo "Certificates generated in ./certs:"
ls -1 *.crt *.key
