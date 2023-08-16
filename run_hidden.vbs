Set WshShell = CreateObject("WScript.Shell")

' Define the path to the batch file in the same folder as the VBScript
batch_file_path = WshShell.CurrentDirectory & "\run_python.bat"

' Run the batch file
WshShell.Run batch_file_path, 0
