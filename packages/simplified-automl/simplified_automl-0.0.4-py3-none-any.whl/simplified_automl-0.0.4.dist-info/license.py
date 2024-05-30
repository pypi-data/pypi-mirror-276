import datetime, os
from cryptography.fernet import Fernet

key = b'ZURcRzqQWVngiwQeKCq1a2Z5iLTm7i6wHKU6mK6LmnM='
fernet = Fernet(key)


def generate_license(expiry_date):
    encrypted_expiry_date = fernet.encrypt(expiry_date.encode())
    with open('license.key', 'w') as f:
        f.write(encrypted_expiry_date.decode())


def check_license():
    file_path = os.path.abspath('license.key')
    if not os.path.exists(file_path):
        with open(file_path, "x") as file:
            generate_license('2023-01-01')

    with open(file_path, 'r') as f:
        encrypted_expiry_date = f.read()
        expiry_date = fernet.decrypt(encrypted_expiry_date).decode()
        if expiry_date < datetime.datetime.now().strftime('%Y-%m-%d'):
            print("The license has expired on " + expiry_date)
            return False;
        else:
            print("The license is valid till " + expiry_date)
            return True;


# generate_license('2024-07-01')
