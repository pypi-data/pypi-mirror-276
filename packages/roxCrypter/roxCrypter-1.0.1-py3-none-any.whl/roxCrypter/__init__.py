import base64

class roxCrypter:
    def __init__(self):
        self.alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"

    def encrypt_letter(self, letter):
        letter_index = self.alphabet.index(letter.lower()) + 1
        x = letter_index
        result = (2 * x ** 2 + 3 * x + 4) ** 3
        remainder = result % 29
        encrypted_index = remainder + 1
        encrypted_letter = self.alphabet[encrypted_index - 1] 
        return encrypted_letter

    def encrypt_text(self, text):
        encrypted_text = ""
        for letter in text:
            if letter.lower() in self.alphabet:
                encrypted_text += self.encrypt_letter(letter)
            else:
                encrypted_text += letter
        encrypted_text = base64.b64encode(encrypted_text.encode()).decode()
        return encrypted_text

    def check_encrypted_text(self, original_text, encrypted_text):
        return self.encrypt_text(original_text) == encrypted_text
