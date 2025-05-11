import hashlib
import time
import argparse
from typing import Tuple

def find_nonce(data: str, prefix: str) -> Tuple[int, str, float]:
    start_time = time.time()
    nonce = 0
    
    while True:
        string_to_hash = f"{data}{nonce}"
        hash_result = hashlib.sha256(string_to_hash.encode()).hexdigest()
        
        if hash_result.startswith(prefix):
            end_time = time.time()
            return nonce, hash_result, end_time - start_time
        
        nonce += 1

def main():
    parser = argparse.ArgumentParser(description='Find a nonce that produces a hash with a given prefix')
    parser.add_argument('--data', type=str, default="Hello, Blockchain!",
                      help='The data to hash (default: "Hello, Blockchain!")')
    parser.add_argument('--prefix', type=str, default="0000",
                      help='The prefix that the hash should start with (default: "0000")')
    
    args = parser.parse_args()
    
    print(f"\nFinding nonce for prefix: {args.prefix}")
    nonce, hash_result, time_taken = find_nonce(args.data, args.prefix)
    
    print(f"Data: {args.data}")
    print(f"Nonce: {nonce}")
    print(f"Hash: {hash_result}")
    print(f"Time taken: {time_taken:.2f} seconds")
    
    verification = hashlib.sha256(f"{args.data}{nonce}".encode()).hexdigest()
    print(f"Verification: {verification}")
    print(f"Verification successful: {verification == hash_result}")

if __name__ == "__main__":
    main() 

# python nonce_finder.py --data "Hello Blockchain" --prefix "0000"