#!/usr/bin/env python3
"""
Crypto Manager - Secure File Encryption/Decryption Tool
Provides secure file encryption and decryption using AES-256 with password-based key derivation.
"""

import os
import sys
import getpass
import argparse
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CryptoManager:
    """Handles file encryption and decryption operations."""
    
    SALT_SIZE = 16  # 16 bytes for salt
    IV_SIZE = 16    # 16 bytes for IV (AES block size)
    KEY_SIZE = 32   # 32 bytes for AES-256
    ITERATIONS = 100000  # PBKDF2 iterations
    
    def __init__(self):
        self.backend = default_backend()
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a key from a password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=self.ITERATIONS,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def encrypt_file(self, input_path: str, output_path: str, password: str) -> bool:
        """
        Encrypt a file using AES-256-CBC.
        
        Args:
            input_path: Path to the file to encrypt
            output_path: Path where encrypted file will be saved
            password: Password for encryption
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read input file
            with open(input_path, 'rb') as f:
                plaintext = f.read()
            
            # Generate random salt and IV
            salt = os.urandom(self.SALT_SIZE)
            iv = os.urandom(self.IV_SIZE)
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Perform encryption
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # Add PKCS7 padding
            padding_length = self.IV_SIZE - (len(plaintext) % self.IV_SIZE)
            padded_plaintext = plaintext + bytes([padding_length] * padding_length)
            
            # Encrypt the data
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
            
            # Write encrypted file (salt + iv + ciphertext)
            with open(output_path, 'wb') as f:
                f.write(salt)
                f.write(iv)
                f.write(ciphertext)
            
            print(f"✓ File encrypted successfully: {output_path}")
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: Input file not found: {input_path}")
            return False
        except PermissionError:
            print(f"✗ Error: Permission denied accessing file")
            return False
        except Exception as e:
            print(f"✗ Encryption error: {str(e)}")
            return False
    
    def decrypt_file(self, input_path: str, output_path: str, password: str) -> bool:
        """
        Decrypt a file that was encrypted with encrypt_file.
        
        Args:
            input_path: Path to the encrypted file
            output_path: Path where decrypted file will be saved
            password: Password for decryption
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read encrypted file
            with open(input_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Extract salt, IV, and ciphertext
            salt = encrypted_data[:self.SALT_SIZE]
            iv = encrypted_data[self.SALT_SIZE:self.SALT_SIZE + self.IV_SIZE]
            ciphertext = encrypted_data[self.SALT_SIZE + self.IV_SIZE:]
            
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Perform decryption
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Decrypt the data
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove PKCS7 padding
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]
            
            # Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            
            print(f"✓ File decrypted successfully: {output_path}")
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: Input file not found: {input_path}")
            return False
        except ValueError:
            print(f"✗ Error: Invalid password or corrupted file")
            return False
        except PermissionError:
            print(f"✗ Error: Permission denied accessing file")
            return False
        except Exception as e:
            print(f"✗ Decryption error: {str(e)}")
            return False

def get_password(confirm=False) -> str:
    """Prompt user for password securely."""
    password = getpass.getpass("Enter password: ")
    
    if confirm:
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("✗ Error: Passwords do not match!")
            sys.exit(1)
    
    if len(password) < 8:
        print("✗ Error: Password must be at least 8 characters long!")
        sys.exit(1)
    
    return password

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Crypto Manager - Secure File Encryption/Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt a file:
    python crypto_manager.py encrypt document.txt document.txt.enc
  
  Decrypt a file:
    python crypto_manager.py decrypt document.txt.enc document.txt
        """
    )
    
    parser.add_argument(
        'operation',
        choices=['encrypt', 'decrypt'],
        help='Operation to perform (encrypt or decrypt)'
    )
    
    parser.add_argument(
        'input_file',
        help='Input file path'
    )
    
    parser.add_argument(
        'output_file',
        help='Output file path'
    )
    
    parser.add_argument(
        '-p', '--password',
        help='Password (not recommended for security reasons, will prompt if not provided)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"✗ Error: Input file does not exist: {args.input_file}")
        sys.exit(1)
    
    # Check if output file exists
    if os.path.exists(args.output_file):
        response = input(f"Output file '{args.output_file}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Get password
    if args.password:
        print("Warning: Passing password via command line is insecure!")
        password = args.password
    else:
        password = get_password(confirm=(args.operation == 'encrypt'))
    
    # Perform operation
    manager = CryptoManager()
    
    print(f"\n{'='*60}")
    print(f"Crypto Manager - {args.operation.capitalize()}ing File")
    print(f"{'='*60}")
    print(f"Input:  {args.input_file}")
    print(f"Output: {args.output_file}")
    print(f"{'='*60}\n")
    
    if args.operation == 'encrypt':
        success = manager.encrypt_file(args.input_file, args.output_file, password)
    else:
        success = manager.decrypt_file(args.input_file, args.output_file, password)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)
