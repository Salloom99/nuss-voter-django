from cryptography.fernet import Fernet

decryptor = Fernet(b'FzoBo2bN6JyNyhfGD5JrgOVOWIBBNGMm9RQy6OOebXI=')

def decrypt(qr):
    qr_bytes = qr.encode()
    decrypted_qr = decryptor.decrypt(qr_bytes) 
    return decrypted_qr.decode()

def encrypt(qr):
    qr_bytes = qr.encode()
    decrypted_qr = decryptor.encrypt(qr_bytes) 
    return decrypted_qr.decode()
