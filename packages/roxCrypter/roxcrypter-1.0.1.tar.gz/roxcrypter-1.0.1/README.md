
# roxCrypter: Simple ROT-Based Encryption Module

This Python module, roxCrypter, implements a basic encryption algorithm inspired by the ROT (Rotate) cipher family. It encrypts lowercase Turkish characters using a mathematical transformation.



#

## Installation

__Direct Import:__
```py
import roxCrypter

crypter = roxCrypter.roxCrypter()
encrypted_text = crypter.encrypt_text("Your message here")
```

## Functionality

The roxCrypter class provides two main methods:

encrypt_letter(self, letter): Encrypts a single lowercase Turkish letter using a mathematical formula involving squaring, cubing, taking the remainder, and adding offsets.
encrypt_text(self, text): Encrypts an entire string of text, handling both lowercase Turkish characters and other characters (which are left unchanged). The encrypted text is then base64 encoded for improved readability and storage.
Verification

The check_encrypted_text(self, original_text, encrypted_text) method allows you to verify if the encryption process was successful. It re-encrypts the original text and compares it to the provided encrypted text.

```py
import roxCrypter

crypter = roxCrypter.roxCrypter()
original_text = "Merhaba, dünya!"  # Turkish for "Hello, world!"
encrypted_text = crypter.encrypt_text(original_text)

print("Original Text:", original_text)
print("Encrypted Text:", encrypted_text)

is_valid = crypter.check_encrypted_text(original_text, encrypted_text)
print("Encryption Valid:", is_valid)
```
This code will output:
```
Original Text: Merhaba, dünya!
Encrypted Text: xZ91xLHEn2TDp2QsIHbFn3J5ZCE=
Encryption Valid: True
```

## Security Considerations

It's important to note that roxCrypter is a very simple encryption algorithm and should not be used for sensitive information. It's susceptible to brute-force attacks, statistical analysis, and other cryptanalysis techniques. Consider using more robust encryption methods for real-world applications.

## Future Enhancements

* Implement support for uppercase letters and other character sets.
* Explore more secure encryption algorithms like AES or RSA.
* Add functionality for decryption.