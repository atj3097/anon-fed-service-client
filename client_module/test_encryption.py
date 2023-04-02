import unittest
from encryption import encrypt_data, decrypt_data, encryptor, encoder, decryptor

class TestEncryption(unittest.TestCase):
    def test_encryption_decryption(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        encrypted_data = encrypt_data(data, encryptor, encoder)
        decrypted_data = decrypt_data(encrypted_data, decryptor, encoder)

        # Check if the decrypted data is approximately equal to the original data
        for original, decrypted in zip(data, decrypted_data):
            self.assertAlmostEqual(original, decrypted, delta=1e-3)

if __name__ == '__main__':
    unittest.main()
