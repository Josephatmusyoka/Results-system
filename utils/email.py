import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    try:
        # Set up the server (Gmail example)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your email account
        server.login('your_email@gmail.com', 'your_password')  # Replace with your email and password

        # Craft the message
        msg = MIMEMultipart()
        msg['From'] = 'your_email@gmail.com'  # Replace with your email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail('your_email@gmail.com', to_email, msg.as_string())  # Replace with your email
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error: {e}")
