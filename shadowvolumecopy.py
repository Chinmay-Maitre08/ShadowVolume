import win32com.client
import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import difflib

# Specify the file to monitor and the directory where snapshots will be created
file_to_monitor = "E:\\DeepCytes\\Ransomware_Research\\Testrun.txt"
snapshot_directory = "E:\\Deepcytes\\_Buffers_"
backup_directory = "E:\\DeepCytes\\Ransomware_Research\\backup"
original_directory = "E:\\DeepCytes\\Ransomware_Research\\original"
backup_interval_seconds = 3600  # Backup every 1 hour (adjust as needed)

class VSSFileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_snapshot_time = 0
        self.last_file_content = None

    def on_modified(self, event):
        # When the file is modified, create a new backup and save the original
        print(f"File '{event.src_path}' has been modified. Creating a backup and saving the original.")
        backup_file()
        save_original()

        # Track changes in the file
        track_changes()

        # Check for backups
        current_time = time.time()
        if current_time - self.last_snapshot_time >= backup_interval_seconds:
            self.last_snapshot_time = current_time
            create_volume_snapshot()

def create_volume_snapshot():
    # Initialize the VSS COM interface
    vss = win32com.client.Dispatch("VSS.Service")
    vss_coord = vss.QueryCoordinator()

    # Create a snapshot set
    snapshot_set = vss_coord.StartSnapshotSet()

    # Add the volumes you want to snapshot
    volumes = vss_coord.QueryVolumes()
    for volume in volumes:
        vss_coord.AddToSnapshotSet(volume, provider_id=volume.ProviderId)

    # Prepare the snapshot set
    vss_coord.SetBackupState(True, False, win32com.client.constants.VSS_BT_COPY)

    # Create the snapshots
    vss_coord.DoSnapshotSet()

    # List the created snapshots
    snapshots = vss_coord.QuerySnapshots()
    for snapshot in snapshots:
        print(f"Snapshot ID: {snapshot.SnapshotId}")
        print(f"Snapshot Device Name: {snapshot.DeviceObject}")

def backup_file():
    # Create a backup of the monitored file in the backup directory
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    backup_file_name = f"backup_{current_time}.txt"
    backup_path = os.path.join(backup_directory, backup_file_name)

    try:
        shutil.copy(file_to_monitor, backup_path)
        print(f"Created backup: {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {str(e)}")

def save_original():
    # Save the original file content
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    original_file_name = f"original_{current_time}.txt"
    original_path = os.path.join(original_directory, original_file_name)

    try:
        shutil.copy(file_to_monitor, original_path)
        print(f"Saved the original file as: {original_path}")
    except Exception as e:
        print(f"Error saving the original file: {str(e)}")

def track_changes():
    current_file_content = read_file_content()
    if file_change_handler.last_file_content is not None and current_file_content != file_change_handler.last_file_content:
        print("Changes detected in the file:")
        diff_lines(current_file_content, file_change_handler.last_file_content)
    file_change_handler.last_file_content = current_file_content

def read_file_content():
    with open(file_to_monitor, 'r') as file:
        return file.read()

def diff_lines(content1, content2):
    # Compare the content of two versions of the file and log differences
    lines1 = content1.splitlines()
    lines2 = content2.splitlines()
    diff = difflib.unified_diff(lines2, lines1, lineterm='', fromfile='previous_version', tofile='current_version')
    for line in diff:
        print(line)

if __name__ == "__main__":
    # Create the directories if they don't exist
    for directory in [snapshot_directory, backup_directory]:
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
