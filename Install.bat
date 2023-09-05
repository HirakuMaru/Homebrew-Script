@echo off


:start
cls

python ./get-pip.py

cd \
cd "C:\Users\lnhs-student\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"
pip install pycryptodomex
pip install pywin32
pip install AES

pause
exit