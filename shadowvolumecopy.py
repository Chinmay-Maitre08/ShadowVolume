import win32com.client
import os
import time
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cryptography.fernet import Fernet
import getpass

# Specify the file to monitor and the directory where snapshots will be created
file_to_monitor = "E:\\DeepCytes\\Ransomware_Research\\ShadowVolumeCopy\\trial_run.txt"
snapshot_directory = "E:\\Deepcytes\\_Buffers_"
backup_directory = "E:\\DeepCytes\\Ransomware_Research\\ShadowVolumeCopy\\backup"
original_directory = "E:\\DeepCytes\\Ransomware_Research\\ShadowVolumeCopy\\original"
backup_interval_seconds = 3600  # Backup every 1 hour (adjust as needed)

# Password to access the backup
backup_password = "1234"

# Cache the password for 1 minute (adjust as needed)
password_cache_duration = 60
last_password_time = 0
cached_password = None

class VSSFileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_snapshot_time = 0
        self.last_original_content = None

    def on_modified(self, event):
        # When the file is modified, create a new backup, save the original, and encrypt the backup
        print(f"File '{event.src_path}' has been modified. Creating a backup, saving the original, and encrypting the backup.")
        if check_password():
            backup_file()
            save_original()
        else:
            print("Incorrect password. Access to the backup is denied.")

        # Track changes in the file
        track_changes()

        # Check for backups
        current_time = time.time()
        if current_time - self.last_snapshot_time >= backup_interval_seconds:
            self.last_snapshot_time = current_time
            create_volume_snapshot()

def create_volume_snapshot():
    # Implement your VSS snapshot creation logic here
    pass

def backup_file():
    global encryption_key

    # Create a backup of the modified file in the backup directory
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    backup_file_name = f"backup_{current_time}.enc"
    backup_path = os.path.join(backup_directory, backup_file_name)

    try:
        # Encrypt the original file content and save it as a backup
        with open(file_to_monitor, 'rb') as file:
            original_data = file.read()
            encrypted_data = encrypt_data(original_data, encryption_key)

        with open(backup_path, 'wb') as backup_file:
            backup_file.write(encrypted_data)

        print(f"Created encrypted backup: {backup_path}")

    except Exception as e:
        print(f"Error creating backup: {str(e)}")

def save_original():
    # Create a backup of the original file in the original directory
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    original_file_name = f"original_{current_time}.txt"
    original_path = os.path.join(original_directory, original_file_name)

    try:
        # Copy the original file content
        shutil.copy(file_to_monitor, original_path)
        print(f"Saved the original file as: {original_path}")
    except Exception as e:
        print(f"Error saving the original file: {str(e)}")

def track_changes():
    # Implement file change tracking logic here
    pass

def check_password():
    global cached_password
    global last_password_time

    current_time = time.time()

    if cached_password and (current_time - last_password_time) <= password_cache_duration:
        password_attempt = getpass.getpass("Enter the backup password (cached): ")
    else:
        password_attempt = getpass.getpass("Enter the backup password: ")

    if password_attempt == backup_password:
        cached_password = password_attempt
        last_password_time = current_time

        # Generate a new encryption key
        global encryption_key
        encryption_key = Fernet.generate_key()
        
        print(f"Generated encryption key: {encryption_key.decode()}")  # Print the encryption key

        return True
    else:
        print("Incorrect password. Try again.")
        return False

def encrypt_data(data, encryption_key):
    f = Fernet(encryption_key)
    return f.encrypt(data)

if __name__ == "__main__":
    global encryption_key  # Initialize the encryption key

    # Create the directories if they don't exist
    for directory in [snapshot_directory, backup_directory, original_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Initialize the file change handler
    file_change_handler = VSSFileChangeHandler()
    observer = Observer()
    observer.schedule(file_change_handler, path=os.path.dirname(file_to_monitor), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
