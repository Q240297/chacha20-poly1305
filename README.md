# ChaCha20-Poly1305 AEAD Cipher — Educational Implementation

A complete **cryptographic implementation** of the **ChaCha20-Poly1305 AEAD cipher** in Python, conforming to RFC 7539 and RFC 8439. This project demonstrates secure stream cipher design, authenticated encryption, and cryptographic testing against official vectors.

## 📋 Overview

ChaCha20-Poly1305 is a modern, high-performance cipher combining:
- **ChaCha20**: A secure stream cipher based on ARX (Add-Rotate-XOR) operations
- **Poly1305**: A universal polynomial authenticator for message integrity
- **AEAD mode**: Authenticated Encryption with Associated Data

This implementation is suitable for education, research, and understanding modern cryptography, but **not** for production security-critical applications (use `cryptography` or `libsodium` instead).

## 🎯 Features

✅ **Complete ChaCha20 stream cipher**
- Quarter-round permutations (ARX operations)
- Block function with 20 rounds (columns + diagonals)
- Keystream generation (256-bit keys, 96-bit nonces)
- XOR-based encryption

✅ **Poly1305 message authenticator**
- Clamp-based key derivation
- Polynomial accumulation with Clamp(r)
- 128-bit authentication tags
- Constant-time construction

✅ **AEAD ChaCha20-Poly1305 integration**
- Additional Associated Data (AAD) support
- Authenticated encryption & decryption
- RFC 8439 padding & length encoding
- Full test suite with RFC vectors

✅ **Modular, well-documented code**
- Separate modules for each cryptographic primitive
- Helper functions (endianness, block chunking)
- Comprehensive unit tests

## 📁 Project Structure

```
.
├── chacha20.py                    # ChaCha20 cipher implementation
├── block_function.py              # 20-round block function
├── quarter_round.py               # ARX quarter-round operation
├── poly1305.py                    # Poly1305 authenticator
├── aead_chacha20_poly1305.py      # AEAD mode combining both
├── picture.py                     # Image encryption/decryption utility
├── main.py                        # Demo and usage examples
├── tests/                         # Unit test suite
│   ├── test_chacha20.py
│   ├── test_block_function.py
│   ├── test_quarter_round.py
│   ├── test_poly1305.py
│   └── test_aead_chacha20_poly1305.py
├── resources/                     # Test vectors & sample data
│   ├── data.txt                   # RFC 8439 test vectors
│   ├── Images/                    # Original images for demo
│   ├── Encrypted/                 # Encrypted images
│   └── Decrypted/                 # Decrypted results
├── ChaCha20Poly1305_schema.png    # Visual architecture diagram
└── README.md                      # Documentation
```

## 🚀 Quick Start

### Installation

No external dependencies required (pure Python 3.8+).

```bash
git clone https://github.com/yourusername/chacha20-poly1305.git
cd chacha20-poly1305
python3 -m pytest tests/
```

### Basic Usage

```python
from aead_chacha20_poly1305 import (
    aead_chacha20_poly1305_encrypt,
    aead_chacha20_poly1305_decrypt,
)

# 256-bit key & 96-bit nonce (RFC 8439)
key = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
nonce = bytes.fromhex("000000090000004a00000000")

# Optional: additional authenticated data
aad = b"authenticated-metadata"
plaintext = b"Secret message"

# Encrypt & authenticate
ciphertext, tag = aead_chacha20_poly1305_encrypt(key, nonce, plaintext, aad)
print("Ciphertext:", ciphertext.hex())
print("Auth Tag:  ", tag.hex())

# Decrypt & verify
decrypted, tag_check = aead_chacha20_poly1305_decrypt(key, nonce, ciphertext, aad)
assert decrypted == plaintext
assert tag_check == tag
print("✓ Message authenticated and decrypted")
```

### Image Encryption Demo

```python
from picture import encrypt_image, decrypt_image

# Encrypt an image file
encrypt_image(
    input_path="resources/Images/bmw.png",
    output_path="encrypted_bmw.png",
    key=key,
    nonce=nonce
)

# Decrypt it back
decrypt_image(
    input_path="encrypted_bmw.png",
    output_path="decrypted_bmw.png",
    key=key,
    nonce=nonce
)
```

## 🔬 Technical Details

### ChaCha20 Construction

Each 512-bit block is generated from a 256-bit key using 20 rounds of operations on 16 32-bit words:

```
Rounds 0-9:   Column operations (vertical)
Rounds 10-19: Diagonal operations
```

The cipher processes plaintext in 64-byte blocks via XOR, with remaining bytes handled via truncation.

### Poly1305 Authenticator

- **r-clamp**: Derive secret from first 32 bytes of ChaCha20 keystream
- **Accumulation**: Add message blocks as 130-bit numbers in GF(2^130 - 5)
- **Tag**: Final XOR with secret clamp value (first 16 bytes of ChaCha20 block 0)

### AEAD Composition

```
Encrypt(k, n, m, aad):
  1. Generate ChaCha20 keystream block 0 → derive Poly1305 key
  2. Encrypt message with ChaCha20 blocks 1+ → ciphertext
  3. Authenticate [AAD || padding || ciphertext || lengths] → tag
  4. Return (ciphertext, tag)

Decrypt(k, n, c, aad):
  1-3. Same, computing tag over received data
  4. Compare computed vs. received tag (constant-time comparison)
  5. Return plaintext iff tags match, else reject
```

## ✅ Testing

Run the comprehensive test suite:

```bash
# All tests
python3 -m pytest tests/ -v

# Specific test file
python3 -m pytest tests/test_aead_chacha20_poly1305.py -v

# With RFC 8439 vector verification
python3 -m pytest tests/test_chacha20.py::test_rfc_vectors -v
```

**Test Coverage:**
- Quarter-round permutations (ARX correctness)
- Block function with RFC 8439 vectors
- ChaCha20 keystream generation
- Poly1305 tag computation
- Full AEAD encrypt/decrypt cycles
- Edge cases (empty AAD, partial blocks, etc.)

## 📚 References

- **RFC 7539** – ChaCha20 and Poly1305 Architecture
- **RFC 8439** – AEAD Construction, Test Vectors & Errata
- **Daniel J. Bernstein** – Original ChaCha design
- **Martin Aumont** – Poly1305 specification

## ⚠️ Security Disclaimer

**This is an educational implementation** intended to teach cryptographic principles. It:
- ✓ Implements the RFC correctly
- ✓ Includes comprehensive test vectors
- ✓ Uses constant-time operations where practical
- ✗ Is **not audited** for production use
- ✗ May contain timing side-channels or other vulnerabilities

**For production:** Use well-tested libraries like [`cryptography`](https://cryptography.io/), [`libnacl`](https://github.com/saltstack/libnacl), or [`libsodium`](https://doc.libsodium.org/).

## 👨‍💻 Author

**Ibrahim El Komey** – Cybersecurity Student, HELMo  
Academic Project – February 2025  
[LinkedIn](https://linkedin.com/in/ibrahim-el-komey) | [GitHub](https://github.com/yourusername)

## 📄 License

This project is provided for educational purposes. Modify and distribute freely with attribution.

---

**Questions or contributions?** Open an issue or submit a pull request!
