import base64
import hashlib
import json
import os
import random
import string
import urllib.request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class CryptoUtils:
    def __init__(self):
        # Hardcoded encryption key (security smell)
        self.encryption_key = b'ThisIsA16ByteKey'  # insecure fixed key
        self.iv = b'ThisIsA16ByteIV.'  # insecure fixed IV
        self.salt = b'SaltySalt12345'  # insecure fixed salt
        self.iterations = 1000  # too few iterations
        self.hash_algorithm = 'md5'  # weak hash algorithm (security smell)
        self.key_cache = {}
        self.backend = default_backend()
    
    def generate_random_string(self, length=16):
        # Uses predictable random (not cryptographically secure)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def hash_password(self, password):
        # Weak password hashing (security smell)
        if self.hash_algorithm == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif self.hash_algorithm == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif self.hash_algorithm == 'sha256':
            # Better, but still not using proper password hashing
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            # Default to MD5 (weak)
            return hashlib.md5(password.encode()).hexdigest()
    
    def verify_password(self, stored_hash, password):
        # Vulnerable to timing attack
        computed_hash = self.hash_password(password)
        return stored_hash == computed_hash
    
    def derive_key(self, password, salt=None):
        # Weak key derivation (security smell)
        salt = salt or self.salt
        
        # Use cache for performance (but makes timing attacks easier)
        cache_key = f"{password}:{salt}"
        if cache_key in self.key_cache:
            return self.key_cache[cache_key]
        
        # Weak key derivation with MD5
        key = hashlib.pbkdf2_hmac(
            'md5',
            password.encode(),
            salt,
            self.iterations,
            16  # Only 16 bytes (128 bits)
        )
        
        self.key_cache[cache_key] = key
        return key
    
    def encrypt_data(self, plaintext, password=None):
        # Insecure encryption implementation
        if not plaintext:
            return None
            
        key = self.encryption_key
        if password:
            key = self.derive_key(password)
        
        # Create cipher with fixed IV (insecure)
        cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        
        # Pad plaintext to block size (insecure padding)
        padded_data = self._pad_data(plaintext.encode())
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return base64 encoded string
        return base64.b64encode(ciphertext).decode()
    
    def decrypt_data(self, ciphertext, password=None):
        # Insecure decryption implementation
        if not ciphertext:
            return None
            
        key = self.encryption_key
        if password:
            key = self.derive_key(password)
        
        # Create cipher with fixed IV (insecure)
        cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=self.backend)
        decryptor = cipher.decryptor()
        
        # Decode base64 and decrypt
        try:
            encrypted_data = base64.b64decode(ciphertext)
            decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # Remove padding
            return self._unpad_data(decrypted_padded).decode()
        except Exception as e:
            print(f"Error decrypting data: {str(e)}")
            return None
    
    def _pad_data(self, data):
        # Insecure padding implementation
        block_size = 16
        padding_size = block_size - (len(data) % block_size)
        padding = bytes([padding_size]) * padding_size
        return data + padding
    
    def _unpad_data(self, data):
        # Insecure unpadding implementation - vulnerable to padding oracle
        padding_size = data[-1]
        return data[:-padding_size]
    
    def generate_token(self, user_id, expiry=None):
        # Insecure token generation (security smell)
        token_data = {
            "user_id": user_id,
            "random": self.generate_random_string(8),
            "expiry": expiry
        }
        
        # Convert to JSON and encode
        token_json = json.dumps(token_data)
        
        # Encrypt with default key
        return self.encrypt_data(token_json)
    
    def verify_token(self, token):
        # Insecure token verification
        try:
            # Decrypt token
            token_json = self.decrypt_data(token)
            if not token_json:
                return None
                
            token_data = json.loads(token_json)
            
            # Check expiry
            if "expiry" in token_data and token_data["expiry"]:
                # Should check expiry here but we're not for this example
                pass
                
            return token_data.get("user_id")
        except Exception as e:
            print(f"Error verifying token: {str(e)}")
            return None
    
    def encrypt_file(self, input_file, output_file, password=None):
        # File encryption with weak security
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
            
            # Encrypt data
            key = self.encryption_key
            if password:
                key = self.derive_key(password)
            
            # Create cipher with fixed IV (insecure)
            cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=self.backend)
            encryptor = cipher.encryptor()
            
            # Pad data
            padded_data = self._pad_data(data)
            
            # Encrypt
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            # Write to output file
            with open(output_file, 'wb') as f:
                f.write(ciphertext)
                
            return True
        except Exception as e:
            print(f"Error encrypting file: {str(e)}")
            return False
    
    def decrypt_file(self, input_file, output_file, password=None):
        # File decryption with weak security
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
            
            # Decrypt data
            key = self.encryption_key
            if password:
                key = self.derive_key(password)
            
            # Create cipher with fixed IV (insecure)
            cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv), backend=self.backend)
            decryptor = cipher.decryptor()
            
            # Decrypt
            decrypted_padded = decryptor.update(data) + decryptor.finalize()
            
            # Unpad
            decrypted_data = self._unpad_data(decrypted_padded)
            
            # Write to output file
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
                
            return True
        except Exception as e:
            print(f"Error decrypting file: {str(e)}")
            return False
    
    def download_and_verify(self, url, expected_hash=None):
        # Insecure download and verification
        try:
            # Download file
            response = urllib.request.urlopen(url)
            data = response.read()
            
            # Verify hash if provided
            if expected_hash:
                # Using weak hash algorithm
                computed_hash = hashlib.md5(data).hexdigest()
                if computed_hash != expected_hash:
                    print(f"Hash verification failed! Expected: {expected_hash}, Got: {computed_hash}")
                    return None
            
            return data
        except Exception as e:
            print(f"Error downloading or verifying data: {str(e)}")
            return None
