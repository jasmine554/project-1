from Crypto.Cipher import AES 
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

univPassword= "pass123"

def encrypt(plainText:str, password:str) -> dict:
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=200000)

    cipher = AES.new(key, AES.MODE_GCM)

    cipherText, tag = cipher.encrypt_and_digest(plainText.encode('utf-8'))
    return {'salt':salt, 'nonce':cipher.nonce,'ct':cipherText, 'tag':tag}

def decrypt(data, password):
    key = PBKDF2(password, data['salt'], dkLen=32, count=200000)
    cipher = AES.new(key,AES.MODE_GCM, nonce=data['nonce'])
    return cipher.decrypt_and_verify(data['ct'], data['tag'])

def addRecord():
    name = str(input("Enter patient name: "))
    diagnosis = str(input("Enter diagnosis: "))
    prescription = str(input("Enter prescription: "))

    plainText = f"name: {name}\ndiagnosis: {diagnosis}\nprescription: {prescription}"
    encrypted = encrypt(plainText, univPassword)

    with open("patientRecords.txt", "a") as f:
        f.write(str(encrypted) + "\n")
    print("Record Saved")

def viewRecord():
    password = input("Enter password: ")
    if password != univPassword:
        print("Authentication Failed")
        return
    
    with open("patientRecords.txt", "r") as f:
        for line in f:
            encrypted = eval(line.strip())
            decrypted = decrypt(encrypted, univPassword)
            print("\n=== Record ===")
            print(decrypted.decode('utf-8'))


def main():
    while True:
        print("\n==Symmetric Encryption==")
        print("1. Add record \n2. View record \n3. Exit")
        choice = int(input("Enter choice: "))

        if choice == 1:
            addRecord()
        elif choice == 2:
            viewRecord()
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()



