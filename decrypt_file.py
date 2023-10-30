from cryptography.fernet import Fernet
import getpass

# The path to the encrypted backup file
backup_path = "E:\\DeepCytes\\Ransomware_Research\\ShadowVolumeCopy\\backup\\backup_timestamp.enc"

# Your encryption key (replace with your actual key)
encryption_key = f'Z9mpF2izDmI_ZAirGFyNeMOx3wCkrHKaXl4VSXstroU='

def decrypt_file(encrypted_file, key):
    f = Fernet(key)

    try:
        with open(encrypted_file, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)

        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting the file: {str(e)}")
        return None

def main():
    # Prompt for the decryption password
    password = getpass.getpass("Enter the decryption password: ")

    # Validate the password (you can check against your actual password)
    if password == "1234":
        # Decrypt the backup file using the encryption key
        decrypted_content = decrypt_file(backup_path, encryption_key)

        if decrypted_content is not None:
            print("Decrypted Content:")
            print(decrypted_content)
        else:
            print("Failed to decrypt the file.")
    else:
        print("Incorrect password. Access denied.")

if __name__ == "__main__":
    main()
