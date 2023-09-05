import webbrowser

def open_microsoft_store_app_page(app_name):
    base_url = "https://apps.microsoft.com/store/detail/"
    app_url = base_url + app_name.replace(" ", "-")
    webbrowser.open(app_url)

app_name = "python-311/9NRWMJP3717K"
open_microsoft_store_app_page(app_name)

app_name = "powershell/9MZ1SNWT0N5D"
open_microsoft_store_app_page(app_name)

app_name = "windows-terminal/9N0DX20HK701"
open_microsoft_store_app_page(app_name)

base_url = "https://code.visualstudio.com/docs/?dv=win64user"
webbrowser.open(base_url)